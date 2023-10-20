/** @file
 * implementation-macros.h -- Helper macros for GDExtension Lite implementation
 */
#ifndef __GDEXTENSION_LITE_IMPLEMENTATION_MACROS_H__
#define __GDEXTENSION_LITE_IMPLEMENTATION_MACROS_H__

#define GDEXTENSION_LITE_LAZY_INIT_VARIANT_CONSTRUCTOR(name, type, index) \
	if (godot_ptr_##name == NULL) { \
		godot_ptr_##name = godot_variant_get_ptr_constructor(type, index); \
	}

#define GDEXTENSION_LITE_LAZY_INIT_TYPE_FROM_VARIANT(name, type) \
		if (godot_ptr_new_##name##_from_Variant == NULL) { \
			godot_ptr_new_##name##_from_Variant = godot_get_variant_to_type_constructor(type); \
		}
#define GDEXTENSION_LITE_LAZY_INIT_VARIANT_FROM_TYPE(name, type) \
		if (godot_ptr_new_Variant_from_##name == NULL) { \
			godot_ptr_new_Variant_from_##name = godot_get_variant_from_type_constructor(type); \
		}

#define GDEXTENSION_LITE_LAZY_INIT_VARIANT_DESTRUCTOR(name, type) \
		if (godot_ptr_##name##_destroy == NULL) { \
			godot_ptr_##name##_destroy = godot_variant_get_ptr_destructor(type); \
		}

#define GDEXTENSION_LITE_LAZY_INIT_VARIANT_MEMBER(get_or_set, name, type, member) \
	if (godot_ptr_##name##_##get_or_set##_##member == NULL) { \
		godot_StringName _member = godot_new_StringName_from_latin1_chars(#name); \
		godot_ptr_##name##_##get_or_set##_##member = godot_variant_get_ptr_##get_or_set##ter(type, &_member); \
		godot_StringName_destroy(&_member); \
	}

#define GDEXTENSION_LITE_LAZY_INIT_VARIANT_INDEXING(get_or_set, indexed_or_keyed, name, type) \
	if (godot_ptr_##name##_##indexed_or_keyed##_##get_or_set == NULL) { \
		godot_ptr_##name##_##indexed_or_keyed##_##get_or_set = godot_variant_get_ptr_##indexed_or_keyed##_##get_or_set##ter(type); \
	}

#define GDEXTENSION_LITE_LAZY_INIT_VARIANT_OPERATOR(name, op, type1, type2) \
	if (godot_ptr_##name == NULL) { \
		godot_ptr_##name = godot_variant_get_ptr_operator_evaluator(op, type1, type2); \
	}

#define GDEXTENSION_LITE_LAZY_INIT_VARIANT_METHOD(name, type, method, hash) \
	if (godot_ptr_##name##_##method == NULL) { \
		godot_StringName _method = godot_new_StringName_from_latin1_chars(#method); \
		godot_ptr_##name##_##method = godot_variant_get_ptr_builtin_method(type, &_method, hash); \
		godot_StringName_destroy(&_method); \
	}

#define GDEXTENSION_LITE_LAZY_INIT_UTILITY_FUNCTION(name, hash) \
	if (godot_ptr_##name == NULL) { \
		godot_StringName _name = godot_new_StringName_from_latin1_chars(#name); \
		godot_ptr_##name = godot_variant_get_ptr_utility_function(&_name, hash); \
		godot_StringName_destroy(&_name); \
	}

#define GDEXTENSION_LITE_LAZY_INIT_CLASS_METHOD(name, method, hash) \
	if (godot_ptr_##name##_##method == NULL) { \
		godot_StringName _class = godot_new_StringName_from_latin1_chars(#name); \
		godot_StringName _method = godot_new_StringName_from_latin1_chars(#method); \
		godot_ptr_##name##_##method = godot_classdb_get_method_bind(&_class, &_method, hash); \
		godot_StringName_destroy(&_method); \
		godot_StringName_destroy(&_class); \
	}

#define GDEXTENSION_LITE_LAZY_INIT_EXTENSION_INTERFACE(symbol) \
	if (godot_ptr_##symbol == NULL) { \
		*((void **) &godot_ptr_##symbol) = (void *) gdextension_lite_get_proc_address(#symbol); \
	}

#define GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(return_type, placement_new, ...) \
	return_type _ret; \
	placement_new(&_ret, ##__VA_ARGS__); \
	return _ret

#endif  // __GDEXTENSION_LITE_IMPLEMENTATION_MACROS_H__
