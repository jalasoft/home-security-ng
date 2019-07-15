import camera


class camera_registry:

  def __init__(self, camera_lib, camera_log_file):
    camera.init(camera_lib)

    self.camera_mapping = {
      "obyvak1": camera.camera_handler("/dev/video0", camera_log_file)
    }

  def __contains__(self, name):
    return name in self.camera_mapping

  def camera(self, name):
    return self.camera_mapping.get(name)

  def __getitem__(self, name):
      return self.camera_mapping[name]

