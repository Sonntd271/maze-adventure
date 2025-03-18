SHELL := /bin/sh

.PHONY: all run setup update upgrade

all: run

OS := $(shell uname)

run:
	@echo "Detected $(OS)"
	@python$(if $(filter $(OS),MINGW64_NT-%,CYGWIN%,MSYS%),,3) src/main.py

setup:
	@if [ -d "venv" ]; then \
		echo "Virtual environment already exists."; \
	else \
		echo "Virtual environment not found. Creating one..."; \
		echo "Detected $(OS)."; \
		python$(if $(filter $(OS),MINGW64_NT-%,CYGWIN%,MSYS%),,3) -m venv venv; \
		echo "Virtual environment created successfully."; \
	fi
	@venv/bin/pip install -r requirements.txt

update:
	@venv/bin/pip freeze > requirements.txt

upgrade:
	@if [ -f "venv/bin/activate" ]; then \
		. venv/bin/activate && pip install --upgrade -r requirements.txt; \
	else \
		. venv/Scripts/activate && pip install --upgrade -r requirements.txt; \
	fi
