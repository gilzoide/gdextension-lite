#include "string_name.h"

#include "string.h"
#include "../implementation-macros.h"

#ifdef __cplusplus
extern "C" {
#endif

void godot_String_destroy(godot_String *self);
void godot_placement_new_StringName_from_String(godot_StringName *self, const godot_String *from);

void godot_placement_new_StringName_from_latin1_chars(godot_StringName *self, const char *p_contents) {
	godot_String str = godot_new_String_from_latin1_chars(p_contents);
	godot_placement_new_StringName_from_String(self, &str);
	godot_String_destroy(&str);
}

void godot_placement_new_StringName_from_utf8_chars(godot_StringName *self, const char *p_contents) {
	godot_String str = godot_new_String_from_utf8_chars(p_contents);
	godot_placement_new_StringName_from_String(self, &str);
	godot_String_destroy(&str);
}

void godot_placement_new_StringName_from_utf16_chars(godot_StringName *self, const char16_t *p_contents) {
	godot_String str = godot_new_String_from_utf16_chars(p_contents);
	godot_placement_new_StringName_from_String(self, &str);
	godot_String_destroy(&str);
}

void godot_placement_new_StringName_from_utf32_chars(godot_StringName *self, const char32_t *p_contents) {
	godot_String str = godot_new_String_from_utf32_chars(p_contents);
	godot_placement_new_StringName_from_String(self, &str);
	godot_String_destroy(&str);
}

void godot_placement_new_StringName_from_wide_chars(godot_StringName *self, const wchar_t *p_contents) {
	godot_String str = godot_new_String_from_wide_chars(p_contents);
	godot_placement_new_StringName_from_String(self, &str);
	godot_String_destroy(&str);
}

godot_StringName godot_new_StringName_from_latin1_chars(const char *p_contents) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_StringName, godot_placement_new_StringName_from_latin1_chars, p_contents);
}

godot_StringName godot_new_StringName_from_utf8_chars(const char *p_contents) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_StringName, godot_placement_new_StringName_from_utf8_chars, p_contents);
}

godot_StringName godot_new_StringName_from_utf16_chars(const char16_t *p_contents) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_StringName, godot_placement_new_StringName_from_utf16_chars, p_contents);
}

godot_StringName godot_new_StringName_from_utf32_chars(const char32_t *p_contents) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_StringName, godot_placement_new_StringName_from_utf32_chars, p_contents);
}

godot_StringName godot_new_StringName_from_wide_chars(const wchar_t *p_contents) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_StringName, godot_placement_new_StringName_from_wide_chars, p_contents);
}

void godot_placement_new_StringName_from_latin1_chars_and_len(godot_StringName *self, const char *p_contents, godot_int p_size) {
	godot_String str = godot_new_String_from_latin1_chars_and_len(p_contents, p_size);
	godot_placement_new_StringName_from_String(self, &str);
	godot_String_destroy(&str);
}

void godot_placement_new_StringName_from_utf8_chars_and_len(godot_StringName *self, const char *p_contents, godot_int p_size) {
	godot_String str = godot_new_String_from_utf8_chars_and_len(p_contents, p_size);
	godot_placement_new_StringName_from_String(self, &str);
	godot_String_destroy(&str);
}

void godot_placement_new_StringName_from_utf16_chars_and_len(godot_StringName *self, const char16_t *p_contents, godot_int p_size) {
	godot_String str = godot_new_String_from_utf16_chars_and_len(p_contents, p_size);
	godot_placement_new_StringName_from_String(self, &str);
	godot_String_destroy(&str);
}

void godot_placement_new_StringName_from_utf32_chars_and_len(godot_StringName *self, const char32_t *p_contents, godot_int p_size) {
	godot_String str = godot_new_String_from_utf32_chars_and_len(p_contents, p_size);
	godot_placement_new_StringName_from_String(self, &str);
	godot_String_destroy(&str);
}

void godot_placement_new_StringName_from_wide_chars_and_len(godot_StringName *self, const wchar_t *p_contents, godot_int p_size) {
	godot_String str = godot_new_String_from_wide_chars_and_len(p_contents, p_size);
	godot_placement_new_StringName_from_String(self, &str);
	godot_String_destroy(&str);
}

godot_StringName godot_new_StringName_from_latin1_chars_and_len(const char *p_contents, godot_int p_size) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_StringName, godot_placement_new_StringName_from_latin1_chars_and_len, p_contents, p_size);
}

godot_StringName godot_new_StringName_from_utf8_chars_and_len(const char *p_contents, godot_int p_size) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_StringName, godot_placement_new_StringName_from_utf8_chars_and_len, p_contents, p_size);
}

godot_StringName godot_new_StringName_from_utf16_chars_and_len(const char16_t *p_contents, godot_int p_size) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_StringName, godot_placement_new_StringName_from_utf16_chars_and_len, p_contents, p_size);
}

godot_StringName godot_new_StringName_from_utf32_chars_and_len(const char32_t *p_contents, godot_int p_size) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_StringName, godot_placement_new_StringName_from_utf32_chars_and_len, p_contents, p_size);
}

godot_StringName godot_new_StringName_from_wide_chars_and_len(const wchar_t *p_contents, godot_int p_size) {
	GDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_StringName, godot_placement_new_StringName_from_wide_chars_and_len, p_contents, p_size);
}

#ifdef __cplusplus
}
#endif
