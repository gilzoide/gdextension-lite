#include "variant.h"

#include "../implementation-macros.h"
#include "../generated/extension_interface.h"

#ifdef __cplusplus
extern "C" {
#endif

void godot_placement_new_Variant(godot_Variant *self) {
	godot_variant_new_nil(self);
}

godot_Variant godot_new_Variant() {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_Variant, godot_placement_new_Variant);
}

void godot_placement_new_Variant_from_Variant(godot_Variant *self, const godot_Variant *other) {
	godot_variant_new_copy(self, other);
}

godot_Variant godot_new_Variant_from_Variant(const godot_Variant *other) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_Variant, godot_placement_new_Variant_from_Variant, other);
}

void godot_destroy_Variant(godot_Variant *self) {
	godot_variant_destroy(self);
}

#ifdef __cplusplus
}
#endif
