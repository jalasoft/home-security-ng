from flask import Flask
from flask import request
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

camera_lib = args.param("camera_lib").value

logging.info("Initializing camera library...")
logging.debug("Camera logs directed to " + camera_log_file)

_qualities = [ "worst", "medium", "best" ]

camera.init(camera_lib)    
    
cam = camera.camera_handler('/dev/video0', camera_log_file)

def _extract_resolution(cam, quality_id):
    if quality_id is None:
        quality_id = 0

    res = cam.supported_resolutions()
    
    if int(quality_id) < 0:
        raise Exception("Quality must be a positive number.")

    if int(quality_id) >= res.size():
        raise Exception("Quality must not be greater than " + str(res.size()) + ".")

    return res[int(quality_id)]

def _get_resolution(value, camera):
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


@app.route("/api/camera/<camera_name>/resolution")
def get_supported_resolutions(camera_name, methods = ['GET']):
    logging.info("Supported resolutions requested for camera '" + camera_name + "'.")
    
    payload = []
    resolutions = cam.supported_resolutions()

    for i in range(0, resolutions.size()):
        res = resolutions[i]
        payload.append({
            "id": i,
            "width": res.width,
            "height": res.height
        })
    return json.dumps(payload)

@app.route("/api/camera/<camera_name>")
def take_frame(camera_name, methods =  ['GET']):

    logging.debug("camera '" + camera_name + "' is about to take a frame")

    resolution = None
    try:
        resolution = _extract_resolution(cam, request.args.get("quality"))
    except Exception as ex:
        logging.error(str(ex))
        return str(ex), 400
    
    #with camera.camera_handler("/dev/video0", camera_log_file) as cam:
    
    logging.debug("Having supported reslution " + str(resolution.width) + "x" + str(resolution.height))

    with cam.take_frame(resolution) as frame:
        logging.info("A frame has been taken of size " + str(frame.size()) + "bytes")

        data = frame.bytes()

        b64string = str(base64.b64encode(data), "UTF-8")       

        payload = {
            "resolution_width": str(resolution.width),
            "resolution_height": str(resolution.height),
            "data": b64string
        }
        return json.dumps(payload)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

