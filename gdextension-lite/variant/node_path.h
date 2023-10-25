/** @file
 * node_path.h -- Godot NodePath type
 */
#ifndef __GDEXTENSION_LITE_NODE_PATH_H__
#define __GDEXTENSION_LITE_NODE_PATH_H__

#include <stdint.h>
#include "sizes.h"

typedef struct godot_NodePath {
	uint8_t _[GDEXTENSION_LITE_SIZE_NodePath];
} godot_NodePath;

GDEXTENSION_LITE_ASSERT_SIZE(NodePath)

#endif  // __GDEXTENSION_LITE_NODE_PATH_H__
