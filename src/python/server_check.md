server check

request
curl -X GET 'http://localhost:8080?expression=y=x^2&image=True&sound=True&range=-5:5'

zip check
curl -o get.zip -X GET 'http://localhost:8080?expression=y=x^2&image=True&sound=True&range=-5:5'
unzip -Z ./get.zip