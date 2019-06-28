from flask import Flask
from flask import request
import logging
import parameters

app = Flask(__name__)

args = parameters.Parameters.parse()
logfile = args.param("logfile").value

logging.basicConfig(filename=logfile, level=logging.DEBUG)

@app.route("/api/camera/<camera_name>/")
def hello(camera_name, methods =  ['GET']):
    logging.debug("cusicek")

    refresh = request.args.get("refresh")

    logging.info("refresh je " + refresh)
    return "Nazdarek...."


if __name__ == "__main__":
    app.run(host='0.0.0.0')

