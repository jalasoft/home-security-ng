from flask import Flask
from flask import request
import logging
import parameters
import json

app = Flask(__name__)

args = parameters.Parameters.parse()
logfile = args.param("logfile").value

logging.basicConfig(filename=logfile, level=logging.DEBUG)

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

