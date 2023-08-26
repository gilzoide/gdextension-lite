# GDExtension Lite
Automatically generated header-only GDExtension bindings for C/C++


## Features
- Header-only, easily embeddable in any project
- Automatically generated from `extension_api.json` file, so new Godot APIs are easily added
- Bindings for all Godot classes, variant types, methods, operators, utility functions, enums, GDExtension interface functions
- Compatible with C99 and above, as well as C++
- Fast compilation times (much faster than godot-cpp project)


## How to use
First, create a C file for compiling the GDExtension Lite implementation.
This must be done in **exactly** one C/C++ file across your project.
```c
// @file gdextension-lite-implementation.c
#define GDEXTENSION_LITE_IMPLEMENTATION
#include <gdextension-lite/gdextension-lite.h>
```

Now, for the extension implementation:
```c
// 1. Include gdextension-lite.h: the whole API is accessible through it
#include <gdextension-lite/gdextension-lite.h>

void initialize(void *userdata, GDExtensionInitializationLevel p_level);
void deinitialize(void *userdata, GDExtensionInitializationLevel p_level);

// 2. In your GDExtension entrypoint, call `gdextension_lite_initialize`
GDExtensionBool gdextension_entry(
    const GDExtensionInterfaceGetProcAddress p_get_proc_address,
    GDExtensionClassLibraryPtr p_library,
    GDExtensionInitialization *r_initialization
) {
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

	godot_String msg = godot_new_String_from_latin1_chars("Hello from GDExtension Lite!");
	godot_Variant msg_var = godot_Variant_from_String(&msg);
  // godot_print_v is the variadic version of godot_print
  // This avoids having to pass argc/argv parameters manually
	godot_print_v(&msg_var);
  // As always in C, you are responsible for freeing objects
	godot_destroy_Variant(&msg_var);
	godot_destroy_String(&msg);
}

void deinitialize(void *userdata, GDExtensionInitializationLevel p_level) {
   // no-op
}
```

Sample code is also available at the [sample](sample) folder.


## Naming conventions
1. Every type and function binding from Godot have the prefix `godot_`
2. Every GDExtension Lite function have the prefix `gdextension_lite_`
3. Constructors have the format `godot_new_<type name>` or `godot_new_<type name>_from_<arg1 type>_<arg2 type>...`
4. Destructors have the format `godot_destroy_<type name>`
5. Member getters have the format `godot_<type name>_get_<member name>`
6. Member setters have the format `godot_<type name>_set_<member name>`
7. Indexed getters have the format `godot_<type name>_indexed_get`
8. Indexed setters have the format `godot_<type name>_indexed_set`
9. Keyed getters have the format `godot_<type name>_keyed_get`
10. Keyed setters have the format `godot_<type name>_keyed_set`
11. Operators have the format `godot_<type name>_op_<operator name>` for unary operators and `godot_<type name>_op_<operator name>_<right-hand side type>` for binary operators
12. Methods have the format `godot_<type name>_<method name>`
13. Enumerators defined by classes have the format `godot_<type name>_<enum name>`
14. Godot utility functions have the format `godot_<function name>`
15. Variadic methods and utility functions expect argc/argv parameters.
    Variadic macros with the format `godot_<function name>_v` are declared so that C developers can call them more easily.


## Generating bindings
1. Update the `extension_api.json` and `gdextension_interface.h` files (depends on Make, Python 3.10+):
   ```sh
   make refresh-gdextension-api
   ```
2. Generate the bindings files:
   ```sh
   make generate-bindings
   ```
3. Generate the distribution `build/gdextension-lite.zip` file with all headers:
   ```sh
   make dist
   ```
