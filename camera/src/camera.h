#ifndef __CAMERA_H__
#define __CAMERA_H __

#include <vector>
#include <string>
#include <linux/videodev2.h>

#include "logger.h"
#include "resolution.h"
#include "file_descriptor.h"
#include "frame.h"

/*
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <string>
#include <fcntl.h>
#include <sstream>
#include <unistd.h>
#include <tuple>
#include <stdexcept>
#include <linux/videodev2.h>
#include <chrono>
#include <ctime>
#include <chrono>
#include <thread>
*/


namespace camera_handler {

class camera {

  std::string path_;
  resolutions* resolutions_;
  logger logger_;

  int open_file_repeatedly(const std::string& file);
  void check_video_device(int&);
  void check_supported_format(int&);
  std::vector<resolution*>* load_supported_resolutions(int&);

  void set_frame_format(int fd, resolution*);
  void request_buffer(int fd, int count);
  std::tuple<v4l2_buffer, void*> query_buffer(int fd, int index);
  void activate_streaming(const int, v4l2_buffer);
  void queue_buffer(const int, v4l2_buffer);
  void dequeue_buffer(const int, v4l2_buffer);
  void deactivate_streaming(const int, v4l2_buffer);

  public:
    
    camera(const std::string& path = "/dev/video0", const std::string& log_file = "camera.log") : path_{path}, logger_{log_file} {
      file_descriptor file(path, &logger_);
      int fd = file.descriptor();

      check_video_device(fd);
      check_supported_format(fd);

      resolutions_ = new resolutions(load_supported_resolutions(fd));
    }

    std::string file_path() const {
      return path_;
    }

    resolutions* supported_resolutions() const {
      return resolutions_;
    }

    std::string to_string() const;

    frame* take_frame(resolution*);
    frame* take_frame_repeatedly(resolution*);

    ~camera() {
      delete resolutions_;
    }
};
}
#endif
