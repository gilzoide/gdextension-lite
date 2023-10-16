/** @file
 * implementation-macros.hpp -- Helper macros for GDExtension Lite C++ implementation
 */
#ifndef __GDEXTENSION_LITE_IMPLEMENTATION_MACROS_HPP__
#define __GDEXTENSION_LITE_IMPLEMENTATION_MACROS_HPP__

struct godot_Variant;

namespace gdextension_lite {

template<class... Args>
inline void fill_variadic_array(const godot_Variant *array[], const godot_Variant& var, Args... args) {
	*array = &var;
	fill_variadic_array(array + 1, args...);
}
inline void fill_variadic_array(const godot_Variant *array[], const godot_Variant& var) {
	*array = &var;
}

#define GDEXTENSION_LITE_VARIADIC_TEMPLATE_TO_ARRAY(args_name, argc_name, argv_name) \
	int argc_name = sizeof...(args_name); \
	const godot_Variant *argv_name[argc_name]; \
	gdextension_lite::fill_variadic_array(argv_name, args_name...);

}

#endif  // __GDEXTENSION_LITE_IMPLEMENTATION_MACROS_HPP__

