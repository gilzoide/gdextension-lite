/** @file
 * vector4.h -- Godot Vector4 type
 */
#ifndef __GDEXTENSION_LITE_VECTOR4_H__
#define __GDEXTENSION_LITE_VECTOR4_H__

#include "float.h"
#include "sizes.h"
#include "vector2.h"
#include "vector3.h"

typedef struct godot_Vector4 {
	union {
		godot_real_t coord[4];
		// xyzw
		struct { godot_real_t x, y, z, w; };
		struct { godot_Vector2 xy; godot_Vector2 zw; };
		struct { godot_Vector3 xyz; godot_real_t _0; };
		struct { godot_real_t _1; godot_Vector3 yzw; };
		// rgba
		struct { godot_real_t r, g, b, a; };
		struct { godot_Vector2 rg; godot_Vector2 ba; };
		struct { godot_Vector3 rgb; godot_real_t _2; };
		struct { godot_real_t _3; godot_Vector3 gba; };
		// stpq
		struct { godot_real_t s, t, p, q; };
		struct { godot_Vector2 st; godot_Vector2 pq; };
		struct { godot_Vector3 stp; godot_real_t _6; };
		struct { godot_real_t _7; godot_Vector3 tpq; };
	};
} godot_Vector4;

GDEXTENSION_LITE_ASSERT_SIZE(Vector4)

#endif  // __GDEXTENSION_LITE_VECTOR4_H__
