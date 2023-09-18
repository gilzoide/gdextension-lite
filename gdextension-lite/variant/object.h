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

extern GDExtensionTypeFromVariantConstructorFunc godot_ptr_Object_from_Variant;
godot_Object *godot_Object_from_Variant(godot_Variant *variant);
extern GDExtensionVariantFromTypeConstructorFunc godot_ptr_Variant_from_Object;
godot_Variant godot_Variant_from_Object(godot_Object **object);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_OBJECT_H__

#ifdef GDEXTENSION_LITE_IMPLEMENTATION
#ifndef __GDEXTENSION_LITE_OBJECT_H_IMPLEMENTATION__
#define __GDEXTENSION_LITE_OBJECT_H_IMPLEMENTATION__

#ifdef __cplusplus
extern "C" {
#endif

GDExtensionTypeFromVariantConstructorFunc godot_ptr_Object_from_Variant;
godot_Object *godot_Object_from_Variant(godot_Variant *value) {
	godot_Object *self;
	godot_ptr_Object_from_Variant(&self, value);
	return self;
}
GDExtensionVariantFromTypeConstructorFunc godot_ptr_Variant_from_Object;
godot_Variant godot_Variant_from_Object(godot_Object **value) {
	godot_Variant self;
	godot_ptr_Variant_from_Object(&self, value);
	return self;
}

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_OBJECT_H_IMPLEMENTATION__
#endif  // GDEXTENSION_LITE_IMPLEMENTATION
