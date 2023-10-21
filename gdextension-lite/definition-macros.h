/** @file
 * definition-macros.h -- Helper macros for GDExtension Lite definitions
 */
#ifndef __GDEXTENSION_LITE_DEFINITION_MACROS_H__
#define __GDEXTENSION_LITE_DEFINITION_MACROS_H__

#define GDCLEANUP(godot_Type) \
	__attribute__((cleanup(godot_Type##_destroy))) godot_Type

#define GDEXTENSION_LITE_INLINE \
	static inline

#endif
