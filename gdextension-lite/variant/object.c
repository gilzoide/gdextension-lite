#include "object.h"

#include "../implementation-macros.h"
#include "../generated/extension_interface.h"

#ifdef __cplusplus
extern "C" {
#endif

static GDExtensionVariantFromTypeConstructorFunc godot_ptr_new_Variant_from_Object;
void godot_placement_new_Variant_from_Object(godot_Variant *self, godot_Object **value) {
	GDEXTENSION_LITE_LAZY_INIT_VARIANT_FROM_TYPE(Object, GDEXTENSION_VARIANT_TYPE_OBJECT);
	godot_ptr_new_Variant_from_Object(self, value);
}

godot_Variant godot_new_Variant_from_Object(godot_Object **object) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_Variant, godot_placement_new_Variant_from_Object, object);
}

static GDExtensionTypeFromVariantConstructorFunc godot_ptr_new_Object_from_Variant;
void godot_placement_new_Object_from_Variant(godot_Object **self, godot_Variant *value) {
	GDEXTENSION_LITE_LAZY_INIT_TYPE_FROM_VARIANT(Object, GDEXTENSION_VARIANT_TYPE_OBJECT);
	godot_ptr_new_Object_from_Variant(self, value);
}

godot_Object *godot_new_Object_from_Variant(godot_Variant *variant) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_Object *, godot_placement_new_Object_from_Variant, variant);
}

#ifdef __cplusplus
}
#endif
