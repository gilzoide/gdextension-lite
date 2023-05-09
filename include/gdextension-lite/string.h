/** @file
 * string.h -- Godot String type
 */
#ifndef __GDEXTENSION_C_STRING_H__
#define __GDEXTENSION_C_STRING_H__

#include <stdint.h>

typedef struct godot_String {
	uint8_t _[sizeof(void *)];
} godot_String;

#endif
