/** @file
 * gdextension-lite.h -- GDExtension Lite entrypoint, includes every other file
 */
#ifndef __GDEXTENSION_LITE_H__
#define __GDEXTENSION_LITE_H__

#include "definition-macros.h"
#include "generated/extension_interface.h"
#include "generated/global_enums.h"
#include "generated/native_structures.h"
#include "generated/utility_functions.h"
#include "generated/class-stubs/all.h"
#include "generated/class-methods/all.h"
#include "generated/singletons.h"
#include "generated/variant/all.h"
#include "variant/all.h"

#ifdef __cplusplus
extern "C" {
#endif

GDEXTENSION_LITE_DECL void gdextension_lite_initialize(const GDExtensionInterfaceGetProcAddress get_proc_address);

#ifdef __cplusplus
}
#endif

#endif  // __GDEXTENSION_LITE_H__
