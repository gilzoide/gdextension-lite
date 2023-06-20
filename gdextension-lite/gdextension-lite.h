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

void gdextension_lite_initialize(const GDExtensionInterface *interface);

#endif

#ifdef GDEXTENSION_LITE_IMPLEMENTATION
#ifndef __GDEXTENSION_LITE_H_IMPLEMENTATION__
#define __GDEXTENSION_LITE_H_IMPLEMENTATION__

void gdextension_lite_initialize(const GDExtensionInterface *interface) {
	godot_interface = interface;
	godot_ptr_destroy_String = interface->variant_get_ptr_destructor(GDEXTENSION_VARIANT_TYPE_STRING);
	gdextension_lite_initialize_StringName(interface);
	gdextension_lite_initialize_generated(interface);
	gdextension_lite_initialize_utility_functions(interface);
}

#endif  // __GDEXTENSION_LITE_H_IMPLEMENTATION__
#endif  // GDEXTENSION_LITE_IMPLEMENTATION

