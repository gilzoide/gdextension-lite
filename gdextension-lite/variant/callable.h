/** @file
 * callable.h -- Godot Callable type
 */
#ifndef __GDEXTENSION_LITE_CALLABLE_H__
#define __GDEXTENSION_LITE_CALLABLE_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_Callable {
	uint8_t _[GDEXTENSION_LITE_SIZE_Callable];
} godot_Callable;

GDEXTENSION_LITE_ASSERT_SIZE(Callable)

#endif  // __GDEXTENSION_LITE_CALLABLE_H__
