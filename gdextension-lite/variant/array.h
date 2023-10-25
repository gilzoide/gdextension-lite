/** @file
 * array.h -- Godot Array type
 */
#ifndef __GDEXTENSION_LITE_ARRAY_H__
#define __GDEXTENSION_LITE_ARRAY_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_Array {
	uint8_t _[GDEXTENSION_LITE_SIZE_Array];
} godot_Array;

GDEXTENSION_LITE_ASSERT_SIZE(Array)

#define godot_TypedArray(type)  godot_Array

#endif  // __GDEXTENSION_LITE_ARRAY_H__
