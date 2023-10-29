#include "../gdextension-lite/gdextension-lite.h"

void initialize(void *userdata, GDExtensionInitializationLevel p_level) {
	if (p_level != GDEXTENSION_INITIALIZATION_SCENE) {
		return;
	}

	// print("Hello from GDExtension Lite!")
	{
		GDCLEANUP(godot_String) msg = godot_String_new_with_latin1_chars("Hello from GDExtension Lite!");
		GDCLEANUP(godot_Variant) msg_var = godot_Variant_new_with_String(&msg);

		godot_print(&msg_var, NULL, 0);
	}

	// prints("OS.get_name() ==", OS.get_name(), OS)
	{
		GDCLEANUP(godot_StringName) singleton_name = godot_StringName_new_with_latin1_chars("OS");
		godot_OS *os = (godot_OS *) godot_global_get_singleton(&singleton_name);
		GDCLEANUP(godot_Variant) os_var = godot_Variant_new((godot_Object *)os);
		
		GDCLEANUP(godot_String) os_name = godot_OS_get_name(os);
		GDCLEANUP(godot_Variant) os_name_var = godot_Variant_new_with_String(&os_name);

		GDCLEANUP(godot_String) msg = godot_String_new_with_latin1_chars("OS.get_name() ==");
		GDCLEANUP(godot_Variant) msg_var = godot_Variant_new_with_String(&msg);

		const godot_Variant *args[] = { &os_name_var, &os_var };
		godot_prints(&msg_var, args, 2);
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

