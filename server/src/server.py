from flask import Flask
from flask import request
import logging
import parameters
import json
import camera

app = Flask(__name__)

args = parameters.Parameters.parse()
logfile = args.param("logfile").value

logging.basicConfig(filename=logfile, level=logging.DEBUG)

camera_lib = args.param("camera_lib")

logging.info("Initializing camera library...")

camera.init(camera_lib.value)
camera1 = camera.camera_handler("/dev/video0")

@app.route("/api/camera/<camera_name>/")
def hello(camera_name, methods =  ['GET']):
    logging.debug("cusicek")

    refresh = request.args.get("refresh")

    logging.info("refresh je " + refresh)

    payload = {
      "resolution": "bleeee",
      "data": "obrazek"
    }

    asStr = json.dumps(payload)

    return asStr


if __name__ == "__main__":
    app.run(host='0.0.0.0')

