/** @file
 * callable.h -- Godot Callable type
 */
#ifndef __GDEXTENSION_LITE_CALLABLE_H__
#define __GDEXTENSION_LITE_CALLABLE_H__

#include <stdint.h>

typedef struct godot_Callable {
	uint8_t _[16];
} godot_Callable;

#endif  // __GDEXTENSION_LITE_CALLABLE_H__
