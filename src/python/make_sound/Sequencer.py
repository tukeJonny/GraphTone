# -*- coding: utf-8 -*-
import re
import math
from Components import Config
from Components import Clock
from Components import Mixer
from Components import Amplifeir
from decimal import*

class MyCompiler(object):
    def __init__(self, yPosMin, tempo=120, volume=8, on_length=4):
        self.base = 261 #ドの音を、(0, 0)の音として、この音を基準に他の値を求める
        self.tick_position = 0
        self.tempo = tempo
        self.volume = volume
        self.on_length = on_length
        self.yPosMin = yPosMin

        #引数を元に計算される値(音長、テンポ、音量等は固定のため、インスタンス変数として保持させる)
        #発声長の取得
        note_length = int(on_length) if on_length else self.on_length
        self.note_on_tick = (Config.SampleRate / 1.0) * (60.0 / self.tempo) * (4.0 / note_length)
        #発声終了時刻を更新
        self.tick_position += self.note_on_tick
        # 音量指示をアッテネーター値に計算(休符は使わない)
        self.attenuate = self.volume / 15.0

    def get_sequence(self, yPosArray):
        #print "yPosArray = " + str(yPosArray)
        sequence = list()
        yPosArray = map(lambda y: y-self.yPosMin, yPosArray) #グラフのy座標の最小値を、グラフの全ての座標から引いたものを新しくyPosArrayとする

        for ypos in yPosArray:
            note_frequency = (ypos) + self.base #受け取ったy座標を元に、baseを基準にして周波数を求める
            sequence.append((self.attenuate, note_frequency, int(self.tick_position)))
            print  "[+] Append Frequency(y = "+str(ypos)+") = " + str(note_frequency)
            self.tick_position += self.note_on_tick
        return sequence
        
    #def #print _args(self):
        #print  "*"*30 + " BEGIN DEBUG " + "*"*30
        #print  "Tick_Position = " + str(self.tick_position)
        #print  "Tempo = " + str(self.tempo)
        #print  "Volume = " + str(self.volume)
        #print  "On_Length = " + str(self.on_length)
        #print  "Attenuate = " + str(self.attenuate)
        #print  "*"*30 + " END DEBUG " + "*"*30

class Sequencer(object):
    def __init__(self):
        self.tracks = dict()
        self.sequences = dict()
        self.mixer = Mixer()


    def add_track(self, track_id, track_name, input_component, output_component):
        output_component = Amplifeir(source=output_component,
                                     gain=Config.MaxGain,
                                     attenuate=0.5)
        self.tracks[track_id] = (track_name, input_component, output_component)
        self.mixer.add_track(track_id, track_name, output_component)
        self.sequences[track_id] = list()

        
    def add_sequence(self, track_id, sequence_data):
        self.sequences[track_id].extend(sequence_data)
        #print  "Track: " + str(self.sequences[track_id])


    def get_value(self, tick):
        #print  "@get_value: " + str(self.sequences)
        for (track_id, sequence_data) in self.sequences.items():
            if tick > sequence_data[0][2]:
                del sequence_data[0]

            if len(sequence_data) == 0:
                return None
            
            (attenuate, frequency, off_tick) = sequence_data[0]
            ##print  "@get_value: sequence = " + str(frequency)

            (track_name, input_component, output_component) = self.tracks[track_id]

            input_component.frequency = frequency
            output_component.attenuate = attenuate

        return self.mixer.get_value(tick)

    #def debug_args(self):
        #print  "tracks = " + str(self.tracks)
        #print  "sequences = " + str(self.sequences)
        ##print  "mixer = " + str(mixer)