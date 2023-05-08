GODOT_BIN ?= godot
PYTHON_BIN ?= python
PYCODESTYLE_BIN ?= pycodestyle

# Python / code generator targets
refresh-gdextension-api:
	cd gdextension && $(GODOT_BIN) --headless --dump-gdextension-interface --dump-extension-api

generate-bindings:
	$(PYTHON_BIN) binding_generator/main.py gdextension/extension_api.json include/generated

python-check-codestyle:
	$(PYCODESTYLE_BIN) binding_generator
