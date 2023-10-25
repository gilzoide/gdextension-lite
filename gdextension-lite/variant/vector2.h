/** @file
 * vector2.h -- Godot Vector2 type
 */
#ifndef __GDEXTENSION_LITE_VECTOR2_H__
#define __GDEXTENSION_LITE_VECTOR2_H__

#include "float.h"
#include "sizes.h"

typedef struct godot_Vector2 {
	union {
		godot_real_t coord[2];
		// xy
		struct { godot_real_t x, y; };
		// rg
		struct { godot_real_t r, g; };
		// st
		struct { godot_real_t s, t; };
		// uv
		struct { godot_real_t u, v; };
		// Size: width/height
		struct { godot_real_t width, height; };
	};
} godot_Vector2;

GDEXTENSION_LITE_ASSERT_SIZE(Vector2)

#endif  // __GDEXTENSION_LITE_VECTOR2_H__
