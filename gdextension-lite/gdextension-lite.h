/** @file
 * gdextension-lite.h -- GDExtension Lite entrypoint, includes every other file
 */
#ifndef __GDEXTENSION_LITE_H__
#define __GDEXTENSION_LITE_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "generated/extension_interface.h"
#include "generated/global_enums.h"
#include "generated/utility_functions.h"
#include "generated/class-stubs/all.h"
#include "generated/class-methods/all.h"
#include "generated/variant/all.h"
#include "variant/all.h"

void gdextension_lite_initialize(const GDExtensionInterfaceGetProcAddress get_proc_address);

#ifdef __cplusplus
}
#endif

#endif

#ifdef GDEXTENSION_LITE_IMPLEMENTATION
#ifndef __GDEXTENSION_LITE_H_IMPLEMENTATION__
#define __GDEXTENSION_LITE_H_IMPLEMENTATION__

#ifdef __cplusplus
extern "C" {
#endif

void gdextension_lite_initialize(const GDExtensionInterfaceGetProcAddress get_proc_address) {
	gdextension_lite_initialize_interface(get_proc_address);
	godot_ptr_Object_from_Variant = godot_get_variant_to_type_constructor(GDEXTENSION_VARIANT_TYPE_OBJECT);
	godot_ptr_Variant_from_Object = godot_get_variant_from_type_constructor(GDEXTENSION_VARIANT_TYPE_OBJECT);
}

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_H_IMPLEMENTATION__
#endif  // GDEXTENSION_LITE_IMPLEMENTATION

