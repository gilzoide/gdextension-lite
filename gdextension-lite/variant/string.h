/** @file
 * string.h -- Godot String type
 */
#ifndef __GDEXTENSION_LITE_STRING_H__
#define __GDEXTENSION_LITE_STRING_H__

#include "int.h"
#include "sizes.h"
#include "../definition-macros.h"

typedef struct godot_String {
	uint8_t _[GDEXTENSION_LITE_SIZE_String];
} godot_String;

GDEXTENSION_LITE_ASSERT_SIZE(String)

#ifdef __cplusplus
extern "C" {
#endif

GDEXTENSION_LITE_DECL godot_String godot_new_String_from_latin1_chars(const char *p_contents);
GDEXTENSION_LITE_DECL godot_String godot_new_String_from_utf8_chars(const char *p_contents);
GDEXTENSION_LITE_DECL godot_String godot_new_String_from_utf16_chars(const char16_t *p_contents);
GDEXTENSION_LITE_DECL godot_String godot_new_String_from_utf32_chars(const char32_t *p_contents);
GDEXTENSION_LITE_DECL godot_String godot_new_String_from_wide_chars(const wchar_t *p_contents);
GDEXTENSION_LITE_DECL void godot_placement_new_String_from_latin1_chars(godot_String *self, const char *p_contents);
GDEXTENSION_LITE_DECL void godot_placement_new_String_from_utf8_chars(godot_String *self, const char *p_contents);
GDEXTENSION_LITE_DECL void godot_placement_new_String_from_utf16_chars(godot_String *self, const char16_t *p_contents);
GDEXTENSION_LITE_DECL void godot_placement_new_String_from_utf32_chars(godot_String *self, const char32_t *p_contents);
GDEXTENSION_LITE_DECL void godot_placement_new_String_from_wide_chars(godot_String *self, const wchar_t *p_contents);

GDEXTENSION_LITE_DECL godot_String godot_new_String_from_latin1_chars_and_len(const char *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL godot_String godot_new_String_from_utf8_chars_and_len(const char *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL godot_String godot_new_String_from_utf16_chars_and_len(const char16_t *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL godot_String godot_new_String_from_utf32_chars_and_len(const char32_t *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL godot_String godot_new_String_from_wide_chars_and_len(const wchar_t *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL void godot_placement_new_String_from_latin1_chars_and_len(godot_String *self, const char *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL void godot_placement_new_String_from_utf8_chars_and_len(godot_String *self, const char *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL void godot_placement_new_String_from_utf16_chars_and_len(godot_String *self, const char16_t *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL void godot_placement_new_String_from_utf32_chars_and_len(godot_String *self, const char32_t *p_contents, godot_int p_size);
GDEXTENSION_LITE_DECL void godot_placement_new_String_from_wide_chars_and_len(godot_String *self, const wchar_t *p_contents, godot_int p_size);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_STRING_H__
