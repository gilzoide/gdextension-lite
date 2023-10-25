/** @file
 * dictionary.h -- Godot Dictionary type
 */
#ifndef __GDEXTENSION_LITE_DICTIONARY_H__
#define __GDEXTENSION_LITE_DICTIONARY_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_Dictionary {
	uint8_t _[GDEXTENSION_LITE_SIZE_Dictionary];
} godot_Dictionary;

GDEXTENSION_LITE_ASSERT_SIZE(Dictionary)

#endif  // __GDEXTENSION_LITE_DICTIONARY_H__
