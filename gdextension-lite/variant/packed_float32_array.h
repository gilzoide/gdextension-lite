/** @file
 * packed_float32_array.h -- Godot PackedFloat32Array type
 */
#ifndef __GDEXTENSION_LITE_PACKED_FLOAT32_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_FLOAT32_ARRAY_H__

#include <stdint.h>

typedef struct godot_PackedFloat32Array {
	uint8_t _[2 * sizeof(void *)];
} godot_PackedFloat32Array;

#endif  // __GDEXTENSION_LITE_PACKED_FLOAT32_ARRAY_H__
