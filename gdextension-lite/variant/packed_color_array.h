/** @file
 * packed_color_array.h -- Godot PackedColorArray type
 */
#ifndef __GDEXTENSION_LITE_PACKED_COLOR_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_COLOR_ARRAY_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_PackedColorArray {
	uint8_t _[GDEXTENSION_LITE_SIZE_PackedColorArray];
} godot_PackedColorArray;

GDEXTENSION_LITE_ASSERT_SIZE(PackedColorArray)

#endif  // __GDEXTENSION_LITE_PACKED_COLOR_ARRAY_H__
