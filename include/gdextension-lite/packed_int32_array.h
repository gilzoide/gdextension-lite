/** @file
 * packed_int32_array.h -- Godot PackedInt32Array type
 */
#ifndef __GDEXTENSION_C_PACKED_INT32_ARRAY_H__
#define __GDEXTENSION_C_PACKED_INT32_ARRAY_H__

#include <stdint.h>

typedef struct godot_PackedInt32Array {
	uint8_t _[2 * sizeof(void *)];
} godot_PackedInt32Array;

#endif
