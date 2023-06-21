#include "../gdextension-lite/gdextension-lite.h"

void initialize(void *userdata, GDExtensionInitializationLevel p_level) {
    if (p_level != GDEXTENSION_INITIALIZATION_SCENE) {
        return;
    }

	godot_String msg = godot_new_String_from_latin1_chars("Hello from GDExtension Lite!");
	godot_Variant msg_var = godot_Variant_from_String(&msg);
	godot_destroy_String(&msg);
	godot_prints_v(&msg_var, &msg_var, &msg_var);
	godot_destroy_Variant(&msg_var);
}

void deinitialize(void *userdata, GDExtensionInitializationLevel p_level) {
    if (p_level != GDEXTENSION_INITIALIZATION_SCENE) {
        return;
    }
}

GDExtensionBool gdextension_entry(
    const GDExtensionInterface *p_interface,
    GDExtensionClassLibraryPtr p_library,
    GDExtensionInitialization *r_initialization
) {
    r_initialization->initialize = &initialize;
    r_initialization->deinitialize = &deinitialize;
	gdextension_lite_initialize(p_interface);
    return 1;
}
