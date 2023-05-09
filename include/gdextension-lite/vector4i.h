/** @file
 * vector4i.h -- Godot Vector4i type
 */
#ifndef __GDEXTENSION_C_VECTOR4I_H__
#define __GDEXTENSION_C_VECTOR4I_H__

#include <stdint.h>

#include "vector2i.h"
#include "vector3i.h"

typedef struct godot_Vector4i {
	union {
		int32_t coord[4];
		// xyzw
		struct { int32_t x, y, z, w; };
		struct { godot_Vector2i xy; godot_Vector2i zw; };
		struct { godot_Vector3i xyz; int32_t _0; };
		struct { int32_t _1; godot_Vector3i yzw; };
	};
} godot_Vector4i;

#endif
