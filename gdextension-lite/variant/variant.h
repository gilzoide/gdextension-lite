/** @file
 * variant.h -- Godot Variant type
 */
#ifndef __GDEXTENSION_LITE_VARIANT_H__
#define __GDEXTENSION_LITE_VARIANT_H__

#include <stdint.h>

#ifdef REAL_T_IS_DOUBLE
	#define GODOT_VARIANT_SIZE 40
#else
	#define GODOT_VARIANT_SIZE 24
#endif

typedef struct godot_Variant {
	uint8_t _[GODOT_VARIANT_SIZE];
} godot_Variant;

// Constructors
void godot_placement_new_Variant(godot_Variant *self);
godot_Variant godot_new_Variant();
void godot_placement_new_Variant_from_Variant(godot_Variant *self, const godot_Variant *other);
godot_Variant godot_new_Variant_from_Variant(const godot_Variant *other);

// Destructor
void godot_destroy_Variant(godot_Variant *self);

#endif  // __GDEXTENSION_LITE_VARIANT_H__

#ifdef GDEXTENSION_LITE_IMPLEMENTATION
#ifndef __GDEXTENSION_LITE_VARIANT_H_IMPLEMENTATION__
#define __GDEXTENSION_LITE_VARIANT_H_IMPLEMENTATION__

#include "../generated/extension_interface.h"

void godot_placement_new_Variant(godot_Variant *self) {
	godot_variant_new_nil(self);
}

godot_Variant godot_new_Variant() {
	godot_Variant self;
	godot_placement_new_Variant(&self);
	return self;
}

void godot_placement_new_Variant_from_Variant(godot_Variant *self, const godot_Variant *other) {
	godot_variant_new_copy(self, other);
}

godot_Variant godot_new_Variant_from_Variant(const godot_Variant *other) {
	godot_Variant self;
	godot_placement_new_Variant_from_Variant(&self, other);
	return self;
}

void godot_destroy_Variant(godot_Variant *self) {
	godot_variant_destroy(self);
}

#endif  // __GDEXTENSION_LITE_VARIANT_H_IMPLEMENTATION__
#endif  // GDEXTENSION_LITE_IMPLEMENTATION
