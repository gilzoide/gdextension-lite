/** @file
 * string_name.h -- Godot StringName type
 */
#ifndef __GDEXTENSION_LITE_STRING_NAME_H__
#define __GDEXTENSION_LITE_STRING_NAME_H__

#include "int.h"
#include "sizes.h"
#include "../definition-macros.h"

typedef struct godot_StringName {
	uint8_t _[GDEXTENSION_LITE_SIZE_StringName];
} godot_StringName;

GDEXTENSION_LITE_ASSERT_SIZE(StringName)

#ifdef __cplusplus
extern "C" {
#endif

GDEXTENSION_LITE_DECL godot_StringName godot_new_StringName_from_latin1_chars(const char *p_contents);
GDEXTENSION_LITE_DECL godot_StringName godot_new_StringName_from_utf8_chars(const char *p_contents);
GDEXTENSION_LITE_DECL godot_StringName godot_new_StringName_from_utf16_chars(const char16_t *p_contents);
GDEXTENSION_LITE_DECL godot_StringName godot_new_StringName_from_utf32_chars(const char32_t *p_contents);
GDEXTENSION_LITE_DECL godot_StringName godot_new_StringName_from_wide_chars(const wchar_t *p_contents);
GDEXTENSION_LITE_DECL void godot_placement_new_StringName_from_latin1_chars(godot_StringName *self, const char *p_contents);
GDEXTENSION_LITE_DECL void godot_placement_new_StringName_from_utf8_chars(godot_StringName *self, const char *p_contents);
GDEXTENSION_LITE_DECL void godot_placement_new_StringName_from_utf16_chars(godot_StringName *self, const char16_t *p_contents);
GDEXTENSION_LITE_DECL void godot_placement_new_StringName_from_utf32_chars(godot_StringName *self, const char32_t *p_contents);
GDEXTENSION_LITE_DECL void godot_placement_new_StringName_from_wide_chars(godot_StringName *self, const wchar_t *p_contents);

GDEXTENSION_LITE_DECL godot_StringName godot_new_StringName_from_latin1_chars_and_len(const char *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL godot_StringName godot_new_StringName_from_utf8_chars_and_len(const char *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL godot_StringName godot_new_StringName_from_utf16_chars_and_len(const char16_t *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL godot_StringName godot_new_StringName_from_utf32_chars_and_len(const char32_t *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL godot_StringName godot_new_StringName_from_wide_chars_and_len(const wchar_t *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL void godot_placement_new_StringName_from_latin1_chars_and_len(godot_StringName *self, const char *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL void godot_placement_new_StringName_from_utf8_chars_and_len(godot_StringName *self, const char *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL void godot_placement_new_StringName_from_utf16_chars_and_len(godot_StringName *self, const char16_t *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL void godot_placement_new_StringName_from_utf32_chars_and_len(godot_StringName *self, const char32_t *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL void godot_placement_new_StringName_from_wide_chars_and_len(godot_StringName *self, const wchar_t *p_contents, godot_int p_size);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_STRING_NAME_H__
