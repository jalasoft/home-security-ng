TARGET_DIR=/opt
APP_NAME=home-security
PYTHON_CMD=python3

#######################################################################

LOCAL_PORT=8383
SSL_SERVER_CERT=/opt/certificates/server_cert.pem
SSL_SERVER_CERT_KEY=/opt/certificates/server_key.pem
SSL_CLIENT_CA=/opt/certificates/ca_cert.pem

########################################################################

ROOT_DIR=$(TARGET_DIR)/$(APP_NAME)
SERVER_DIR=$(ROOT_DIR)/server
LOG_DIR=$(ROOT_DIR)/logs

#########################################################################

WORKSPACE_DIR=$(shell pwd)

SERVER_SOURCE_DIR=$(WORKSPACE_DIR)/server
CAMERA_SOURCE_DIR=$(WORKSPACE_DIR)/camera

########################################################################

SERVER_SOURCE_FILENAMES=$(shell cd $(SERVER_SOURCE_DIR)/src/ && ls *.py)
SERVER_TARGET_FILES=$(patsubst %, $(SERVER_DIR)/app/%, $(SERVER_SOURCE_FILENAMES))

CAMERA_SOURCES=$(wildcard $(CAMERA_SOURCE_DIR)/src/*.*)

#######################################################################

.PHONY: run install, prepare_dir, install_prerequisites, prepare_venv, clean reload reload_server stop start


run: $(SERVER_DIR)/lib/camera_handler.so $(SERVER_TARGET_FILES) $(ROOT_DIR)/nginx.conf $(ROOT_DIR)/uwsgi.ini $(ROOT_DIR)/start.sh $(ROOT_DIR)/stop.sh $(SERVER_DIR)/app/camera.py


$(SERVER_DIR)/lib/camera_handler.so: $(CAMERA_SOURCES)
	cd $(CAMERA_SOURCE_DIR); \
	make clean; \
	make; \
	cd build; \
	cp $(@F) $(@D); \
	cp $(CAMERA_SOURCE_DIR)/camera.py $(SERVER_DIR)/app

$(SERVER_DIR)/app/camera.py: $(CAMERA_SOURCE_DIR)/camera.py
	cp $^ $@

$(SERVER_DIR)/app/%.py: $(SERVER_SOURCE_DIR)/src/%.py
	cp $^ $@

$(ROOT_DIR)/nginx.conf: $(SERVER_SOURCE_DIR)/conf/nginx.conf_template
	mkdir -p $(@D)
	sed -e 's#{SSL_SERVER_CERT}#$(SSL_SERVER_CERT)#g' \
	    -e 's#{SSL_SERVER_KEY}#$(SSL_SERVER_CERT_KEY)#g' \
    	    -e 's#{SSL_CLIENT_CA}#$(SSL_CLIENT_CA)#g' \
	    -e 's#{LOCAL_PORT}#$(LOCAL_PORT)#g' \
	    -e 's#{LOG_DIR}#$(LOG_DIR)#g' \
	    $< > $@	    
	
$(ROOT_DIR)/uwsgi.ini: $(SERVER_SOURCE_DIR)/conf/uwsgi.ini_template
	mkdir -p $(@D)
	sed -e 's#{VENV_DIR}#$(SERVER_DIR)#g'\
	    -e 's#{MODULE_ROOT_DIR}#$(SERVER_DIR)/app#g' \
	    -e 's#{LOCAL_PORT}#$(LOCAL_PORT)#g' \
	    -e 's#{LOGFILE}#$(LOG_DIR)/main.log#g' \
	    -e 's#{CAMERA_LOGFILE}#$(LOG_DIR)/camera.log#g' \
	    -e 's#{CAMERA_LIB}#$(SERVER_DIR)/lib/camera_handler.so#g' \
	    $< > $@;

$(ROOT_DIR)/start.sh: $(SERVER_SOURCE_DIR)/conf/start.sh_template
	sed -e 's#{LOG_FILE}#$(LOG_DIR)/uwsgi.log#g' \
	    -e 's#{UWSGI_PID}#$(ROOT_DIR)/uwsgi.pid#g' \
	    -e 's#{UWSGI_INI}#$(ROOT_DIR)/uwsgi.ini#g' \
	    $< > $@;
	chmod u=rwx,go=rx $@

$(ROOT_DIR)/stop.sh: $(SERVER_SOURCE_DIR)/conf/stop.sh
	cp -f $< $@

#########################################################################

install: prepare_dir prepare_venv install_prerequisites run

prepare_dir:
	mkdir -p $(SERVER_DIR)/app
	mkdir -p $(LOG_DIR)


prepare_venv:
	$(PYTHON_CMD) -m venv $(SERVER_DIR)

install_prerequisites:
	cd $(SERVER_DIR)/bin; \
	. ./activate;  \
	cd ..; \
	python -m pip install -r $(SERVER_SOURCE_DIR)/requirements.txt; \
	deactivate;

###########################################################################

reload: run reload_server

reload_server: stop start

stop:
	cd $(ROOT_DIR) && ./stop.sh && sleep 3

start:
	cd $(ROOT_DIR) && ./start.sh

###########################################################################

clean:
	rm -rf $(ROOT_DIR)
