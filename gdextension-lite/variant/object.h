/** @file
 * object.h -- Godot Object type
 *
 * `Object` and the other class types are opaque, since they are always used through pointers.
 */
#ifndef __GDEXTENSION_LITE_OBJECT_H__
#define __GDEXTENSION_LITE_OBJECT_H__

#include "variant.h"
#include "../gdextension/gdextension_interface.h"
#include "../generated/extension_interface.h"
#include "../implementation-macros.h"

typedef struct godot_Object godot_Object;

#ifdef __cplusplus
extern "C" {
#endif

static inline godot_Variant godot_new_Variant_from_Object(const godot_Object *value) {
	GDEXTENSION_LITE_VARIANT_FROM_TYPE_IMPL(Object*, GDEXTENSION_VARIANT_TYPE_OBJECT, &value);
}

static inline godot_Object *godot_new_Object_from_Variant(const godot_Variant *value) {
	GDEXTENSION_LITE_TYPE_FROM_VARIANT_IMPL(Object*, GDEXTENSION_VARIANT_TYPE_OBJECT, value);
}

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_OBJECT_H__
