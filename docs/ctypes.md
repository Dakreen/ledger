### Notes — Calling C from Python with `ctypes`

1. **Compile C as a shared library**

   * `.so` on Linux
   * `.dll` on Windows
   * `.dylib` on macOS

   Example:

   ```bash
   gcc -shared -fPIC mylib.c -o libmylib.so
   ```

2. **Load the library in Python**

   ```python
   from ctypes import CDLL
   lib = CDLL("./libmylib.so")
   ```

3. **Define argument and return types**
   Prevents type errors and crashes:

   ```python
   from ctypes import c_int, c_char_p

   lib.add.argtypes = [c_int, c_int]
   lib.add.restype = c_int
   ```

4. **Call the function**

   ```python
   result = lib.add(5, 3)
   print(result)  # 8
   ```

5. **String handling**

   * C strings → `c_char_p`
   * Python `str` must be encoded → `b"hello"`
   * Convert back to string with `.decode()`

   ```python
   lib.compute.restype = c_char_p
   print(lib.compute(b"hello").decode())
   ```

6. **Memory ownership**

   * If C returns malloc’d memory → Python must free it (use a free() function in C)
   * Avoid leaks by designing APIs that return buffers owned by C or caller

7. **Error sources**

   * Wrong `argtypes` or `restype`
   * Passing Python objects without conversion
   * Missing or wrong library path

8. **When to use**

   * CPU-heavy code (hashing, cryptography)
   * Low-level memory/binary manipulation
   * Integrate existing C logic into Python apps

---

**Note: Using `c_void_p` in `ctypes` for Manual Memory Management**

---

### 1. Purpose

`c_void_p` represents a **raw C pointer** (`void *`) that Python does **not** copy or manage.
It is essential when you allocate memory in C (with `malloc`, `calloc`, or `realloc`) and need to free it explicitly.

---

### 2. Typical Pattern

**C code**

```c
#include <stdlib.h>
#include <string.h>

char* make_buffer(const char* msg) {
    char* buf = malloc(strlen(msg) + 1);
    strcpy(buf, msg);
    return buf;   // caller must free
}

void free_buffer(void* ptr) {
    free(ptr);
}
```

**Python code**

```python
from ctypes import CDLL, c_void_p, c_char_p, string_at

lib = CDLL("./libmylib.so")

# Configure types
lib.make_buffer.argtypes = [c_char_p]
lib.make_buffer.restype = c_void_p     # raw pointer, not copied
lib.free_buffer.argtypes = [c_void_p]
lib.free_buffer.restype = None

# Allocate and use
ptr = lib.make_buffer(b"hello")
data = string_at(ptr).decode()         # copy bytes from memory
print(data)

# Free safely on C side
lib.free_buffer(ptr)
```

---

### 3. Key Rules

1. `c_void_p` → Python holds the **actual C address**, not a copy.
2. You **must** call the C `free()` (via your `free_*` function) to avoid leaks.
3. Never call `free()` on a pointer Python created (e.g., `c_char_p` result).
4. Always pair memory allocation and freeing on the **same side** (C allocates → C frees).
5. Use `ctypes.string_at(ptr, size)` to safely read memory before freeing it.

---

### 4. Common Mistakes

| Mistake                                            | Result                  |
| -------------------------------------------------- | ----------------------- |
| Declaring `restype = c_char_p` but freeing pointer | `invalid pointer` crash |
| Freeing stack or static memory                     | Undefined behavior      |
| Forgetting to free after malloc                    | Memory leak             |

---

**Summary:**
Use `c_void_p` whenever you want Python to handle a **C-managed buffer** safely and release it later using your own C `free_*()` helper.


**Summary**

* `ctypes` bridges Python and C by mapping types and pointers safely.
* You load the shared library, set types, then call C like a normal function.
* Correct type declarations are essential for stability.
