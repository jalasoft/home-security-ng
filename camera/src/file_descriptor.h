
#ifndef _FILE_DESCRIPTOR_H_
#define _FILE_DESCRIPTOR_H_

#include "logger.h"
#include "camera_error.h"

#include <fcntl.h>
#include <chrono>
#include <string>
#include <thread>
#include <unistd.h>

namespace camera_handler {

class file_descriptor {

  const int attempts_total = 60;
  const int attempt_delay_millis = 250;

  int descriptor_;
  logger* logger_;

  public:
    file_descriptor(const std::string& path, logger* l) : logger_(l) {
      unsigned int attempt_counter = 0;
      
      do {
	logger_->info() << "Attempt " << attempt_counter << " to open camera file " << path << std::endl;      
        descriptor_ = open(path.c_str(), O_RDWR);

	if (descriptor_ > 0) {
	  return;
	}
	
	logger_->info() << "Attempt was not successfull: " << descriptor_ << std::endl;

	std::this_thread::sleep_for(std::chrono::milliseconds(attempt_delay_millis));
      } while(descriptor_ < 0 && attempt_counter++ < attempts_total);      

      logger_->info() << "No attempt has been successfull" << std::endl;

      throw new camera_error(path, "Cannot open file");
    }

    int descriptor() {
      return descriptor_;
    }

    ~file_descriptor() {
      logger_->info() << "Closing file " << descriptor_ << std::endl;
      int g = close(descriptor_);
      logger_->info() << "result: " << g << std::endl;
    }
};
}
#endif
