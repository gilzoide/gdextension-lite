/** @file
 * signal.h -- Godot Signal type
 */
#ifndef __GDEXTENSION_LITE_SIGNAL_H__
#define __GDEXTENSION_LITE_SIGNAL_H__

#include <stdint.h>

typedef struct godot_Signal {
	uint8_t _[16];
} godot_Signal;

#endif
