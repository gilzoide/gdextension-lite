/** @file
 * packed_float64_array.h -- Godot PackedFloat64Array type
 */
#ifndef __GDEXTENSION_LITE_PACKED_FLOAT64_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_FLOAT64_ARRAY_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_PackedFloat64Array {
	uint8_t _[GDEXTENSION_LITE_SIZE_PackedFloat64Array];
} godot_PackedFloat64Array;

GDEXTENSION_LITE_ASSERT_SIZE(PackedFloat64Array)

#endif  // __GDEXTENSION_LITE_PACKED_FLOAT64_ARRAY_H__
