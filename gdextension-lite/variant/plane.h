/** @file
 * plane.h -- Godot Plane type
 */
#ifndef __GDEXTENSION_LITE_PLANE_H__
#define __GDEXTENSION_LITE_PLANE_H__

#include "float.h"
#include "sizes.h"
#include "vector3.h"

typedef struct godot_Plane {
	union {
		godot_real_t elements[4];
		struct { godot_Vector3 normal; godot_real_t d; };
	};
} godot_Plane;

GDEXTENSION_LITE_ASSERT_SIZE(Plane)

#endif  // __GDEXTENSION_LITE_PLANE_H__
