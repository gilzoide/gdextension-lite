/** @file
 * packed_byte_array.h -- Godot PackedByteArray type
 */
#ifndef __GDEXTENSION_LITE_PACKED_BYTE_ARRAY_H__
#define __GDEXTENSION_LITE_PACKED_BYTE_ARRAY_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_PackedByteArray {
	uint8_t _[GDEXTENSION_LITE_SIZE_PackedByteArray];
} godot_PackedByteArray;

GDEXTENSION_LITE_ASSERT_SIZE(PackedByteArray)

#endif  // __GDEXTENSION_LITE_PACKED_BYTE_ARRAY_H__
