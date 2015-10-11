# -*- coding: utf-8 -*-
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

from Sequencer import MMLCompiler
from Sequencer import Sequencer

from subprocess import*
from time import*
from os import*
import re


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

xPosArray = [r for r in range(-20, 21)]
yPosArray = [r**2 for r in range(-20, 21)]

#sounds = ['c', 'c+', 'd', 'd+', 'e', 'e+', 'f', 'f+', 'g', 'g+', 'a', 'a+', 'b', 'b+']
sounds = ['c', 'd', 'e', 'f','g', 'a','b']
rev_sounds = ['b', 'a', 'g', 'f', 'e', 'd','c']
mappingTable = {}
reverseMappingTable = {}

mml_pattern = re.compile(r"V\d+T\d+>*[cdefgab]", re.IGNORECASE)

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
    


#マッピングテーブルに基づき、引数に渡されたy座標が含まれている範囲のセクションの音を返す
def getMappedSound(y):
    print "Received value: " + str(y)
    absY = abs(y)
    if y >= 0:
        div = absY / len(sounds)
    else:
        div = absY / (len(sounds)+1)
    mod = absY % len(sounds)
    
    ret = ""
    
    if y < 0:
        mod -= 1

    if y >= 0:
        
        #ret += "b+"
        print "Octave count is ", div
        ret += ">"*div
        #ret += sounds[mod]
        ret += "c"
    else:
        
        #ret += "b+"
        print "Octave count is ", div
        ret += "<"*div
        #ret += rev_sounds[mod]
        ret += "c"
    
    return ret

#x座標, y座標に対して、パラメータを設定した音符１つ分のMMLコマンド文字列を返す
def getMMLCommandString(x, y):
    #print "Mapped Table: " + str(mappingTable)
    ret = ""
    #音量(Default: 10)
    ret += "V10"
    #テンポ(Default: 120)
    ret += "T120"
    #音(マップされた値に応じて変化させる)
    ret += getMappedSound(y)
    print "Mapped Sound is " + str(ret[4:])

    return ret

#MMLコマンド生成(ここで、x,y座標を用いて楽譜を生成する)
def generateMMLCommandsString(xPosArray, yPosArray):
    MML = ""
    #initMappingTable(yPosArray)
    for r in range(len(xPosArray)):
        MML += getMMLCommandString(xPosArray[r], yPosArray[r])
    return MML

#Wavファイルの生成

def generateWavFile(MMLCommands):
    mml_compiler = MMLCompiler()
    sequencer = Sequencer()
    tone1 = Tone()
    sequencer.add_track(0, "manual", tone1, tone1)
    print "regex result...", re.findall(mml_pattern, MMLCommands)
    for mml in re.findall(mml_pattern, MMLCommands):
        #print "Track_num = ", track_num
        print "mml = ", mml
        sequence = mml_compiler.to_sequence(mml)
        sequencer.add_sequence(0, sequence)
        print "Sequence Added."

    sink = WaveFileSink(output_file_name="output.wav")
    clock = Clock()
    renderer = Renderer(clock=clock, source=sequencer, sink=sink)
    renderer.do_rendering()

#Wavファイル -> mp3ファイル変換
def convertWavToMp3():
    check_output('echo "y" | ffmpeg -i output.wav -ab 128 output.mp3', shell=True) #yを出力させているのは、同じファイル名のmp3ファイルを上書きするようにするため

def main():
    MML = generateMMLCommandsString(xPosArray, yPosArray)
    print "Generated MML: " + MML
    generateWavFile(MML)
    convertWavToMp3()

if __name__ == "__main__":
    main()






























