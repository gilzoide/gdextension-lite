/** @file
 * rid.h -- Godot RID type
 */
#ifndef __GDEXTENSION_C_RID_H__
#define __GDEXTENSION_C_RID_H__

#include <stdint.h>

typedef struct godot_RID {
	uint64_t id;
} godot_RID;

#endif
