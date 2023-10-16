/** @file
 * packed_color_array.h -- Godot PackedColorArray type
 */
#ifndef __GDEXTENSION_LITE_PACKED_COLOR_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_COLOR_ARRAY_H__

#include <stdint.h>

typedef struct godot_PackedColorArray {
	uint8_t _[2 * sizeof(void *)];
} godot_PackedColorArray;

#endif  // __GDEXTENSION_LITE_PACKED_COLOR_ARRAY_H__
