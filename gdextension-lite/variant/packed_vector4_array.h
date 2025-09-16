/** @file
 * packed_vector4_array.h -- Godot PackedVector4Array type
 */
#ifndef __GDEXTENSION_LITE_PACKED_VECTOR4_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_VECTOR4_ARRAY_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_PackedVector4Array {
	uint8_t _[GDEXTENSION_LITE_SIZE_PackedVector4Array];
} godot_PackedVector4Array;

GDEXTENSION_LITE_ASSERT_SIZE(PackedVector4Array)

#endif  // __GDEXTENSION_LITE_PACKED_VECTOR4_ARRAY_H__
