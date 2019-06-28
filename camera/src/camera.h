#ifndef __CAMERA_H__
#define __CAMERA_H __

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


namespace camera_handler {

class camera_error : public std::exception {

  std::string file_path;
  std::string reason;
  
  public:
	            
  camera_error(std::string path, const char* r) : file_path{path}, reason{r} {}
		      
  virtual const char* what() const throw() {
    return reason.c_str();
  }  
};

//------------------------------------------------------------------------------

class resolution {
 
  unsigned int width_;
  unsigned int height_;
  unsigned int total_points_;

  friend class resolutions;

  public:
  
  resolution(unsigned int width, unsigned int height) : width_{width}, height_{height}, total_points_(width * height) {}

  
  unsigned int width() const {
    return width_;
  }

  unsigned int height() const {
    return height_;
  }

  std::string to_string() const {
    std::stringstream stream;
    stream << "resolution[" << width_ << "x" << height_ << "]";
    return stream.str();
  }

  bool operator==(resolution& other) {
    return this->width_ == other.width_ && this->height_ == other.height_;
  }

  bool operator<(resolution* other) {
    return this->total_points_ < other->total_points_;
  }
};

std::ostream& operator<<(std::ostream& stream, const resolution& res);

//-------------------------------------------------------------------------------

class resolutions {

  std::vector<resolution*>* resolutions_;

  static bool trid(resolution* r1, resolution* r2) {
    return r1->total_points_ > r2->total_points_;
  }

  public:
  
  resolutions(std::vector<resolution*>* r) : resolutions_{r} {
    if (r->empty()) {
      throw std::invalid_argument("Resolutions must not be empty.");
    }  
    std::sort(resolutions_->begin(), resolutions_->end(), resolutions::trid);
  }
  
  resolution* worst() {
    return resolutions_->back();
  }

  resolution* best() {
    return resolutions_->front();
  }

  resolution* medium() {
    return resolutions_->operator[](size() / 2);
  }

  unsigned int size() {
    return resolutions_->size();
  }

  resolution* operator[](int index) {
    return resolutions_->operator[](index);
  }

  ~resolutions() {
    for(resolution* r : *resolutions_) {
       delete r;
    }

    delete resolutions_;
  }
};

//-------------------------------------------------------------------------------

class frame {

  char* ptr_;
  const size_t size_;
  const resolution* res_;

  public:
  
  frame(char* ptr, size_t size, resolution* res) : ptr_(ptr), size_(size), res_(res) {}

  const resolution* res() const {
    return res_;
  }

  size_t size() const {
    return size_;
  }

  char* ptr() {
     return ptr_;
  }

  void to_file(std::string file) {
    std::ofstream o;
    o.open(file.c_str(), std::ios::binary | std::ios::app);
    o.write(ptr_, size_);
    o.close(); 
  }

  ~frame() {
    free(ptr_);
  }
};

class logger {

  std::ofstream stream;
  
  using clock = std::chrono::system_clock;

  public:
    logger(const std::string& file) {
      stream.open(file, std::ofstream::app);
    }

    std::ostream& info() {
      //clock::time_point time = clock::now();
      //std::time_t t = clock::to_time_t(time);

      return stream << "INFO " << ": ";
    }

    ~logger() {
      stream.close();
    }
};

//-------------------------------------------------------------------------------
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
      int fd = open_file_repeatedly(path);

      check_video_device(fd);
      check_supported_format(fd);

      resolutions_ = new resolutions(load_supported_resolutions(fd));

      close(fd);
    }

    std::string file_path() const {
      return path_;
    }

    resolutions* supported_resolutions() const {
      return resolutions_;
    }

    std::string to_string() const;

    frame* take_frame(resolution*);

    ~camera() {
      delete resolutions_;
    }
};

}
#endif
