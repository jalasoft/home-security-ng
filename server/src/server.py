from flask import Flask
from flask import request
import logging
import parameters
import json
import base64
from camera_registry import camera_registry


app = Flask(__name__)

args = parameters.Parameters.parse()
logfile = args.param("logfile").value
camera_log_file = args.param("camera_log_file").value

logging.basicConfig(filename=logfile, level=logging.DEBUG)

camera_lib = args.param("camera_lib").value

logging.info("Initializing camera library...")
logging.debug("Camera logs directed to " + camera_log_file)

_qualities = [ "worst", "medium", "best" ]


cameras = camera_registry(camera_lib, camera_log_file)

def _extract_resolution(cam, quality_id):
    if quality_id is None:
        quality_id = 0

    res = cam.supported_resolutions()
   
    try:
        quality_id = int(quality_id)
    except ValueError:
        if quality_id == "worst":
            return res.worst()
        elif quality_id == "medium":
            return res.medium()
        elif quality_id == "best":
            return res.best()
        else:
            raise Exception("Quality must be a word 'worst', 'medium', 'best' or a number >= 0")

    if quality_id < 0:
        raise Exception("Quality must be a positive number.")

    if quality_id >= res.size():
        raise Exception("Quality must not be greater than " + str(res.size()) + ".")

    return res[quality_id]

@app.route("/api/camera/<camera_name>/resolution")
def get_supported_resolutions(camera_name, methods = ['GET']):
    logging.info("Supported resolutions requested for camera '" + camera_name + "'.")
    
    if camera_name not in cameras:
        return "No camera '" + camera_name + "' found.", 400

    payload = []

    resolutions = cameras[camera_name].supported_resolutions()

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
    
    if camera_name not in cameras:
        return "No camera '" + camera_name + "' found.", 400

    logging.debug("camera '" + camera_name + "' is about to take a frame")

    resolution = None
    cam = cameras[camera_name]

    try:
        resolution = _extract_resolution(cam, request.args.get("quality"))
    except Exception as ex:
        logging.error(str(ex))
        return str(ex), 400
    
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

