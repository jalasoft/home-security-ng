import ctypes

lib = ctypes.cdll.LoadLibrary('build/camera_handler.so')

class camera_handler:

    def __init__(self, video_file = '/dev/video0'):  
      lib.new_camera.argtypes = [ ctypes.c_char_p ]
      lib.camera_file_path.restype = ctypes.c_char_p
      lib.release_camera.argtypes = [ ctypes.c_void_p ]
      lib.supported_resolutions_best.argtypes = [ ctypes.c_void_p ]
      lib.supported_resolutions_medium.argtypes = [ ctypes.c_void_p ]
      lib.supported_resolutions_worst.argtypes = [ ctypes.c_void_p ]
      lib.supported_resolutions_size.argtypes = [ ctypes.c_void_p ]
      lib.supported_resolutions_size.restype = ctypes.c_int
      lib.supported_resolutions_at.argtypes = [ ctypes.c_void_p, ctypes.c_int ]
      lib.resolution_height.argtypes = [ ctypes.c_void_p ]
      lib.resolution_height.restype = ctypes.c_int
      lib.camera_take_frame.argtypes = [ ctypes.c_void_p, ctypes.c_void_p ]
      lib.camera_take_frame.restype = ctypes.c_void_p
      lib.camera_release_frame.argtypes = [ ctypes.c_void_p ]
      lib.frame_size.argtypes = [ ctypes.c_void_p ]
      lib.frame_size.restype = ctypes.c_int
      lib.frame_ptr.argtypes = [ ctypes.c_void_p ]
      lib.frame_ptr.restype = ctypes.c_void_p

      string_as_bytes = str.encode(video_file)
      self.handler = lib.new_camera(ctypes.c_char_p(string_as_bytes))

    def file_path(self):
        return lib.camera_file_path(self.handler)

    def supported_resolutions(self):
        res_handler = lib.camera_supported_resolutions(self.handler)
        return supported_resolutions(res_handler)
  
    def take_frame(self, resolution):
        frame_handler = lib.camera_take_frame(self.handler, resolution.handler)
        return frame(frame_handler, resolution)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        lib.release_camera(self.handler)

class supported_resolutions:

    def __init__(self, handler):
        self.handler = handler;
    
    def best(self):
        res_handler = lib.supported_resolutions_best(self.handler)
        return resolution(res_handler)

    def worst(self):
        res_handler = lib.supported_resolutions_worst(self.handler)
        return resolution(res_handler)

    def medium(self):
        res_handler = lib.supported_resolutions_medium(self.handler)
        return resolution(res_handler)
    
    def size(self):
        return lib.supported_resolutions_size(self.handler)

    def __getitem__(self, index):
        res_handler = lib.supported_resolutions_at(self.handler, index)
        return resolution(res_handler)
    
    def __iter__(self):
        return resolution_iterator(self)


class resolution_iterator:

    def __init__(self, iterable):
        self.index = 0
        self.iterable = iterable

    def __next__(self):
        if self.index >= self.iterable.size():
            raise StopIteration()

        value = self.iterable[self.index]
        self.index += 1
        return value

class resolution:

    def __init__(self, handler):
        self.handler = handler
        self.height = lib.resolution_height(self.handler)
        self.width = lib.resolution_width(self.handler)

    def width(self):
        return self.width

    def height(self):
        return self.height

    def __str__(self):
        return f"resolution[{self.width}x{self.height}]"


class frame:

    def __init__(self, handler, resolution):
        self.handler = handler;
        self.resolution = resolution;

    def size(self):
        return lib.frame_size(self.handler)

    def bytes(self):
        ptr = lib.frame_ptr(self.handler)
        return ctypes.string_at(ptr, self.size())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        lib.camera_release_frame(self.handler)

######################################################################################

if __name__ == "__main__":
        
    with camera_handler('/dev/video0') as camera:
        resolutions = camera.supported_resolutions()

        print("size: " + str(resolutions.size()))
        print(f"best: {resolutions.best()}")
        print(f"medium: {resolutions.medium()}")
        print(f"worst: {resolutions.worst()}")

        for r in resolutions:
            print(r)

        with camera.take_frame(resolutions.best()) as frame:
            print(f"size: {frame.size()}")
        
            data = frame.bytes()
            print("writing frame into obj.jpg")
            with open("obr.jpg", "wb") as file:
                file.write(data)

