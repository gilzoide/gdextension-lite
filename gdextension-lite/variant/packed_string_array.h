/** @file
 * packed_string_array.h -- Godot PackedStringArray type
 */
#ifndef __GDEXTENSION_LITE_PACKED_STRING_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_STRING_ARRAY_H__

#include <stdint.h>

typedef struct godot_PackedStringArray {
	uint8_t _[2 * sizeof(void *)];
} godot_PackedStringArray;

#endif
