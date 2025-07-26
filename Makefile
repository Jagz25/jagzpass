# Makefile for JagzPass — build, bundle, and launch

PYTHON := python3
VENV := venv
ENTRY := main.py
DIST := dist
APP := jagzpass

.PHONY: help setup run build clean distclean

help:
	@echo "Usage:"
	@echo "  make setup       Set up virtual environment and install dependencies"
	@echo "  make run         Run the JagzPass CLI via Python"
	@echo "  make build       Clean + build executable + run it (Linux)"
	@echo "  make clean       Remove temp and cache files"
	@echo "  make distclean   Remove everything including dist/ and venv/"

setup:
	@$(PYTHON) -m venv $(VENV)
	@. $(VENV)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "✅ Virtual environment and dependencies installed."

run:
	@. $(VENV)/bin/activate && $(PYTHON) $(ENTRY)

build:
	@echo "🧨 Cleaning previous build artifacts..."
	@rm -rf build/ dist/ __pycache__ ./*.spec
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@. $(VENV)/bin/activate && pip install pyinstaller > /dev/null
	@echo "🚧 Building executable..."
	@pyinstaller --onefile --name $(APP) \
		--add-data "PasswordGenerator/100k-most-used-passwords-NCSC.txt:PasswordGenerator" \
		--add-data "Vaults:Vaults" \
		$(ENTRY)
	@echo "✅ Build complete. Launching..."
	@./dist/$(APP)

clean:
	@rm -rf build/ __pycache__ ./*.spec
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "🧹 Cleaned temp files."

distclean: clean
	@rm -rf $(VENV) $(DIST)
	@echo "🧹 Fully wiped venv and dist."
