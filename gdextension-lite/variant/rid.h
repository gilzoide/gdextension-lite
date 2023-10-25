/** @file
 * rid.h -- Godot RID type
 */
#ifndef __GDEXTENSION_LITE_RID_H__
#define __GDEXTENSION_LITE_RID_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_RID {
	uint8_t _[GDEXTENSION_LITE_SIZE_RID];
} godot_RID;

GDEXTENSION_LITE_ASSERT_SIZE(RID)

#endif  // __GDEXTENSION_LITE_RID_H__
