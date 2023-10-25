/** @file
 * sizes.h -- Variant sizes
 */
#ifndef __GDEXTENSION_LITE_VARIANT_SIZES_H__
#define __GDEXTENSION_LITE_VARIANT_SIZES_H__

#include "../generated/variant/sizes.h"

#if __STDC_VERSION__ >= 201112L
	#include <assert.h>
	#define GDEXTENSION_LITE_ASSERT_SIZE(type) static_assert(sizeof(godot_##type) == GDEXTENSION_LITE_SIZE_##type, "Incompatible size for " #type);
#elif __cplusplus >= 201103L
	#define GDEXTENSION_LITE_ASSERT_SIZE(type) static_assert(sizeof(godot_##type) == GDEXTENSION_LITE_SIZE_##type, "Incompatible size for " #type);
#else
	#define GDEXTENSION_LITE_ASSERT_SIZE(type)
#endif

#endif  // __GDEXTENSION_LITE_VARIANT_SIZES_H__
