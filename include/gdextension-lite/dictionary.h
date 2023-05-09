/** @file
 * dictionary.h -- Godot Dictionary type
 */
#ifndef __GDEXTENSION_C_DICTIONARY_H__
#define __GDEXTENSION_C_DICTIONARY_H__

#include <stdint.h>

typedef struct godot_Dictionary {
	uint8_t _[sizeof(void *)];
} godot_Dictionary;

#endif
