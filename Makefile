SHELL = /bin/bash
VENV = venv

.PHONY: all run venv clean
all: clean run

venv/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	source $@ && pip install -r $<
	touch $@

venv: venv/bin/activate

run: venv/bin/activate
	source $< && source .env && python get_weather.py

clean:
	rm -rf $(VENV)
	find . | grep __pycache__ | xargs rm -rf
