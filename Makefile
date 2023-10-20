# Options
GODOT_BIN ?= godot
PYTHON_BIN ?= python
PYCODESTYLE_BIN ?= pycodestyle
SCONS_BIN ?= scons

# Constants
GDEXTENSION_DIR = gdextension-lite/gdextension
GENERATED_HEADER_DIR = gdextension-lite/generated
GENERATED_FOLDERS = build $(GENERATED_HEADER_DIR)

$(GENERATED_FOLDERS):
	@mkdir -p $@

# Python / code generator targets
refresh-gdextension-api:
	@mkdir -p $(GDEXTENSION_DIR)
	cd $(GDEXTENSION_DIR) && $(GODOT_BIN) --headless --dump-gdextension-interface --dump-extension-api

$(GENERATED_HEADER_DIR)/%.h: $(wildcard binding_generator/*.py binding_generator/**/*.py) | $(GENERATED_HEADER_DIR)
	$(PYTHON_BIN) binding_generator/main.py $(GDEXTENSION_DIR)/extension_api.json $(GENERATED_HEADER_DIR)
generate-bindings: $(GENERATED_HEADER_DIR)/global_enums.h

python-check-codestyle:
	$(PYCODESTYLE_BIN) binding_generator

# Distribution
build/gdextension-lite.zip: generate-bindings | build
	zip $@ $(shell find . -type f -name '*.h' -or -name '*.hpp')
dist: build/gdextension-lite.zip

# Sample
sample/.godot:
	$(GODOT_BIN) --headless --quit --editor --path sample || true

sample: generate-bindings
	$(SCONS_BIN) -C sample

run-sample: sample/.godot
	$(GODOT_BIN) --headless --quit --path sample --script test_entrypoint.gd

# Miscelaneous
clean:
	$(RM) -r $(GENERATED_FOLDERS)

.PHONY: clean sample run-sample
