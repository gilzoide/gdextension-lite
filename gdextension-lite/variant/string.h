/** @file
 * string.h -- Godot String type
 */
#ifndef __GDEXTENSION_LITE_STRING_H__
#define __GDEXTENSION_LITE_STRING_H__

#include <stdint.h>

#include "../generated/extension_interface.h"

typedef struct godot_String {
	uint8_t _[sizeof(void *)];
} godot_String;

#ifdef __cplusplus
extern "C" {
#endif

godot_String godot_new_String_from_latin1_chars(const char *p_contents);
godot_String godot_new_String_from_utf8_chars(const char *p_contents);
godot_String godot_new_String_from_utf16_chars(const char16_t *p_contents);
godot_String godot_new_String_from_utf32_chars(const char32_t *p_contents);
godot_String godot_new_String_from_wide_chars(const wchar_t *p_contents);

godot_String godot_new_String_from_latin1_chars_and_len(const char *p_contents, GDExtensionInt p_size);
godot_String godot_new_String_from_utf8_chars_and_len(const char *p_contents, GDExtensionInt p_size);
godot_String godot_new_String_from_utf16_chars_and_len(const char16_t *p_contents, GDExtensionInt p_size);
godot_String godot_new_String_from_utf32_chars_and_len(const char32_t *p_contents, GDExtensionInt p_size);
godot_String godot_new_String_from_wide_chars_and_len(const wchar_t *p_contents, GDExtensionInt p_size);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_STRING_H__  // __GDEXTENSION_LITE_STRING_H__

#ifdef GDEXTENSION_LITE_IMPLEMENTATION
#ifndef __GDEXTENSION_LITE_STRING_H_IMPLEMENTATION__
#define __GDEXTENSION_LITE_STRING_H_IMPLEMENTATION__

#ifdef __cplusplus
extern "C" {
#endif

godot_String godot_new_String_from_latin1_chars(const char *p_contents) {
	godot_String self;
	godot_string_new_with_latin1_chars(&self, p_contents);
	return self;
}

godot_String godot_new_String_from_utf8_chars(const char *p_contents) {
	godot_String self;
	godot_string_new_with_utf8_chars(&self, p_contents);
	return self;
}

godot_String godot_new_String_from_utf16_chars(const char16_t *p_contents) {
	godot_String self;
	godot_string_new_with_utf16_chars(&self, p_contents);
	return self;
}

godot_String godot_new_String_from_utf32_chars(const char32_t *p_contents) {
	godot_String self;
	godot_string_new_with_utf32_chars(&self, p_contents);
	return self;
}

godot_String godot_new_String_from_wide_chars(const wchar_t *p_contents) {
	godot_String self;
	godot_string_new_with_wide_chars(&self, p_contents);
	return self;
}

godot_String godot_new_String_from_latin1_chars_and_len(const char *p_contents, GDExtensionInt p_size) {
	godot_String self;
	godot_string_new_with_latin1_chars_and_len(&self, p_contents, p_size);
	return self;
}

godot_String godot_new_String_from_utf8_chars_and_len(const char *p_contents, GDExtensionInt p_size) {
	godot_String self;
	godot_string_new_with_utf8_chars_and_len(&self, p_contents, p_size);
	return self;
}

godot_String godot_new_String_from_utf16_chars_and_len(const char16_t *p_contents, GDExtensionInt p_size) {
	godot_String self;
	godot_string_new_with_utf16_chars_and_len(&self, p_contents, p_size);
	return self;
}

godot_String godot_new_String_from_utf32_chars_and_len(const char32_t *p_contents, GDExtensionInt p_size) {
	godot_String self;
	godot_string_new_with_utf32_chars_and_len(&self, p_contents, p_size);
	return self;
}

godot_String godot_new_String_from_wide_chars_and_len(const wchar_t *p_contents, GDExtensionInt p_size) {
	godot_String self;
	godot_string_new_with_wide_chars_and_len(&self, p_contents, p_size);
	return self;
}

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_STRING_H_IMPLEMENTATION__
#endif  // GDEXTENSION_LITE_IMPLEMENTATION
