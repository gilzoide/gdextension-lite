/** @file
 * string_name.h -- Godot StringName type
 */
#ifndef __GDEXTENSION_LITE_STRING_NAME_H__
#define __GDEXTENSION_LITE_STRING_NAME_H__

#include <stdint.h>

#include "string.h"

typedef struct godot_StringName {
	uint8_t _[sizeof(void *)];
} godot_StringName;

godot_StringName godot_new_StringName_from_latin1_chars(const char *p_contents);
godot_StringName godot_new_StringName_from_utf8_chars(const char *p_contents);
godot_StringName godot_new_StringName_from_utf16_chars(const char16_t *p_contents);
godot_StringName godot_new_StringName_from_utf32_chars(const char32_t *p_contents);
godot_StringName godot_new_StringName_from_wide_chars(const wchar_t *p_contents);

godot_StringName godot_new_StringName_from_latin1_chars_and_len(const char *p_contents, GDExtensionInt p_size);
godot_StringName godot_new_StringName_from_utf8_chars_and_len(const char *p_contents, GDExtensionInt p_size);
godot_StringName godot_new_StringName_from_utf16_chars_and_len(const char16_t *p_contents, GDExtensionInt p_size);
godot_StringName godot_new_StringName_from_utf32_chars_and_len(const char32_t *p_contents, GDExtensionInt p_size);
godot_StringName godot_new_StringName_from_wide_chars_and_len(const wchar_t *p_contents, GDExtensionInt p_size);

void godot_destroy_StringName(godot_StringName *self);
#define GDEXTENSION_LITE_WITH_STRING_NAME(name, body) \
	{ \
		godot_StringName name = godot_new_StringName_from_latin1_chars(#name); \
		body \
		godot_destroy_StringName(&name); \
	}

#endif  // __GDEXTENSION_LITE_STRING_NAME_H__

#ifdef GDEXTENSION_LITE_IMPLEMENTATION
#ifndef __GDEXTENSION_LITE_STRING_NAME_H_IMPLEMENTATION__
#define __GDEXTENSION_LITE_STRING_NAME_H_IMPLEMENTATION__

void godot_destroy_String(godot_String *self);
godot_StringName godot_new_StringName_from_String(const godot_String *from);

godot_StringName godot_new_StringName_from_latin1_chars(const char *p_contents) {
	godot_String str = godot_new_String_from_latin1_chars(p_contents);
	godot_StringName self = godot_new_StringName_from_String(&str);
	godot_destroy_String(&str);
	return self;
}

godot_StringName godot_new_StringName_from_utf8_chars(const char *p_contents) {
	godot_String str = godot_new_String_from_utf8_chars(p_contents);
	godot_StringName self = godot_new_StringName_from_String(&str);
	godot_destroy_String(&str);
	return self;
}

godot_StringName godot_new_StringName_from_utf16_chars(const char16_t *p_contents) {
	godot_String str = godot_new_String_from_utf16_chars(p_contents);
	godot_StringName self = godot_new_StringName_from_String(&str);
	godot_destroy_String(&str);
	return self;
}

godot_StringName godot_new_StringName_from_utf32_chars(const char32_t *p_contents) {
	godot_String str = godot_new_String_from_utf32_chars(p_contents);
	godot_StringName self = godot_new_StringName_from_String(&str);
	godot_destroy_String(&str);
	return self;
}

godot_StringName godot_new_StringName_from_wide_chars(const wchar_t *p_contents) {
	godot_String str = godot_new_String_from_wide_chars(p_contents);
	godot_StringName self = godot_new_StringName_from_String(&str);
	godot_destroy_String(&str);
	return self;
}

godot_StringName godot_new_StringName_from_latin1_chars_and_len(const char *p_contents, GDExtensionInt p_size) {
	godot_String str = godot_new_String_from_latin1_chars_and_len(p_contents, p_size);
	godot_StringName self = godot_new_StringName_from_String(&str);
	godot_destroy_String(&str);
	return self;
}

godot_StringName godot_new_StringName_from_utf8_chars_and_len(const char *p_contents, GDExtensionInt p_size) {
	godot_String str = godot_new_String_from_utf8_chars_and_len(p_contents, p_size);
	godot_StringName self = godot_new_StringName_from_String(&str);
	godot_destroy_String(&str);
	return self;
}

godot_StringName godot_new_StringName_from_utf16_chars_and_len(const char16_t *p_contents, GDExtensionInt p_size) {
	godot_String str = godot_new_String_from_utf16_chars_and_len(p_contents, p_size);
	godot_StringName self = godot_new_StringName_from_String(&str);
	godot_destroy_String(&str);
	return self;
}

godot_StringName godot_new_StringName_from_utf32_chars_and_len(const char32_t *p_contents, GDExtensionInt p_size) {
	godot_String str = godot_new_String_from_utf32_chars_and_len(p_contents, p_size);
	godot_StringName self = godot_new_StringName_from_String(&str);
	godot_destroy_String(&str);
	return self;
}

godot_StringName godot_new_StringName_from_wide_chars_and_len(const wchar_t *p_contents, GDExtensionInt p_size) {
	godot_String str = godot_new_String_from_wide_chars_and_len(p_contents, p_size);
	godot_StringName self = godot_new_StringName_from_String(&str);
	godot_destroy_String(&str);
	return self;
}

#endif  // __GDEXTENSION_LITE_STRING_NAME_H_IMPLEMENTATION__
#endif  // GDEXTENSION_LITE_IMPLEMENTATION
