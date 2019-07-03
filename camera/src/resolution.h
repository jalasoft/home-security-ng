
#ifndef _RESOLUTION_H_
#define _RESOLUTION_H_

#include <stdexcept>
#include <sstream>
#include <algorithm>

namespace camera_handler {

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

}

#endif
