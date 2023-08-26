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

extern GDExtensionTypeFromVariantConstructorFunc godot_ptr_Object_from_Variant;
godot_Object *godot_Object_from_Variant(godot_Variant *variant);
extern GDExtensionVariantFromTypeConstructorFunc godot_ptr_Variant_from_Object;
godot_Variant godot_Variant_from_Object(godot_Object **object);

#endif

#ifdef GDEXTENSION_LITE_IMPLEMENTATION
#ifndef __GDEXTENSION_LITE_OBJECT_H_IMPLEMENTATION__
#define __GDEXTENSION_LITE_OBJECT_H_IMPLEMENTATION__

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

#endif  // __GDEXTENSION_LITE_OBJECT_H_IMPLEMENTATION__
#endif  // GDEXTENSION_LITE_IMPLEMENTATION
