#include "variant.h"

#include "../implementation-macros.h"
#include "../generated/extension_interface.h"

#ifdef __cplusplus
extern "C" {
#endif

godot_Variant godot_Variant_new_nil() {
	godot_Variant self;
	godot_variant_new_nil(&self);
	return self;
}

godot_Variant godot_Variant_new_with_Variant(const godot_Variant *other) {
	godot_Variant self;
	godot_variant_new_copy(&self, other);
	return self;
}

void godot_Variant_destroy(godot_Variant *self) {
	godot_variant_destroy(self);
}

#ifdef __cplusplus
}
#endif
