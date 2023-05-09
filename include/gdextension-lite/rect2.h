/** @file
 * rect2.h -- Godot Rect2 type
 */
#ifndef __GDEXTENSION_C_RECT2_H__
#define __GDEXTENSION_C_RECT2_H__

#include "float.h"
#include "vector2.h"

typedef struct godot_Rect2 {
	union {
		struct { godot_real_t x, y, width, height; };
		struct { godot_Vector2 position; godot_Vector2 size; };
	};
} godot_Rect2;

#endif
