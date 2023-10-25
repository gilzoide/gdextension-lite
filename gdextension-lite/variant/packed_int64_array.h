/** @file
 * packed_int64_array.h -- Godot PackedInt64Array type
 */
#ifndef __GDEXTENSION_LITE_PACKED_INT64_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_INT64_ARRAY_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_PackedInt64Array {
	uint8_t _[GDEXTENSION_LITE_SIZE_PackedInt64Array];
} godot_PackedInt64Array;

GDEXTENSION_LITE_ASSERT_SIZE(PackedInt64Array)

#endif  // __GDEXTENSION_LITE_PACKED_INT64_ARRAY_H__
