GODOT_BIN ?= godot

refresh-gdextension-api:
	cd gdextension && $(GODOT_BIN) --headless --dump-gdextension-interface --dump-extension-api
