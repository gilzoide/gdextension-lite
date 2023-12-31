/** @file
 * aabb.h -- Godot AABB type
 */
#ifndef __GDEXTENSION_LITE_AABB_H__
#define __GDEXTENSION_LITE_AABB_H__

#include "sizes.h"
#include "vector3.h"

typedef struct godot_AABB {
	godot_Vector3 position;
	godot_Vector3 size;
} godot_AABB;

GDEXTENSION_LITE_ASSERT_SIZE(AABB)

#endif  // __GDEXTENSION_LITE_AABB_H__
