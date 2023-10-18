#include "gdextension-lite.h"

#ifdef __cplusplus
extern "C" {
#endif

void gdextension_lite_initialize(const GDExtensionInterfaceGetProcAddress get_proc_address) {
	gdextension_lite_initialize_interface(get_proc_address);
}

#ifdef __cplusplus
}
#endif
