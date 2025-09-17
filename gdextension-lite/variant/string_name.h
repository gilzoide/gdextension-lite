/** @file
 * string_name.h -- Godot StringName type
 */
#ifndef __GDEXTENSION_LITE_STRING_NAME_H__
#define __GDEXTENSION_LITE_STRING_NAME_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_StringName {
	uint8_t _[GDEXTENSION_LITE_SIZE_StringName];
} godot_StringName;

GDEXTENSION_LITE_ASSERT_SIZE(StringName)

#endif  // __GDEXTENSION_LITE_STRING_NAME_H__
