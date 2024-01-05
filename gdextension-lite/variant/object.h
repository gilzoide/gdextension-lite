/** @file
 * object.h -- Godot Object type
 *
 * `Object` and the other class types are opaque, since they are always used through pointers.
 */
#ifndef __GDEXTENSION_LITE_OBJECT_H__
#define __GDEXTENSION_LITE_OBJECT_H__

#include "variant.h"
#include "../definition-macros.h"

GDEXTENSION_LITE_OPAQUE_STRUCT(godot_Object);

#ifdef __cplusplus
extern "C" {
#endif

GDEXTENSION_LITE_DECL godot_Variant godot_new_Variant_with_Object(const godot_Object *value);
GDEXTENSION_LITE_DECL godot_Object *godot_new_Object_with_Variant(const godot_Variant *value);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_OBJECT_H__
