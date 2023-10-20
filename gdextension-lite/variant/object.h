/** @file
 * object.h -- Godot Object type
 *
 * `Object` and the other class types are opaque, since they are always used through pointers.
 */
#ifndef __GDEXTENSION_LITE_OBJECT_H__
#define __GDEXTENSION_LITE_OBJECT_H__

#include "variant.h"
#include "../gdextension/gdextension_interface.h"

typedef struct godot_Object godot_Object;

#ifdef __cplusplus
extern "C" {
#endif

void godot_placement_new_Variant_from_Object(godot_Variant *self, const godot_Object *object);
godot_Variant godot_new_Variant_from_Object(const godot_Object *object);

void godot_placement_new_Object_from_Variant(godot_Object ** self, const godot_Variant *variant);
godot_Object *godot_new_Object_from_Variant(const godot_Variant *variant);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_OBJECT_H__
