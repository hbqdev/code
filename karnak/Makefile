ENVIRONMENT=PYTHONPATH=`pwd`
PROTO_DIR=proto
HOSTNAME=`hostname`

all_protos:
	protoc -I=${PROTO_DIR} --python_out=model ${PROTO_DIR}/*.proto

proto: all_protos

auth_server: proto
	${ENVIRONMENT} python ui/auth_server.py config/auth_server.yaml

checkin: proto
	${ENVIRONMENT} python ui/checkin_desk_server.py config/checkin_desk.yaml

fakecheckin: proto
	${ENVIRONMENT} python ui/checkin_desk_server.py config/fake_checkin_desk.yaml

webserver: proto
	${ENVIRONMENT} python ui/server.py config/${HOSTNAME}.yaml

websocket: proto
	${ENVIRONMENT} python ui/websocket.py config/${HOSTNAME}.yaml

elphel: proto
	${ENVIRONMENT} python ui/websocket.py config/station.yaml

fakeserver: proto
	${ENVIRONMENT} python ui/websocket.py config/fake_station.yaml

browser: proto
	${ENVIRONMENT} python ui/browser.py

sanity:
	-killall camera_server
	perl util/cameraprobe.pl config/${HOSTNAME}.yaml static/camera_info.html
	python util/configure_camera_server.py config/${HOSTNAME}.yaml

empty:
	rm -rf static/calibration/empty-[123]0*
	curl -d capture_type=empty http://localhost:8080/config/scanners/scan2d/start

ortho-empty:
	rm -rf static/calibration/empty-40*
	curl -d capture_type=empty http://localhost:8080/config/scanners/ortho_table/start

calibration:
	rm -f static/calibration/*
	curl -d capture_type=calibration http://localhost:8080/config/scanners/scan2d/start

ortho-calibration:
	rm -f static/calibration/40*
	curl -d capture_type=calibration http://localhost:8080/config/scanners/ortho_table/start

daily:
	rm -rf static/daily/*
	curl -X POST http://localhost:8080/config/resources/scan2d/daily

ortho-daily:
	rm -rf static/daily/40*
	curl -d capture_type=daily http://localhost:8080/config/scanners/ortho_table/start

swivel:
	curl -d capture_type=swivel http://localhost:8080/config/scanners/scan2d/start

cancel:
	curl -d cancel=true http://localhost:8080/config/scanners/scan2d/stop

sync:
	rsync -v -v ./static/capture rsync://persephone/scan

localui:
	gsutil/gsutil cp -r gs://katamari-2d-serve/scanshop static

captainslog:
	perl util/captainslog.pl

clean:
	find . | egrep pyc$$ | xargs rm -f
	find . | egrep ~$$ | xargs rm -f
	rm -f model/*pb2.py
	rm -f static/logs/*

test: proto
	${ENVIRONMENT} nosetests tests --with-coverage --cover-package=resources,upload,scanner,ui

