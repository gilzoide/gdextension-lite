// 1. Include gdextension-lite.h: the whole API is accessible through it
#include <gdextension-lite/gdextension-lite.h>

void initialize(void *userdata, GDExtensionInitializationLevel p_level);
void deinitialize(void *userdata, GDExtensionInitializationLevel p_level);

GDExtensionBool gdextension_entry(
	const GDExtensionInterfaceGetProcAddress p_get_proc_address,
	GDExtensionClassLibraryPtr p_library,
	GDExtensionInitialization *r_initialization
) {
	// 2. In your GDExtension entrypoint, call `gdextension_lite_initialize`
	gdextension_lite_initialize(p_get_proc_address);
	// setup initialize/deinitialize as usual
	r_initialization->initialize = &initialize;
	r_initialization->deinitialize = &deinitialize;
	// return success as usual
	return 1;
}

// 3. Use the bindings freely
void initialize(void *userdata, GDExtensionInitializationLevel p_level) {
	if (p_level != GDEXTENSION_INITIALIZATION_SCENE) {
		return;
	}

	// print("Hello from GDExtension Lite!")
	{
		godot_String msg = godot_String_new_with_latin1_chars("Hello from GDExtension Lite!");
		godot_Variant msg_var = godot_Variant_new_with_String(&msg);
		godot_print(&msg_var, NULL, 0);
		// As always in C, you are responsible for freeing objects
		godot_Variant_destroy(&msg_var);
		godot_String_destroy(&msg);
	}

	// prints("OS.get_name() ==", OS.get_name())
	{
		// If compiling with GCC/clang, use "GDCLEANUP(godot_TYPE)" for
		// automatic variable cleanup at the end of scope
		// (uses `__attribute__((cleanup(...)))`)
		GDCLEANUP(godot_StringName) singleton_name = godot_StringName_new_with_latin1_chars("OS");

		// Objects are always used via pointers, no need for cleanup
		// You may need to reference/unreference RefCounted instances, though
		godot_OS *os = (godot_OS *) godot_global_get_singleton(&singleton_name);
		
		GDCLEANUP(godot_String) os_name = godot_OS_get_name(os);
		GDCLEANUP(godot_Variant) os_name_var = godot_Variant_new_with_String(&os_name);

		GDCLEANUP(godot_String) msg = godot_String_new_with_latin1_chars("OS.get_name() ==");
		GDCLEANUP(godot_Variant) msg_var = godot_Variant_new_with_String(&msg);

		const godot_Variant *args[] = { &os_name_var };
		godot_prints(&msg_var, args, 1);
	}
}

void deinitialize(void *userdata, GDExtensionInitializationLevel p_level) {
	// no-op
}
