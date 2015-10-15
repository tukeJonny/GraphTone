server リクエストチェック方法

request
curl -X GET 'http://localhost:8080?expression=y=x^2&image=True&sound=True&range=-5:5'

zip check
curl -o get.zip -X GET 'http://localhost:8080?expression=y=x^2&image=True&sound=True&range=-5:5'
unzip -Z ./get.zip


test方法
1.terminalを起動する。
2.cd で任意のディレクトリ移動する。
ex. cd /Desktop
3.選んだディレクトリに server.py と image.png と sound.mp3を置く
ex. send.txtの中に文字を書いとく。
ex. /Desktop/server.py    /Desktop/send.txt
4.pyson ./server.py
5.iosシュミレーターを実行