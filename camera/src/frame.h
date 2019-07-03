#ifndef _FRAME_H_
#define _FRAME_H_

#include <fstream>

namespace camera_handler {

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
}
#endif
