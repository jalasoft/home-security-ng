SRC_DIR=src
BUILD_DIR=build
APP_NAME=camera_handler.so

#------------------------------------
VPATH=$(SRC_DIR) $(BUILD_DIR)

CPP=$(shell cd $(SRC_DIR) && ls *.cpp)
OBJ=$(patsubst %.cpp,%.o,$(CPP))

OUTPUT_OPTION=-o $(BUILD_DIR)/$(@F)

.PHONY: clean all

all: deps $(APP_NAME)


$(APP_NAME): $(OBJ) 
	g++ -o $(BUILD_DIR)/$@ -shared -O3 -Wall $(addprefix $(BUILD_DIR)/,$(^F))

-include build/deps

clean:
	[ -d $(BUILD_DIR) ] && rm -rf $(BUILD_DIR)

build/deps: 
	mkdir -p $(@D)
	cd $(SRC_DIR) && g++ -MM $(CPP) >../$(BUILD_DIR)/deps
