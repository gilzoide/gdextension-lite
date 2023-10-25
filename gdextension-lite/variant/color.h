/** @file
 * color.h -- Godot Color type
 */
#ifndef __GDEXTENSION_LITE_COLOR_H__
#define __GDEXTENSION_LITE_COLOR_H__

#include "sizes.h"

typedef struct godot_Color {
	union {
		float components[4];
		struct { float r, g, b, a; };
	};
} godot_Color;

GDEXTENSION_LITE_ASSERT_SIZE(Color)

#endif  // __GDEXTENSION_LITE_COLOR_H__
