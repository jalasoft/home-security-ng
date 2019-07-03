from flask import Flask
from flask import request
#from flask import Response
import logging
import parameters
import json
import camera
import base64

app = Flask(__name__)

args = parameters.Parameters.parse()
logfile = args.param("logfile").value
camera_log_file = args.param("camera_log_file").value

logging.basicConfig(filename=logfile, level=logging.DEBUG)

camera_lib = args.param("camera_lib")

logging.info("Initializing camera library...")
logging.debug("Camera logs directed to " + camera_log_file)

_qualities = [ "worst", "medium", "best" ]

def _get_quality(value):
    if value is None:
        return "medium"

    if value not in _qualities:
        raise Exception("incorrect quality specified: '" + value + "'. Use one of worst, medium or best.")

    return value

def _get_resolution(value, camera):
    print("hodnota je " + value)
    if value == "worst":
        print("davam WORST")
        return camera.supported_resolutions().worst()
    elif value == "medium":
        print("davam MEDIUM")
        return camera.supported_resolutions().medium()
    elif value == "best":
        print("davam BEST")
        return camera.supported_resolutions().best()
    else:
        raise Exception("Unexpected resolution name '" + value + "'.")


@app.route("/api/camera/<camera_name>/")
def take_frame(camera_name, methods =  ['GET']):

    logging.debug("camera '" + camera_name + "' is about to take a frame")

    quality = None
    try:
        quality = _get_quality(request.args.get("quality"))
    except Exception as ex:
        logging.error(str(ex))
        return str(ex), 400

    camera.init(camera_lib.value)
    
    with camera.camera_handler("/dev/video0", camera_log_file) as cam:
    
        logging.info("Got request to take a frame for '" + camera_name + "' with quality '" + quality + "'.")

        resolution = _get_resolution(quality, cam)

        logging.debug("Having supported reslution " + str(resolution.width) + "x" + str(resolution.height) + " that matches " + quality + " quality.")

        with cam.take_frame(resolution) as frame:
            logging.info("A frame has been taken of size " + str(frame.size()) + "bytes")

            data = frame.bytes()

            b64string = str(base64.b64encode(data), "UTF-8")       

            payload = {
                "resolution_width": str(resolution.width),
                "resolution_height": str(resolution.height),
                "data": b64string
            }
            asStr = json.dumps(payload)
            return asStr        



if __name__ == "__main__":
    app.run(host='0.0.0.0')

