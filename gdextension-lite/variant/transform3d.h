/** @file
 * transform3d.h -- Godot Transform3D type
 */
#ifndef __GDEXTENSION_LITE_TRANSFORM3D_H__
#define __GDEXTENSION_LITE_TRANSFORM3D_H__

#include "basis.h"
#include "sizes.h"
#include "vector3.h"

typedef struct godot_Transform3D {
	godot_Basis basis;
	godot_Vector3 origin;
} godot_Transform3D;

GDEXTENSION_LITE_ASSERT_SIZE(Transform3D)

#endif  // __GDEXTENSION_LITE_TRANSFORM3D_H__
