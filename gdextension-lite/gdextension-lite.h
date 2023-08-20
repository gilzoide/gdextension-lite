/** @file
 * gdextension-lite.h -- GDExtension Lite entrypoint, includes every other file
 */
#ifndef __GDEXTENSION_LITE_H__
#define __GDEXTENSION_LITE_H__

#include "gdextension-interface.h"
#include "generated/global_enums.h"
#include "generated/utility_functions.h"
#include "generated/variant/all.h"
#include "variant/all.h"

void gdextension_lite_initialize(const GDExtensionInterfaceGetProcAddress get_proc_address);

#endif

#ifdef GDEXTENSION_LITE_IMPLEMENTATION
#ifndef __GDEXTENSION_LITE_H_IMPLEMENTATION__
#define __GDEXTENSION_LITE_H_IMPLEMENTATION__

void gdextension_lite_initialize(const GDExtensionInterfaceGetProcAddress get_proc_address) {
	gdextension_lite_initialize_interface(get_proc_address);
	godot_ptr_destroy_String = godot_variant_get_ptr_destructor(GDEXTENSION_VARIANT_TYPE_STRING);
	gdextension_lite_initialize_StringName();
	gdextension_lite_initialize_generated();
	gdextension_lite_initialize_utility_functions();
}

#endif  // __GDEXTENSION_LITE_H_IMPLEMENTATION__
#endif  // GDEXTENSION_LITE_IMPLEMENTATION

