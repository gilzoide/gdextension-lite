/** @file
 * packed_vector2_array.h -- Godot PackedVector2Array type
 */
#ifndef __GDEXTENSION_LITE_PACKED_VECTOR2_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_VECTOR2_ARRAY_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_PackedVector2Array {
	uint8_t _[GDEXTENSION_LITE_SIZE_PackedVector2Array];
} godot_PackedVector2Array;

GDEXTENSION_LITE_ASSERT_SIZE(PackedVector2Array)

#endif  // __GDEXTENSION_LITE_PACKED_VECTOR2_ARRAY_H__
