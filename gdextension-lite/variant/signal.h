/** @file
 * signal.h -- Godot Signal type
 */
#ifndef __GDEXTENSION_LITE_SIGNAL_H__
#define __GDEXTENSION_LITE_SIGNAL_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_Signal {
	uint8_t _[GDEXTENSION_LITE_SIZE_Signal];
} godot_Signal;

GDEXTENSION_LITE_ASSERT_SIZE(Signal)

#endif  // __GDEXTENSION_LITE_SIGNAL_H__
