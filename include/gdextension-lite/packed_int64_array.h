/** @file
 * packed_int64_array.h -- Godot PackedInt64Array type
 */
#ifndef __GDEXTENSION_C_PACKED_INT64_ARRAY_H__
#define __GDEXTENSION_C_PACKED_INT64_ARRAY_H__

#include <stdint.h>

typedef struct godot_PackedInt64Array {
	uint8_t _[2 * sizeof(void *)];
} godot_PackedInt64Array;

#endif
