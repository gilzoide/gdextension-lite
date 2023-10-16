/** @file
 * vector2i.h -- Godot Vector2i type
 */
#ifndef __GDEXTENSION_LITE_VECTOR2I_H__
#define __GDEXTENSION_LITE_VECTOR2I_H__

#include <stdint.h>

typedef struct godot_Vector2i {
	union {
		int32_t coord[2];
		// xy
		struct { int32_t x, y; };
		// Size: width/height
		struct { int32_t width, height; };
	};
} godot_Vector2i;

#endif  // __GDEXTENSION_LITE_VECTOR2I_H__
