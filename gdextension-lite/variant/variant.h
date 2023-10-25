/** @file
 * variant.h -- Godot Variant type
 */
#ifndef __GDEXTENSION_LITE_VARIANT_H__
#define __GDEXTENSION_LITE_VARIANT_H__

#include <stdint.h>
#include "sizes.h"
#include "../definition-macros.h"

typedef struct godot_Variant {
	uint8_t _[GDEXTENSION_LITE_SIZE_Variant];
} godot_Variant;

GDEXTENSION_LITE_ASSERT_SIZE(Variant)


#ifdef __cplusplus
extern "C" {
#endif

// Constructors
GDEXTENSION_LITE_DECL void godot_placement_new_Variant_nil(godot_Variant *self);
GDEXTENSION_LITE_DECL godot_Variant godot_new_Variant_nil();
GDEXTENSION_LITE_DECL void godot_placement_new_Variant_from_Variant(godot_Variant *self, const godot_Variant *other);
GDEXTENSION_LITE_DECL godot_Variant godot_new_Variant_from_Variant(const godot_Variant *other);

// Destructor
GDEXTENSION_LITE_DECL void godot_Variant_destroy(godot_Variant *self);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_VARIANT_H__
