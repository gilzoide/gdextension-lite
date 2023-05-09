/** @file
 * packed_vector2_array.h -- Godot PackedVector2Array type
 */
#ifndef __GDEXTENSION_C_PACKED_VECTOR2_ARRAY_H__
#define __GDEXTENSION_C_PACKED_VECTOR2_ARRAY_H__

#include <stdint.h>

typedef struct godot_PackedVector2Array {
	uint8_t _[2 * sizeof(void *)];
} godot_PackedVector2Array;

#endif
