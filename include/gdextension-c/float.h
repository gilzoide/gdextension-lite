/** @file
 * float.h -- Godot float type
 */
#ifndef __GDEXTENSION_C_FLOAT_H__
#define __GDEXTENSION_C_FLOAT_H__

typedef double godot_float;

#ifdef REAL_T_IS_DOUBLE
	typedef double godot_real_t;
#else
	typedef float godot_real_t;
#endif

#endif
