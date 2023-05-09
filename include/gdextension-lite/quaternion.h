/** @file
 * quaternion.h -- Godot Quaternion type
 */
#ifndef __GDEXTENSION_LITE_QUATERNION_H__
#define __GDEXTENSION_LITE_QUATERNION_H__

#include "float.h"
#include "vector2.h"
#include "vector3.h"

typedef struct godot_Quaternion {
	union {
		godot_real_t elements[4];
		struct { godot_real_t x, y, z, w; };
		struct { godot_Vector2 xy; godot_Vector2 zw; };
		struct { godot_Vector3 xyz; godot_real_t _0; };
		struct { godot_real_t _1; godot_Vector3 yzw; };
	};
} godot_Quaternion;

#endif
