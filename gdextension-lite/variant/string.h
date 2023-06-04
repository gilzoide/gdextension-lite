/** @file
 * string.h -- Godot String type
 */
#ifndef __GDEXTENSION_LITE_STRING_H__
#define __GDEXTENSION_LITE_STRING_H__

#include <stdint.h>

#include "../gdextension-interface.h"

typedef struct godot_String {
	uint8_t _[sizeof(void *)];
} godot_String;

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

#endif  // __GDEXTENSION_LITE_STRING_H__

#ifdef GDEXTENSION_LITE_IMPLEMENTATION

godot_String godot_new_String_from_latin1_chars(const char *p_contents) {
	godot_String self;
	godot_interface->string_new_with_latin1_chars(&self, p_contents);
	return self;
}

godot_String godot_new_String_from_utf8_chars(const char *p_contents) {
	godot_String self;
	godot_interface->string_new_with_utf8_chars(&self, p_contents);
	return self;
}

godot_String godot_new_String_from_utf16_chars(const char16_t *p_contents) {
	godot_String self;
	godot_interface->string_new_with_utf16_chars(&self, p_contents);
	return self;
}

godot_String godot_new_String_from_utf32_chars(const char32_t *p_contents) {
	godot_String self;
	godot_interface->string_new_with_utf32_chars(&self, p_contents);
	return self;
}

godot_String godot_new_String_from_wide_chars(const wchar_t *p_contents) {
	godot_String self;
	godot_interface->string_new_with_wide_chars(&self, p_contents);
	return self;
}

godot_String godot_new_String_from_latin1_chars_and_len(const char *p_contents, GDExtensionInt p_size) {
	godot_String self;
	godot_interface->string_new_with_latin1_chars_and_len(&self, p_contents, p_size);
	return self;
}

godot_String godot_new_String_from_utf8_chars_and_len(const char *p_contents, GDExtensionInt p_size) {
	godot_String self;
	godot_interface->string_new_with_utf8_chars_and_len(&self, p_contents, p_size);
	return self;
}

godot_String godot_new_String_from_utf16_chars_and_len(const char16_t *p_contents, GDExtensionInt p_size) {
	godot_String self;
	godot_interface->string_new_with_utf16_chars_and_len(&self, p_contents, p_size);
	return self;
}

godot_String godot_new_String_from_utf32_chars_and_len(const char32_t *p_contents, GDExtensionInt p_size) {
	godot_String self;
	godot_interface->string_new_with_utf32_chars_and_len(&self, p_contents, p_size);
	return self;
}

godot_String godot_new_String_from_wide_chars_and_len(const wchar_t *p_contents, GDExtensionInt p_size) {
	godot_String self;
	godot_interface->string_new_with_wide_chars_and_len(&self, p_contents, p_size);
	return self;
}

#endif
