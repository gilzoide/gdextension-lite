/** @file
 * packed_byte_array.h -- Godot PackedByteArray type
 */
#ifndef __GDEXTENSION_LITE_PACKED_BYTE_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_BYTE_ARRAY_H__

#include <stdint.h>

typedef struct godot_PackedByteArray {
	uint8_t _[2 * sizeof(void *)];
} godot_PackedByteArray;

#endif  // __GDEXTENSION_LITE_PACKED_BYTE_ARRAY_H__
