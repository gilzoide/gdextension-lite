/** @file
 * array.h -- Godot Array type
 */
#ifndef __GDEXTENSION_C_ARRAY_H__
#define __GDEXTENSION_C_ARRAY_H__

#include <stdint.h>

typedef struct godot_Array {
	uint8_t _[sizeof(void *)];
} godot_Array;

#endif
