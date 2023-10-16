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

godot_Variant godot_new_Variant_from_Object(godot_Object **object);
godot_Object *godot_new_Object_from_Variant(godot_Variant *variant);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_OBJECT_H__

#ifdef GDEXTENSION_LITE_IMPLEMENTATION
#ifndef __GDEXTENSION_LITE_OBJECT_H_IMPLEMENTATION__
#define __GDEXTENSION_LITE_OBJECT_H_IMPLEMENTATION__

#include "../implementation-macros.h"

#ifdef __cplusplus
extern "C" {
#endif

static GDExtensionTypeFromVariantConstructorFunc godot_ptr_new_Object_from_Variant;
godot_Object *godot_Object_from_Variant(godot_Variant *value) {
	GDEXTENSION_LITE_LAZY_INIT_TYPE_FROM_VARIANT(Object, GDEXTENSION_VARIANT_TYPE_OBJECT);
	godot_Object *self;
	godot_ptr_new_Object_from_Variant(&self, value);
	return self;
}
static GDExtensionVariantFromTypeConstructorFunc godot_ptr_new_Variant_from_Object;
godot_Variant godot_new_Variant_from_Object(godot_Object **value) {
	GDEXTENSION_LITE_LAZY_INIT_VARIANT_FROM_TYPE(Object, GDEXTENSION_VARIANT_TYPE_OBJECT);
	godot_Variant self;
	godot_ptr_new_Variant_from_Object(&self, value);
	return self;
}

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_OBJECT_H_IMPLEMENTATION__
#endif  // GDEXTENSION_LITE_IMPLEMENTATION
