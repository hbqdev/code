PYINSTALLER=pyinstaller --onefile -c --distpath . --workpath=/tmp --log-level=WARN

update_scanops:
	$(PYINSTALLER) update_scanops.py

live_log:
	$(PYINSTALLER) live_log.py

start:
	$(PYINSTALLER) start.py

clean:
	rm -f update_scanops live_log start
