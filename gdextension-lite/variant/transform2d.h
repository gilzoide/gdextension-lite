/** @file
 * transform2d.h -- Godot Transform2D type
 */
#ifndef __GDEXTENSION_LITE_TRANSFORM2D_H__
#define __GDEXTENSION_LITE_TRANSFORM2D_H__

#include "float.h"
#include "vector2.h"

typedef struct godot_Transform2D {
	union {
		godot_Vector2 columns[3];
		struct { godot_Vector2 x, y, origin; };
	};
} godot_Transform2D;

#endif  // __GDEXTENSION_LITE_TRANSFORM2D_H__
