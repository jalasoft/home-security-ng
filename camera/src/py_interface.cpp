#include "camera.h"

extern "C" {

  camera_handler::camera* new_camera(const char* device_file, const char* log_file) {
    return new camera_handler::camera(std::string(device_file), std::string(log_file));
  }

  const char* camera_file_path(camera_handler::camera* camera) {
    return camera->file_path().c_str();
  }

  void release_camera(camera_handler::camera* camera) {
    delete camera;
  }

  camera_handler::resolutions* camera_supported_resolutions(camera_handler::camera* camera) {
    return camera->supported_resolutions();
  }

  camera_handler::resolution* supported_resolutions_best(camera_handler::resolutions* resolutions) {
    return resolutions->best();
  }

  camera_handler::resolution* supported_resolutions_medium(camera_handler::resolutions* resolutions) {
    return resolutions->medium();
  }

  camera_handler::resolution* supported_resolutions_worst(camera_handler::resolutions* resolutions) {
    return resolutions->worst();
  }

  unsigned int supported_resolutions_size(camera_handler::resolutions* resolutions) {
    return resolutions->size(); 
  }

  camera_handler::resolution* supported_resolutions_at(camera_handler::resolutions* resolutions, unsigned int index) {
    return resolutions->operator[](index);
  }

  unsigned int resolution_width(camera_handler::resolution* res) {
    return res->width();
  }

  unsigned int resolution_height(camera_handler::resolution* res) {
    return res->height();
  }

  camera_handler::frame* camera_take_frame(camera_handler::camera* camera, camera_handler::resolution* resolution) {
    return camera->take_frame(resolution);
  }

  void camera_release_frame(camera_handler::frame* frame) {
    delete frame;
  }

  unsigned int frame_size(camera_handler::frame* frame) {
    return frame->size();
  }

  void* frame_ptr(camera_handler::frame* frame) {
    return frame->ptr();
  }
}

