# GDExtension Lite
Automatically generated GDExtension bindings for C/C++

This is not meant to be a replacement for the [godot-cpp](https://github.com/godotengine/godot-cpp) project,
but rather an alternative for those who want the full API matching `extension_api.json` in a C-compatible interface,
for example for creating bindings for other programming languages.


## Features
- Easily embeddable in any project: include [gdextension-lite.h](gdextension-lite/gdextension-lite.h), compile and link [gdextension-lite-one.c](gdextension-lite/gdextension-lite-one.c) and you're good to go
- Automatically generated from `extension_api.json` file, so new Godot APIs are added in a matter of regenerating the bindings
- Bindings for all Godot classes, variant types, methods, operators, utility functions, enums, GDExtension interface functions
- Extra constructors with C strings for `String`, `StringName`, `NodePath`, `Color`, `godot_int` and `godot_float`
- `GDCLEANUP` macro for declaring variables with automatic cleanup in C (compiler needs to support `__attribute__((cleanup(...)))`, like GCC and clang)
- Supports Godot 4.1+
- Faster compilation time than godot-cpp project


## How to use
1. Generate the bindings files (needs Python 3.10+):
   ```sh
   make generate-bindings
   ```
2. Implement your extension in C/C++:
   ```c
   // @file my-extension.c
   
   // 1. Include gdextension-lite.h: the whole API is accessible through it
   #include <gdextension-lite/gdextension-lite.h>
   
   void initialize(void *userdata, GDExtensionInitializationLevel p_level);
   void deinitialize(void *userdata, GDExtensionInitializationLevel p_level);
   
   // 2. In your GDExtension entrypoint, call `gdextension_lite_initialize`
   GDExtensionBool gdextension_entry(
       GDExtensionInterfaceGetProcAddress p_get_proc_address,
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
   
       // print("Hello from GDExtension Lite!")
       {
           godot_String msg = godot_new_String_with_latin1_chars("Hello from GDExtension Lite!");
           godot_Variant msg_var = godot_new_Variant_with_String(&msg);
           godot_print(&msg_var, NULL, 0);
           // As always in C, you are responsible for freeing objects
           godot_Variant_destroy(&msg_var);
           godot_String_destroy(&msg);
       }
   
       // prints("OS.get_name() ==", OS.get_name())
       {
           // Use "GDCLEANUP(godot_TYPE)" for automatic variable cleanup at the end of scope
           // (compiler needs to support `__attribute__((cleanup(...)))`, like GCC and clang)
           GDCLEANUP(godot_String) msg = godot_new_String_with_latin1_chars("OS.get_name() ==");
           GDCLEANUP(godot_Variant) msg_var = godot_new_Variant_with_String(&msg);
   
           // Objects are always used via pointers, no need for cleanup
           // You may need to reference/unreference RefCounted instances, though
           godot_OS *os = godot_OS_singleton();
   
           GDCLEANUP(godot_String) os_name = godot_OS_get_name(os);
           GDCLEANUP(godot_Variant) os_name_var = godot_new_Variant_with_String(&os_name);
   
           const godot_Variant *args[] = { &os_name_var };
           godot_prints(&msg_var, args, 1);
       }
   
       // var node = Node()
       // print(node)
       // node.free()
       {
           godot_Node *node = godot_new_Node();
           GDCLEANUP(godot_String) node_name = godot_Object_to_string((godot_Object *) node);
           GDCLEANUP(godot_Variant) node_name_var = godot_new_Variant_with_String(&node_name);
           godot_print(&node_name_var, NULL, 0);
           godot_object_destroy(node);
       }
   }
   
   void deinitialize(void *userdata, GDExtensionInitializationLevel p_level) {
       // no-op
   }
   ```
3. Now compile `gdextension-lite-one.c` and link it to your own code.
   Example SConstruct:
   ```python
   SharedLibrary(
       [
         'my-extension.c',
         'path-to-gdextension-lite/gdextension-lite/gdextension-lite-one.c',
       ],
       CFLAGS=["-O2", "-flto"],
   )
   ```
   We recommend compiling `gdextension-lite-one.c` with `-O2 -flto` flags to avoid linking all Godot functions, but rather link only the ones you actually use.

Sample code is also available at the [sample](sample) folder.


## Naming conventions
1. Every type and function binding from Godot have the prefix `godot_`
2. Every GDExtension Lite function have the prefix `gdextension_lite_`
3. Constructors have the format `godot_new_<type name>` or `godot_new_<type name>_with_<arg1 type>_<arg2 type>...`
4. Destructors have the format `godot_<type name>_destroy`
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
15. Variadic methods and utility functions expect argv/argc parameters
16. Singleton getters have the format `godot_<type name>_singleton`


## Generating bindings
1. Update the `extension_api.json` and `gdextension_interface.h` files (depends on Godot 4 executable):
   ```sh
   make refresh-gdextension-api
   ```
2. Generate the bindings files (depends on Python 3.10+):
   ```sh
   make generate-bindings
   ```
3. Generate the distribution `build/gdextension-lite.zip` file with all headers:
   ```sh
   make dist
   ```
