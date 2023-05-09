/** @file
 * bool.h -- Godot bool type
 */
#ifndef __GDEXTENSION_C_BOOL_H__
#define __GDEXTENSION_C_BOOL_H__

#if defined(__cplusplus)
	typedef bool godot_bool;
#elif defined(__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
	#include <stdbool.h>
	typedef bool godot_bool;
#else
	#error Please use at least C99, which has proper bool support
#endif

#endif
