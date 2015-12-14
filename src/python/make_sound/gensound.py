# -*- coding: utf-8 -*-
from subprocess import*
from time import*
from os import*
from decimal import*
from math import*
import sys
import re

import numpy as np
import matplotlib.pyplot as plt
import pylab
import scipy.io.wavfile

from Components import Config
from Components import ConstantValueGenerator
from Components import SquareWaveOscillator
from Components import SineWaveOscillator
from Components import Subtraction
from Components import Inverter
from Components import FrequencyModulator
from Components import Gate
from Components import Clock
from Components import Mixer
from Components import Amplifeir
from Components import WaveFileSink
from Components import Renderer
from Sequencer import MyCompiler
from Sequencer import Sequencer





#MML = "t120o4l4cdefedcrefgagfercrcrcrcrl16crcrdrdrererfrfrl4edcr"
#MML = "cdefgabc+"

#MMLの書き方はここ(http://www15.big.or.jp/~annex-hp/anxmid/nyumon.html)を参考に...
#これだと出力がwavなんだけど、ffmpeg -i output.wav -ab 128 output.mp3
#ってすればいけるっぽい(http://www.xucker.jpn.org/pc/ffmpeg_wav.html) -> いけた

#MMLコマンド調査
#Tempoについて. デフォルト120. 試しに10とか５にしたらめっちゃ長く音がなった. １音づつ調整できる
#Volumeについて. デフォルト8. これも１音づつ調整できる(0 ~ 15の値をとる)
#Octaveについて. デフォルト4. 大きい値にすると、金切音みたいになる...(要は高い音になるってこと)
#音長について. デフォルトL. 2^nの値あるらしい. 俺の耳がおかしいのかもしらんが、違いがようわからん.
#半音について. デフォルトなし. +で#、-で♭を意味するらしい. 聞いた感じ、#は普通？の音で ♭はより低い音な気がした

#構文(N,n=整数)
#MML = <TN|VN|ON|LN><c|d|e|f|g|a|b|r><+|-><1|2|4|8|16|32|64|...|2^n><.>< <> >
#LNumは、音長のデフォルト値をNumに設定するというものである

#まとめ
#変化させられるものとしては
#音(ドレミファソラシド), テンポ(早さ), 音量(音の大きさ), オクターブ(音として２倍の振動数になるらしい), 音長(ようわからん.なんか４分音符とかうんたらとかあるらしいけど...), 半音,　付点(ようわからん)
#テンポ
#音量
#オクターブ
#音長デフォルト値
#音
#半音
#音長
#付点
#オクターブ増減

outputWavFileName = "graph.wav"
outputMp3FileName = "graph.mp3"

#浮動小数点数ステップに対応したrange
def drange(begin, end, step):
    n = begin
    while n <= end+step:
        yield n
        n += step
xyrange = 100
formula = lambda x: x**3
#xPosArray = [x for x in drange(-float(xyrange), float(xyrange), 0.1)]
#yPosArray = [formula(x) for x in drange(-float(xyrange), float(xyrange), 0.1)]

xPosArray = [x for x in drange(-float(xyrange), float(xyrange), 0.1)]
yPosArray = [formula(x) for x in drange(-float(xyrange), float(xyrange), 0.1)]


#Toneクラス
class Tone(object):
    def __init__(self):
        self.osc1 = SquareWaveOscillator()
        self.osc2 = SquareWaveOscillator()

        self.mixer = Mixer()
        self.mixer.add_track(0, "base_tone", Gate(source=self.osc1, state=(True, False)))
        self.mixer.add_track(1, "detuned_tone",
                             Gate(Inverter(
                                 source=FrequencyModulator(
                                     source=self.osc2,
                                     delta=ConstantValueGenerator(2))),
                                  state=(False, True)))

    def get_value(self, tick):
        return self.mixer.get_value(tick)
    
    def get_frequency(self):
        return self.osc1.frequency

    def set_frequency(self, value):
        self.osc1.frequency = value
        self.osc2.frequency = value

    frequency = property(get_frequency, set_frequency)

#Wavファイルの生成
def generateWavFile(yPosArray, tempo, volume):
    yPosMin = min(yPosArray)
    my_compiler = MyCompiler(yPosMin, tempo=tempo, volume=volume)
    sequencer = Sequencer()
    tone1 = Tone()
    sequencer.add_track(0, "manual", tone1, tone1)
    sequence = my_compiler.get_sequence(yPosArray)
    sequencer.add_sequence(0, sequence)

    sink = WaveFileSink(output_file_name=outputWavFileName)
    clock = Clock()
    renderer = Renderer(clock=clock, source=sequencer, sink=sink)
    renderer.do_rendering()

#Wavファイル -> mp3ファイル変換
def convertWavToMp3():
    check_output('echo "y" | ffmpeg -i ' + outputWavFileName + ' -ab 128 ' + outputMp3FileName, shell=True) #yを出力させているのは、同じファイル名のmp3ファイルを上書きするようにするため

##################################### Debug #####################################
def plot_waveform ( waveform , sampling_rate ):
    sampling_interval = 1.0 / sampling_rate
    times = np.arange ( len ( waveform )) * sampling_interval
    pylab.plot ( times , waveform ) # pair of two x - and y - coordinate lists / arrays
    pylab.title ( ' Wav File Analysis ' )
    pylab.xlabel ( ' Time [ sec ] ' )
    pylab.ylabel ( ' Amplitude ' )
    pylab.xlim ([0 , len ( waveform ) * sampling_interval ])
    pylab.ylim ([ -1 , 1])
    pylab.show ()

def analyzeWav():  
    #filename = fn
    sampling_rate , waveform = scipy.io.wavfile.read ( "output.wav" )
    waveform = waveform / 32768.0 # assume 16 - bit integer
    plot_waveform ( waveform , sampling_rate )

def analyzeYPos():
    multipleForArray = lambda y: y + 261
    yArray = map(multipleForArray, yPosArray)
    plt.plot(xPosArray, yArray)
    plt.savefig('pulse.png')
    plt.plot(xPosArray, yPosArray)
    plt.savefig('graph.png')
##################################### Debug #####################################

def genSound(yPosArray, tempo=1500, volume=10):
    generateWavFile(yPosArray, tempo=tempo, volume=volume)
    convertWavToMp3()

def main():
    print "xPosArray = " + str(xPosArray)
    print "yPosArray = " + str(yPosArray)
    genSound(yPosArray)


if __name__ == "__main__":
    main()


























