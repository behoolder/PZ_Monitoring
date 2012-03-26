from sensor.sensor import get_sensor
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return 'test - dziala'

@app.route("/get_data/")
def get_data():
    try:
        a = get_sensor().get_data().get_str_info()
    except Exception, e:
        print e
    else:
        return a

# run app
app.run(host = '0.0.0.0')
