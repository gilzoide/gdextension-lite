#include "../gdextension-lite/gdextension-lite.h"

void initialize(void *userdata, GDExtensionInitializationLevel p_level) {
    if (p_level != GDEXTENSION_INITIALIZATION_SCENE) {
        return;
    }

	godot_String msg = godot_new_String_from_latin1_chars("Hello from GDExtension Lite!");
	godot_Variant msg_var = godot_Variant_from_String(&msg);
	godot_print_v(&msg_var);
	godot_destroy_Variant(&msg_var);
	godot_destroy_String(&msg);
}

void deinitialize(void *userdata, GDExtensionInitializationLevel p_level) {
    if (p_level != GDEXTENSION_INITIALIZATION_SCENE) {
        return;
    }
}

GDExtensionBool gdextension_entry(
    const GDExtensionInterfaceGetProcAddress p_get_proc_address,
    GDExtensionClassLibraryPtr p_library,
    GDExtensionInitialization *r_initialization
) {
	gdextension_lite_initialize(p_get_proc_address);
    r_initialization->initialize = &initialize;
    r_initialization->deinitialize = &deinitialize;
    return 1;
}
