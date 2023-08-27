/** @file
 * float.h -- Godot float type
 */
#ifndef __GDEXTENSION_LITE_FLOAT_H__
#define __GDEXTENSION_LITE_FLOAT_H__

#include <math.h>

typedef double godot_float;

#ifdef REAL_T_IS_DOUBLE
	typedef double godot_real_t;
#else
	typedef float godot_real_t;
#endif

#define godot_inf INFINITY

#endif
