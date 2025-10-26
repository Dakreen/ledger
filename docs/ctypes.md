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

**Summary**

* `ctypes` bridges Python and C by mapping types and pointers safely.
* You load the shared library, set types, then call C like a normal function.
* Correct type declarations are essential for stability.
