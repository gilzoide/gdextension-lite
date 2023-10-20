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


#ifdef __cplusplus
extern "C" {
#endif

// Constructors
void godot_placement_new_Variant_nil(godot_Variant *self);
godot_Variant godot_new_Variant_nil();
void godot_placement_new_Variant_from_Variant(godot_Variant *self, const godot_Variant *other);
godot_Variant godot_new_Variant_from_Variant(const godot_Variant *other);

// Destructor
void godot_Variant_destroy(godot_Variant *self);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_VARIANT_H__
