/** @file
 * rect2i.h -- Godot Rect2i type
 */
#ifndef __GDEXTENSION_LITE_RECT2I_H__
#define __GDEXTENSION_LITE_RECT2I_H__

#include <stdint.h>
#include "sizes.h"
#include "vector2i.h"

typedef struct godot_Rect2i {
	union {
		struct { int32_t x, y, width, height; };
		struct { godot_Vector2i position; godot_Vector2i size; };
	};
} godot_Rect2i;

GDEXTENSION_LITE_ASSERT_SIZE(Rect2i)

#endif  // __GDEXTENSION_LITE_RECT2I_H__
