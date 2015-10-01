# -*- coding: utf-8 -*-
from Components import Config
from Components import SquareWaveOscillator
from Components import Clock
from Components import Renderer
from Components import WaveFileSink

from Sequencer import Sequencer
from Sequencer import MMLCompiler

from subprocess import*
from time import*
from os import*


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

xPosArray = [r for r in range(-5, 5)]
yPosArray = [r**2 for r in range(-5, 5)]

sounds = ["c", "d", "e", "f", "g", "a", "b", "r"]
mappingTable = {}

#マッピングテーブルを初期化
def initMappingTable(yPosArray):
    minY = min(yPosArray)
    maxY = max(yPosArray)
    diff = abs(maxY - minY)
    print "maxY = " + str(maxY) + ", minY = " + str(minY)
    eachSectionRange = diff / len(sounds)
    sum_value = eachSectionRange
    for r in range(len(sounds)):
        print str(sum_value) + " = " + str(sounds[r])
        mappingTable[sum_value] = sounds[r]
        sum_value += eachSectionRange
    print "Initted Mapping Table: " + str(mappingTable)

#マッピングテーブルに基づき、引数に渡されたy座標が含まれている範囲のセクションの音を返す
def getMappedSound(y):
    print "Received value: " + str(y)
    idx = 0
    for key,val in sorted(mappingTable.items()):
        if y <= key or idx == len(sounds) - 1:
            return val
        idx += 1

#x座標, y座標に対して、パラメータを設定した音符１つ分のMMLコマンド文字列を返す
def getMMLCommandString(x, y, nextX, nextY):
    #print "Mapped Table: " + str(mappingTable)
    ret = ""
    #音量(Default: 10)
    ret += "V10"
    #テンポ(Default: 10)
    ret += "T10"
    #音(マップされた値に応じて変化させる)
    ret += getMappedSound(y)
    print "Mapped Sound is " + str(ret[6:])
    #オクターブ増減
    diffy = nextY - y
    if diffy >= 0: #次のy座標の方が大きいならば１オクターブ上げる
        ret += ">"
    else:
        ret += "<" #今見ているy座標の方が大きいならば１オクターブ下げる
    return ret

#MMLコマンド生成(ここで、x,y座標を用いて楽譜を生成する)
def generateMMLCommandsString(xPosArray, yPosArray):
    MML = ""
    initMappingTable(yPosArray)
    for r in range(1, len(xPosArray)):
        MML += getMMLCommandString(xPosArray[r-1], yPosArray[r-1], xPosArray[r], yPosArray[r])
    MML += "V10T10" + getMappedSound(yPosArray[len(yPosArray)-1])
    return MML

#Wavファイルの生成
def generateWavFile(MMLCommands):
    mml_compiler = MMLCompiler()
    music_sequence = mml_compiler.to_sequence(MMLCommands)
    
    osc = SquareWaveOscillator()
    sequencer = Sequencer()
    sequencer.add_track(0, "tone1", osc, osc)
    sequencer.add_sequence(0, music_sequence)

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






























