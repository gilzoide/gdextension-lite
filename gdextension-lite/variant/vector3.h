/** @file
 * vector3.h -- Godot Vector3 type
 */
#ifndef __GDEXTENSION_LITE_VECTOR3_H__
#define __GDEXTENSION_LITE_VECTOR3_H__

#include "float.h"
#include "vector2.h"

typedef struct godot_Vector3 {
	union {
		godot_real_t coord[3];
		// xyz
		struct { godot_real_t x, y, z; };
		struct { godot_Vector2 xy; godot_real_t _0; };
		struct { godot_real_t _1; godot_Vector2 yz; };
		// rgb
		struct { godot_real_t r, g, b; };
		struct { godot_Vector2 rg; godot_real_t _2; };
		struct { godot_real_t _3; godot_Vector2 gb; };
		// stp
		struct { godot_real_t s, t, p; };
		struct { godot_Vector2 st; godot_real_t _6; };
		struct { godot_real_t _7; godot_Vector2 tp; };
		// 3D Size: width/height/depth
		struct { godot_real_t width, height, depth; };
	};
} godot_Vector3;

#endif  // __GDEXTENSION_LITE_VECTOR3_H__
