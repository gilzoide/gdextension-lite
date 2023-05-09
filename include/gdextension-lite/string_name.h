/** @file
 * string_name.h -- Godot StringName type
 */
#ifndef __GDEXTENSION_C_STRING_NAME_H__
#define __GDEXTENSION_C_STRING_NAME_H__

#include <stdint.h>

typedef struct godot_StringName {
	uint8_t _[sizeof(void *)];
} godot_StringName;

#endif
