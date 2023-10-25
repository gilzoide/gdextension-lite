/** @file
 * projection.h -- Godot Projection type
 */
#ifndef __GDEXTENSION_LITE_PROJECTION_H__
#define __GDEXTENSION_LITE_PROJECTION_H__

#include "float.h"
#include "sizes.h"
#include "vector4.h"

typedef struct godot_Projection {
	union {
		godot_real_t columns[4][4];
		struct { godot_Vector4 x, y, z, w; };
	};
} godot_Projection;

GDEXTENSION_LITE_ASSERT_SIZE(Projection)

#endif  // __GDEXTENSION_LITE_PROJECTION_H__
