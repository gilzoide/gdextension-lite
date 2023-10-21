/** @file
 * implementation-macros.h -- Helper macros for GDExtension Lite implementation
 */
#ifndef __GDEXTENSION_LITE_IMPLEMENTATION_MACROS_H__
#define __GDEXTENSION_LITE_IMPLEMENTATION_MACROS_H__

#ifdef __cplusplus
extern "C" {
#endif

struct godot_StringName;
void godot_StringName_destroy(struct godot_StringName *string_name);

// Macro magic to get the number of variable arguments
// Ref: https://groups.google.com/g/comp.std.c/c/d-6Mj5Lko_s
#define GDEXTENSION_LITE_NARG(...)  GDEXTENSION_LITE_NARG_(__VA_ARGS__, GDEXTENSION_LITE_NARG_RSEQ_N())
#define GDEXTENSION_LITE_NARG_(...)  GDEXTENSION_LITE_NARG_N(__VA_ARGS__)
#define GDEXTENSION_LITE_NARG_N(_1, _2, _3, _4, _5, _6, _7, _8, _9,_10,_11,_12,_13,_14,_15,_16,_17,_18,_19,_20,_21,_22,_23,_24,_25,_26,_27,_28,_29,_30,_31,_32,_33,_34,_35,_36,_37,_38,_39,_40,_41,_42,_43,_44,_45,_46,_47,_48,_49,_50,_51,_52,_53,_54,_55,_56,_57,_58,_59,_60,_61,_62,_63,N,...)  N
#define GDEXTENSION_LITE_NARG_RSEQ_N()  63,62,61,60,59,58,57,56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0

// Macro magic to apply a function macro to variadic arguments
// Ref: https://github.com/swansontec/map-macro/issues/11
#define GDEXTENSION_LITE_EVAL0(...) __VA_ARGS__
#define GDEXTENSION_LITE_EVAL1(...) GDEXTENSION_LITE_EVAL0( GDEXTENSION_LITE_EVAL0 ( GDEXTENSION_LITE_EVAL0 ( __VA_ARGS__ )))
#define GDEXTENSION_LITE_EVAL2(...) GDEXTENSION_LITE_EVAL1( GDEXTENSION_LITE_EVAL1 ( GDEXTENSION_LITE_EVAL1 ( __VA_ARGS__ )))
#define GDEXTENSION_LITE_EVAL3(...) GDEXTENSION_LITE_EVAL2( GDEXTENSION_LITE_EVAL2 ( GDEXTENSION_LITE_EVAL2 ( __VA_ARGS__ )))
#define GDEXTENSION_LITE_EVAL4(...) GDEXTENSION_LITE_EVAL3( GDEXTENSION_LITE_EVAL3 ( GDEXTENSION_LITE_EVAL3 ( __VA_ARGS__ )))
#define GDEXTENSION_LITE_EVAL(...) GDEXTENSION_LITE_EVAL4(__VA_ARGS__)
#define GDEXTENSION_LITE_NOP
#define GDEXTENSION_LITE_MAP_POP0(F,X,...) F(X) __VA_OPT__(GDEXTENSION_LITE_MAP_POP1 GDEXTENSION_LITE_NOP (F,__VA_ARGS__))
#define GDEXTENSION_LITE_MAP_POP1(F,X,...) F(X) __VA_OPT__(GDEXTENSION_LITE_MAP_POP0 GDEXTENSION_LITE_NOP (F,__VA_ARGS__))
#define GDEXTENSION_LITE_MAP(F,...) __VA_OPT__(GDEXTENSION_LITE_EVAL (GDEXTENSION_LITE_MAP_POP0(F, __VA_ARGS__)))

// Method argument list
#define GDEXTENSION_LITE_SET_ARG(a) \
	_args[_args_i++] = a;

#define GDEXTENSION_LITE_SET_VARIANT_ARG(a) \
	GDCLEANUP(godot_Variant) _var_##a = godot_new_Variant(a); \
	_args[_args_i++] = &_var_##a;

#define GDEXTENSION_LITE_DEFINE_ARGS(...) \
	const int _final_argc = GDEXTENSION_LITE_NARG(__VA_ARGS__); \
	GDExtensionConstTypePtr _args[_final_argc] = { __VA_ARGS__ };

#define GDEXTENSION_LITE_DEFINE_ARGS_VARIADIC(...) \
	const int _fixed_argc = GDEXTENSION_LITE_NARG(__VA_ARGS__); \
	const int _final_argc = _fixed_argc + argc; \
	GDExtensionConstTypePtr _args[_final_argc]; \
	__VA_OPT__(int _args_i = 0;) \
	GDEXTENSION_LITE_MAP(GDEXTENSION_LITE_SET_ARG, ##__VA_ARGS__) \
	for (int _i = 0; _i < argc; _i++) { \
		_args[_fixed_argc + _i] = argv[_i]; \
	}

#define GDEXTENSION_LITE_DEFINE_VARIANT_ARGS_VARIADIC(...) \
	const int _fixed_argc = GDEXTENSION_LITE_NARG(__VA_ARGS__); \
	const int _final_argc = _fixed_argc + argc; \
	GDExtensionConstVariantPtr _args[_final_argc]; \
	__VA_OPT__(int _args_i = 0;) \
	GDEXTENSION_LITE_MAP(GDEXTENSION_LITE_SET_VARIANT_ARG, ##__VA_ARGS__) \
	for (int _i = 0; _i < argc; _i++) { \
		_args[_fixed_argc + _i] = argv[_i]; \
	}

// Variant constructor/destructor
#define GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(return_type, placement_new, ...) \
	return_type _ret; \
	placement_new(&_ret, ##__VA_ARGS__); \
	return _ret;

#define GDEXTENSION_LITE_VARIANT_CONSTRUCTOR_IMPL(ctor_name, type, index, ...) \
	static GDExtensionPtrConstructor godot_ptr_##ctor_name = NULL; \
	if (godot_ptr_##ctor_name == NULL) { \
		godot_ptr_##ctor_name = godot_variant_get_ptr_constructor(type, index); \
	} \
	GDEXTENSION_LITE_DEFINE_ARGS(__VA_ARGS__) \
	godot_ptr_##ctor_name(self, _args);

#define GDEXTENSION_LITE_VARIANT_DESTRUCTOR_IMPL(cls, type) \
	static GDExtensionPtrDestructor godot_ptr_##cls##_destroy = NULL; \
	if (godot_ptr_##cls##_destroy == NULL) { \
		godot_ptr_##cls##_destroy = godot_variant_get_ptr_destructor(type); \
	} \
	godot_ptr_##cls##_destroy(self);

#define GDEXTENSION_LITE_VARIANT_FROM_TYPE_IMPL(cls, variant_type_enum, value) \
	static GDExtensionVariantFromTypeConstructorFunc _ctor = NULL; \
	if (_ctor == NULL) { \
		_ctor = godot_get_variant_from_type_constructor(variant_type_enum); \
	} \
	godot_Variant self; \
	_ctor(&self, (GDExtensionTypePtr) value); \
	return self;

#define GDEXTENSION_LITE_TYPE_FROM_VARIANT_IMPL(cls, variant_type_enum, value) \
	static GDExtensionTypeFromVariantConstructorFunc _ctor = NULL; \
	if (_ctor == NULL) { \
		_ctor = godot_get_variant_to_type_constructor(variant_type_enum); \
	} \
	godot_##cls self; \
	_ctor(&self, (GDExtensionVariantPtr) value); \
	return self;

// Variant members
#define GDEXTENSION_LITE_VARIANT_MEMBER_SET_IMPL(cls, variant_type_enum, type, member, value) \
	static GDExtensionPtrSetter godot_ptr_##cls##_set_##member = NULL; \
	if (godot_ptr_##cls##_set_##member == NULL) { \
		godot_StringName _member = godot_new_StringName_from_latin1_chars(#member); \
		godot_ptr_##cls##_set_##member = godot_variant_get_ptr_setter(variant_type_enum, &_member); \
		godot_StringName_destroy(&_member); \
	} \
	godot_ptr_##cls##_set_##member(self, value);

#define GDEXTENSION_LITE_VARIANT_MEMBER_GET_IMPL(cls, variant_type_enum, type, member) \
	static GDExtensionPtrGetter godot_ptr_##cls##_get_##member = NULL; \
	if (godot_ptr_##cls##_get_##member == NULL) { \
		godot_StringName _member = godot_new_StringName_from_latin1_chars(#member); \
		godot_ptr_##cls##_get_##member = godot_variant_get_ptr_getter(variant_type_enum, &_member); \
		godot_StringName_destroy(&_member); \
	} \
	godot_##type _value; \
	godot_ptr_##cls##_get_##member(self, &_value); \
	return _value;

// Variant methods
#define GDEXTENSION_LITE_DECLARE_VARIANT_METHOD(cls, method, hash, variant_type_enum) \
	static GDExtensionPtrBuiltInMethod godot_ptr_##cls##_##method = NULL; \
	if (godot_ptr_##cls##_##method == NULL) { \
		godot_StringName _method = godot_new_StringName_from_latin1_chars(#method); \
		godot_ptr_##cls##_##method = godot_variant_get_ptr_builtin_method(variant_type_enum, &_method, hash); \
		godot_StringName_destroy(&_method); \
	}

#define GDEXTENSION_LITE_VARIANT_METHOD_IMPL(cls, method, hash, variant_type_enum, return_type, self, ...) \
	GDEXTENSION_LITE_DECLARE_VARIANT_METHOD(cls, method, hash, variant_type_enum) \
	GDEXTENSION_LITE_DEFINE_ARGS(__VA_ARGS__) \
	return_type _ret; \
	godot_ptr_##cls##_##method((GDExtensionTypePtr) self, _args, &_ret, _final_argc); \
	return _ret;

#define GDEXTENSION_LITE_VARIANT_METHOD_IMPL_VARIADIC(cls, method, hash, variant_type_enum, return_type, self, ...) \
	GDEXTENSION_LITE_DECLARE_VARIANT_METHOD(cls, method, hash, variant_type_enum) \
	GDEXTENSION_LITE_DEFINE_ARGS_VARIADIC(__VA_ARGS__) \
	return_type _ret; \
	godot_ptr_##cls##_##method((GDExtensionTypePtr) self, _args, &_ret, _final_argc); \
	return _ret;

#define GDEXTENSION_LITE_VARIANT_METHOD_IMPL_VOID(cls, method, hash, variant_type_enum, return_type, self, ...) \
	GDEXTENSION_LITE_DECLARE_VARIANT_METHOD(cls, method, hash, variant_type_enum) \
	GDEXTENSION_LITE_DEFINE_ARGS(__VA_ARGS__) \
	godot_ptr_##cls##_##method((GDExtensionTypePtr) self, _args, NULL, _final_argc);

#define GDEXTENSION_LITE_VARIANT_METHOD_IMPL_VARIADIC_VOID(cls, method, hash, variant_type_enum, return_type, self, ...) \
	GDEXTENSION_LITE_DECLARE_VARIANT_METHOD(cls, method, hash, variant_type_enum) \
	GDEXTENSION_LITE_DEFINE_ARGS_VARIADIC(__VA_ARGS__) \
	godot_ptr_##cls##_##method((GDExtensionTypePtr) self, _args, NULL, _final_argc);

// Class methods
#define GDEXTENSION_LITE_DEFINE_CLASS_METHOD_BIND(cls, method, hash) \
	static GDExtensionMethodBindPtr godot_ptr_##cls##_##method = NULL; \
	if (godot_ptr_##cls##_##method == NULL) { \
		godot_StringName _class = godot_new_StringName_from_latin1_chars(#cls); \
		godot_StringName _method = godot_new_StringName_from_latin1_chars(#method); \
		godot_ptr_##cls##_##method = godot_classdb_get_method_bind(&_class, &_method, hash); \
		godot_StringName_destroy(&_method); \
		godot_StringName_destroy(&_class); \
	}

#define GDEXTENSION_LITE_METHOD_BIND_CALL_VARIADIC(cls, method, return_type, self) \
	return_type _ret; \
	godot_object_method_bind_call(godot_ptr_##cls##_##method, (GDExtensionObjectPtr) self, _args, &_ret); \
	return _ret

#define GDEXTENSION_LITE_CLASS_METHOD_IMPL(cls, method, hash, return_type, self, ...) \
	GDEXTENSION_LITE_DEFINE_CLASS_METHOD_BIND(cls, method, hash) \
	GDEXTENSION_LITE_DEFINE_ARGS(__VA_ARGS__) \
	return_type _ret; \
	godot_object_method_bind_ptrcall(godot_ptr_##cls##_##method, (GDExtensionObjectPtr) self, _args, &_ret); \
	return _ret;

#define GDEXTENSION_LITE_CLASS_METHOD_IMPL_VOID(cls, method, hash, return_type, self, ...) \
	GDEXTENSION_LITE_DEFINE_CLASS_METHOD_BIND(cls, method, hash) \
	GDEXTENSION_LITE_DEFINE_ARGS(__VA_ARGS__) \
	godot_object_method_bind_ptrcall(godot_ptr_##cls##_##method, (GDExtensionObjectPtr) self, _args, NULL);


#define GDEXTENSION_LITE_CLASS_METHOD_IMPL_VARIADIC(cls, method, hash, return_type, self, ...) \
	GDEXTENSION_LITE_DEFINE_CLASS_METHOD_BIND(cls, method, hash) \
	GDEXTENSION_LITE_DEFINE_VARIANT_ARGS_VARIADIC(__VA_ARGS__) \
	return_type _ret; \
	GDExtensionCallError _error; \
	godot_object_method_bind_call(godot_ptr_##cls##_##method, (GDExtensionObjectPtr) self, _args, _final_argc, &_ret, &_error); \
	return _ret;

#define GDEXTENSION_LITE_CLASS_METHOD_IMPL_VARIADIC_VOID(cls, method, hash, return_type, self, ...) \
	GDEXTENSION_LITE_DEFINE_CLASS_METHOD_BIND(cls, method, hash) \
	GDEXTENSION_LITE_DEFINE_VARIANT_ARGS_VARIADIC(__VA_ARGS__) \
	GDExtensionCallError _error; \
	godot_object_method_bind_call(godot_ptr_##cls##_##method, (GDExtensionObjectPtr) self, _args, _final_argc, NULL, &_error); \


// misc
#define GDEXTENSION_LITE_LAZY_INIT_VARIANT_INDEXING(get_or_set, indexed_or_keyed, name, type) \
	if (godot_ptr_##name##_##indexed_or_keyed##_##get_or_set == NULL) { \
		godot_ptr_##name##_##indexed_or_keyed##_##get_or_set = godot_variant_get_ptr_##indexed_or_keyed##_##get_or_set##ter(type); \
	}

#define GDEXTENSION_LITE_LAZY_INIT_VARIANT_OPERATOR(name, op, type1, type2) \
	if (godot_ptr_##name == NULL) { \
		godot_ptr_##name = godot_variant_get_ptr_operator_evaluator(op, type1, type2); \
	}

#define GDEXTENSION_LITE_LAZY_INIT_UTILITY_FUNCTION(name, hash) \
	if (godot_ptr_##name == NULL) { \
		godot_StringName _name = godot_new_StringName_from_latin1_chars(#name); \
		godot_ptr_##name = godot_variant_get_ptr_utility_function(&_name, hash); \
		godot_StringName_destroy(&_name); \
	}

// GDExtension API
#define GDEXTENSION_LITE_EXTENSION_INTERFACE_IMPL(symbol_type, symbol, ...) \
	static symbol_type godot_ptr_##symbol = NULL; \
	if (godot_ptr_##symbol == NULL) { \
		godot_ptr_##symbol = (symbol_type) gdextension_lite_get_proc_address(#symbol); \
	} \
	return godot_ptr_##symbol(__VA_ARGS__);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_IMPLEMENTATION_MACROS_H__
