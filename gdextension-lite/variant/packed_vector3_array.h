/** @file
 * packed_vector3_array.h -- Godot PackedVector3Array type
 */
#ifndef __GDEXTENSION_LITE_PACKED_VECTOR3_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_VECTOR3_ARRAY_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_PackedVector3Array {
	uint8_t _[GDEXTENSION_LITE_SIZE_PackedVector3Array];
} godot_PackedVector3Array;

GDEXTENSION_LITE_ASSERT_SIZE(PackedVector3Array)

#endif  // __GDEXTENSION_LITE_PACKED_VECTOR3_ARRAY_H__
