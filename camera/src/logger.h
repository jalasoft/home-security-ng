
#ifndef _LOGGER_H_
#define _LOGGER_H_

#include <chrono>
#include <fstream>
#include <string>

namespace camera_handler {

class logger {

  std::ofstream stream;
  
  using clock = std::chrono::system_clock;

  public:
    logger(const std::string& file) {
      stream.open(file, std::ofstream::app);
    }

    std::ostream& info() {
      return stream << "INFO " << ": ";
    }

    ~logger() {
      stream.close();
    }
};
}
#endif
