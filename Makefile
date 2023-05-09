# Options
GODOT_BIN ?= godot
PYTHON_BIN ?= python
PYCODESTYLE_BIN ?= pycodestyle

# Constants
GDEXTENSION_DIR = include/gdextension
GENERATED_HEADER_DIR = include/gdextension-lite/generated

# Python / code generator targets
refresh-gdextension-api:
	@mkdir -p $(GDEXTENSION_DIR)
	cd $(GDEXTENSION_DIR) && $(GODOT_BIN) --headless --dump-gdextension-interface --dump-extension-api

generate-bindings:
	$(PYTHON_BIN) binding_generator/main.py $(GDEXTENSION_DIR)/extension_api.json $(GENERATED_HEADER_DIR)

python-check-codestyle:
	$(PYCODESTYLE_BIN) binding_generator
