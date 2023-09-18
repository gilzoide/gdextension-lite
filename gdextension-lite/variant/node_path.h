/** @file
 * node_path.h -- Godot NodePath type
 */
#ifndef __GDEXTENSION_LITE_NODE_PATH_H__
#define __GDEXTENSION_LITE_NODE_PATH_H__

#include <stdint.h>

typedef struct godot_NodePath {
	uint8_t _[sizeof(void *)];
} godot_NodePath;

#endif  // __GDEXTENSION_LITE_NODE_PATH_H__
