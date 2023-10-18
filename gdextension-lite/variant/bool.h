/** @file
 * bool.h -- Godot bool type
 */
#ifndef __GDEXTENSION_LITE_BOOL_H__
#define __GDEXTENSION_LITE_BOOL_H__

#include "../gdextension/gdextension_interface.h"

#ifdef __cplusplus
	typedef bool godot_bool;
#else
	typedef GDExtensionBool godot_bool;
#endif

#endif  // __GDEXTENSION_LITE_BOOL_H__
