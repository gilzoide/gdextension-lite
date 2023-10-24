/** @file
 * definition-macros.h -- Helper macros for GDExtension Lite definitions
 */
#ifndef __GDEXTENSION_LITE_DEFINITION_MACROS_H__
#define __GDEXTENSION_LITE_DEFINITION_MACROS_H__

#define GDCLEANUP(godot_Type) \
	__attribute__((cleanup(godot_Type##_destroy))) godot_Type

#define GDEXTENSION_LITE_INLINE \
	static inline

#if __cplusplus >= 201103L
	#define DEFAULT_VALUE(value) = value
#else
	#define DEFAULT_VALUE(value)
#endif

#ifndef GDEXTENSION_LITE_DECL
	#ifndef GDEXTENSION_LITE_VISIBILITY
		#define GDEXTENSION_LITE_VISIBILITY "hidden"
	#endif

	#define GDEXTENSION_LITE_DECL \
		__attribute__((__visibility__(GDEXTENSION_LITE_VISIBILITY)))
#endif

#endif
