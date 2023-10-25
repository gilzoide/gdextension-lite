/** @file
 * rect2.h -- Godot Rect2 type
 */
#ifndef __GDEXTENSION_LITE_RECT2_H__
#define __GDEXTENSION_LITE_RECT2_H__

#include "float.h"
#include "sizes.h"
#include "vector2.h"

typedef struct godot_Rect2 {
	union {
		struct { godot_real_t x, y, width, height; };
		struct { godot_Vector2 position; godot_Vector2 size; };
	};
} godot_Rect2;

GDEXTENSION_LITE_ASSERT_SIZE(Rect2)

#endif  // __GDEXTENSION_LITE_RECT2_H__
