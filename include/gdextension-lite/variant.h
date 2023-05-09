/** @file
 * variant.h -- Godot Variant type
 */
#ifndef __GDEXTENSION_LITE_VARIANT_H__
#define __GDEXTENSION_LITE_VARIANT_H__

#include <stdint.h>

#ifdef REAL_T_IS_DOUBLE
	#define GODOT_VARIANT_SIZE 40
#else
	#define GODOT_VARIANT_SIZE 24
#endif

typedef struct godot_Variant {
	uint8_t _[GODOT_VARIANT_SIZE];
} godot_Variant;

#endif
