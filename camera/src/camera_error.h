
#ifndef _CAMERA_ERROR_H_
#define _CAMERA_ERROR_H_

#include <string>
#include <stdexcept>

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

}
#endif
