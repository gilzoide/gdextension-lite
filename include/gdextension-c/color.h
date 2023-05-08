/** @file
 * color.h -- Godot Color type
 */
#ifndef __GDEXTENSION_C_COLOR_H__
#define __GDEXTENSION_C_COLOR_H__

typedef struct godot_Color {
	union {
		float components[4];
		struct { float r, g, b, a; };
	};
} godot_Color;

#endif
