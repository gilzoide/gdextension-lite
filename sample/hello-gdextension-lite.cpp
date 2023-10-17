#include "../gdextension-lite/gdextension-lite.hpp"

using namespace godot;

void initialize(void *userdata, GDExtensionInitializationLevel p_level) {
	if (p_level != GDEXTENSION_INITIALIZATION_SCENE) {
		return;
	}

	// print("Hello from GDExtension Lite!")
	{
		godot_String msg = godot_new_String_from_latin1_chars("Hello from GDExtension Lite!");
		godot_Variant msg_var = godot_new_Variant_from_String(&msg);
		godot_destroy_String(&msg);

		godot_print(&msg_var, 0, NULL);
		godot_destroy_Variant(&msg_var);
	}

	// prints("OS.get_name() ==", OS.get_name())
	{
		godot_StringName singleton_name = godot_new_StringName_from_latin1_chars("OS");
		godot_OS *os = (godot_OS *) godot_global_get_singleton(&singleton_name);
		godot_destroy_StringName(&singleton_name);
		
		godot_String os_name = godot_OS_get_name(os);
		godot_Variant os_name_var = godot_new_Variant_from_String(&os_name);
		godot_destroy_String(&os_name);

		godot_String msg = godot_new_String_from_latin1_chars("OS.get_name() ==");
		godot_Variant msg_var = godot_new_Variant_from_String(&msg);
		godot_destroy_String(&msg);

		const godot_Variant *args[1] = { &os_name_var };
		godot_prints(&msg_var, 1, args);
		godot_destroy_Variant(&msg_var);
		godot_destroy_Variant(&os_name_var);
	}
}

void deinitialize(void *userdata, GDExtensionInitializationLevel p_level) {}

extern "C" GDExtensionBool gdextension_entry(
	const GDExtensionInterfaceGetProcAddress p_get_proc_address,
	GDExtensionClassLibraryPtr p_library,
	GDExtensionInitialization *r_initialization
) {
	gdextension_lite_initialize(p_get_proc_address);
	r_initialization->initialize = &initialize;
	r_initialization->deinitialize = &deinitialize;
	return 1;
}

