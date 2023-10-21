/** @file
 * object.h -- Godot Object type
 *
 * `Object` and the other class types are opaque, since they are always used through pointers.
 */
#ifndef __GDEXTENSION_LITE_OBJECT_H__
#define __GDEXTENSION_LITE_OBJECT_H__

#include "variant.h"

typedef struct godot_Object godot_Object;

#ifdef __cplusplus
extern "C" {
#endif

godot_Variant godot_new_Variant_from_Object(const godot_Object *value);
godot_Object *godot_new_Object_from_Variant(const godot_Variant *value);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_OBJECT_H__
