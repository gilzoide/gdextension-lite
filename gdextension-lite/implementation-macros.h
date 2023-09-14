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
		if (godot_ptr_destroy_##name == NULL) { \
			godot_ptr_destroy_##name = godot_variant_get_ptr_destructor(type); \
		}

#define GDEXTENSION_LITE_LAZY_INIT_VARIANT_MEMBER(get_or_set, name, type, member) \
	if (godot_ptr_##name##_##get_or_set##_##member == NULL) { \
		GDEXTENSION_LITE_WITH_STRING_NAME(name, _member, { \
			godot_ptr_##name##_##get_or_set##_##member = godot_variant_get_ptr_##get_or_set##ter(type, &_member); \
		}); \
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
		GDEXTENSION_LITE_WITH_STRING_NAME(method, _method, { \
			godot_ptr_##name##_##method = godot_variant_get_ptr_builtin_method(type, &_method, hash); \
		}); \
	}

#define GDEXTENSION_LITE_LAZY_INIT_UTILITY_FUNCTION(name, hash) \
	if (godot_ptr_##name == NULL) { \
		GDEXTENSION_LITE_WITH_STRING_NAME(name, _name, { \
			godot_ptr_##name = godot_variant_get_ptr_utility_function(&_name, hash); \
		}); \
	}

#define GDEXTENSION_LITE_LAZY_INIT_CLASS_METHOD(name, method, hash) \
	if (godot_ptr_##name##_##method == NULL) { \
		GDEXTENSION_LITE_WITH_STRING_NAME(name, _class, { \
			GDEXTENSION_LITE_WITH_STRING_NAME(method, _method, { \
				godot_ptr_##name##_##method = godot_classdb_get_method_bind(&_class, &_method, hash); \
			}); \
		}); \
	}

#endif  // __GDEXTENSION_LITE_IMPLEMENTATION_MACROS_H__
