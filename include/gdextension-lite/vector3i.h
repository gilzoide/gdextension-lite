/** @file
 * vector3i.h -- Godot Vector3i type
 */
#ifndef __GDEXTENSION_LITE_VECTOR3I_H__
#define __GDEXTENSION_LITE_VECTOR3I_H__

#include <stdint.h>

#include "vector2i.h"

typedef struct godot_Vector3i {
	union {
		int32_t coord[3];
		// xyz
		struct { int32_t x, y, z; };
		struct { godot_Vector2i xy; int32_t _0; };
		struct { int32_t _1; godot_Vector2i yz; };
		// 3D Size: width/height/depth
		struct { int32_t width, height, depth; };
	};
} godot_Vector3i;

#endif
