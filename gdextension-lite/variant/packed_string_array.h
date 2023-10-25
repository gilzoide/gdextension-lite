/** @file
 * packed_string_array.h -- Godot PackedStringArray type
 */
#ifndef __GDEXTENSION_LITE_PACKED_STRING_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_STRING_ARRAY_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_PackedStringArray {
	uint8_t _[GDEXTENSION_LITE_SIZE_PackedStringArray];
} godot_PackedStringArray;

GDEXTENSION_LITE_ASSERT_SIZE(PackedStringArray)

#endif  // __GDEXTENSION_LITE_PACKED_STRING_ARRAY_H__
