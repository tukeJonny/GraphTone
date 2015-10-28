server check

リクエストチェック
curl -X GET 'http://localhost:8080?expression=y=x^2&image=True&sound=True&range=-5:5'

zip check
curl -o get.zip -X GET 'http://localhost:8080?expression=y=x^2&image=True&sound=True&range=-5:5'
unzip -Z ./get.zip


test方法
1.terminalを起動する。
2.cd で任意のディレクトリ移動する。
ex. cd /Desktop
3.選んだディレクトリに server.py と image.png sound.mp3を設置
4.pyson ./server.py
5.iosシュミレーターを実行