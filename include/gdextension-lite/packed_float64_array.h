/** @file
 * packed_float64_array.h -- Godot PackedFloat64Array type
 */
#ifndef __GDEXTENSION_C_PACKED_FLOAT64_ARRAY_H__
#define __GDEXTENSION_C_PACKED_FLOAT64_ARRAY_H__

#include <stdint.h>

typedef struct godot_PackedFloat64Array {
	uint8_t _[2 * sizeof(void *)];
} godot_PackedFloat64Array;

#endif
