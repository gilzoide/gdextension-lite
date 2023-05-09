/** @file
 * basis.h -- Godot Basis type
 */
#ifndef __GDEXTENSION_LITE_BASIS_H__
#define __GDEXTENSION_LITE_BASIS_H__

#include "vector3.h"

typedef struct godot_Basis {
	godot_Vector3 rows[3];
} godot_Basis;

#endif
