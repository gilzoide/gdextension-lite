/** @file
 * aabb.h -- Godot AABB type
 */
#ifndef __GDEXTENSION_C_AABB_H__
#define __GDEXTENSION_C_AABB_H__

#include "vector3.h"

typedef struct godot_AABB {
	godot_Vector3 position;
	godot_Vector3 size;
} godot_AABB;

#endif
