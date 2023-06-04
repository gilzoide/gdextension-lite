/** @file
 * gdextension-interface.h -- Global GDExtension interface API pointer
 */
#ifndef __GDEXTENSION_LITE_INTERFACE_H__
#define __GDEXTENSION_LITE_INTERFACE_H__

#include "gdextension/gdextension_interface.h"

extern const GDExtensionInterface *godot_interface;

#endif

#ifdef GDEXTENSION_LITE_IMPLEMENTATION

const GDExtensionInterface *godot_interface;

#endif
