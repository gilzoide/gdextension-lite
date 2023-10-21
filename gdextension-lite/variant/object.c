#include "object.h"
#include "../generated/extension_interface.h"
#include "../implementation-macros.h"

typedef struct godot_Object godot_Object;

#ifdef __cplusplus
extern "C" {
#endif

godot_Variant godot_new_Variant_from_Object(const godot_Object *value) {
	GDEXTENSION_LITE_VARIANT_FROM_TYPE_IMPL(Object*, GDEXTENSION_VARIANT_TYPE_OBJECT, &value);
}

godot_Object *godot_new_Object_from_Variant(const godot_Variant *value) {
	GDEXTENSION_LITE_TYPE_FROM_VARIANT_IMPL(Object*, GDEXTENSION_VARIANT_TYPE_OBJECT, value);
}

#ifdef __cplusplus
}
#endif
