#include "string.h"

#include "../implementation-macros.h"

#ifdef __cplusplus
extern "C" {
#endif

void godot_placement_new_String_from_latin1_chars(godot_String *self, const char *p_contents) {
	godot_string_new_with_latin1_chars(self, p_contents);
}

void godot_placement_new_String_from_utf8_chars(godot_String *self, const char *p_contents) {
	godot_string_new_with_utf8_chars(self, p_contents);
}

void godot_placement_new_String_from_utf16_chars(godot_String *self, const char16_t *p_contents) {
	godot_string_new_with_utf16_chars(self, p_contents);
}

void godot_placement_new_String_from_utf32_chars(godot_String *self, const char32_t *p_contents) {
	godot_string_new_with_utf32_chars(self, p_contents);
}

void godot_placement_new_String_from_wide_chars(godot_String *self, const wchar_t *p_contents) {
	godot_string_new_with_wide_chars(self, p_contents);
}

godot_String godot_new_String_from_latin1_chars(const char *p_contents) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_String, godot_placement_new_String_from_latin1_chars, p_contents);
}

godot_String godot_new_String_from_utf8_chars(const char *p_contents) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_String, godot_placement_new_String_from_utf8_chars, p_contents);
}

godot_String godot_new_String_from_utf16_chars(const char16_t *p_contents) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_String, godot_placement_new_String_from_utf16_chars, p_contents);
}

godot_String godot_new_String_from_utf32_chars(const char32_t *p_contents) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_String, godot_placement_new_String_from_utf32_chars, p_contents);
}

godot_String godot_new_String_from_wide_chars(const wchar_t *p_contents) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_String, godot_placement_new_String_from_wide_chars, p_contents);
}

void godot_placement_new_String_from_latin1_chars_and_len(godot_String *self, const char *p_contents, godot_int p_size) {
	godot_string_new_with_latin1_chars_and_len(self, p_contents, p_size);
}

void godot_placement_new_String_from_utf8_chars_and_len(godot_String *self, const char *p_contents, godot_int p_size) {
	godot_string_new_with_utf8_chars_and_len(self, p_contents, p_size);
}

void godot_placement_new_String_from_utf16_chars_and_len(godot_String *self, const char16_t *p_contents, godot_int p_size) {
	godot_string_new_with_utf16_chars_and_len(self, p_contents, p_size);
}

void godot_placement_new_String_from_utf32_chars_and_len(godot_String *self, const char32_t *p_contents, godot_int p_size) {
	godot_string_new_with_utf32_chars_and_len(self, p_contents, p_size);
}

void godot_placement_new_String_from_wide_chars_and_len(godot_String *self, const wchar_t *p_contents, godot_int p_size) {
	godot_string_new_with_wide_chars_and_len(self, p_contents, p_size);
}

godot_String godot_new_String_from_latin1_chars_and_len(const char *p_contents, GDExtensionInt p_size) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_String, godot_placement_new_String_from_latin1_chars_and_len, p_contents, p_size);
}

godot_String godot_new_String_from_utf8_chars_and_len(const char *p_contents, GDExtensionInt p_size) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_String, godot_placement_new_String_from_utf8_chars_and_len, p_contents, p_size);
}

godot_String godot_new_String_from_utf16_chars_and_len(const char16_t *p_contents, GDExtensionInt p_size) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_String, godot_placement_new_String_from_utf16_chars_and_len, p_contents, p_size);
}

godot_String godot_new_String_from_utf32_chars_and_len(const char32_t *p_contents, GDExtensionInt p_size) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_String, godot_placement_new_String_from_utf32_chars_and_len, p_contents, p_size);
}

godot_String godot_new_String_from_wide_chars_and_len(const wchar_t *p_contents, GDExtensionInt p_size) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_String, godot_placement_new_String_from_wide_chars_and_len, p_contents, p_size);
}

#ifdef __cplusplus
}
#endif
