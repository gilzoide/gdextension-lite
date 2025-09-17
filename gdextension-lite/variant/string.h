/** @file
 * string.h -- Godot String type
 */
#ifndef __GDEXTENSION_LITE_STRING_H__
#define __GDEXTENSION_LITE_STRING_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_String {
	uint8_t _[GDEXTENSION_LITE_SIZE_String];
} godot_String;

GDEXTENSION_LITE_ASSERT_SIZE(String)

#endif  // __GDEXTENSION_LITE_STRING_H__
