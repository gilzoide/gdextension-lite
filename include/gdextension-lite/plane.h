/** @file
 * plane.h -- Godot Plane type
 */
#ifndef __GDEXTENSION_C_PLANE_H__
#define __GDEXTENSION_C_PLANE_H__

#include "float.h"
#include "vector3.h"

typedef struct godot_Plane {
	union {
		godot_real_t elements[4];
		struct { godot_Vector3 normal; godot_real_t d; };
	};
} godot_Plane;

#endif
