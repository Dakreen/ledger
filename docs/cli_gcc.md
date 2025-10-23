### Notes — GCC Compilation Commands

#### 1. **Basic build**

```bash
gcc file.c -o program
```

Compiles normally, no debug info, smallest binary.

#### 2. **With debugger symbols**

```bash
gcc -g file.c -o program
```

Adds debug symbols for **gdb** or VS Code.
→ Enables breakpoints and variable inspection.

#### 3. **With warnings**

```bash
gcc -g -Wall file.c -o program
```

Adds all standard warnings (`-Wall`) + debug info.
Best default for development.

#### 4. **Static build**

```bash
gcc -static file.c -o program
```

Links all libraries directly into the binary.
→ No external `.so` dependencies.
→ Bigger file, portable on systems without shared libs.

#### 5. **Shared (dynamic) build**

```bash
gcc -fPIC -shared file.c -o libname.so
```

Creates a **shared library** (`.so`).
Used for modular projects and linking across programs.

#### 6. **Compile + link manually**

```bash
gcc -c file.c    # produce object file file.o
gcc file.o -o program
```

Useful for multi-file builds.

#### Summary Table

| Purpose          | Command                              | Output         |
| ---------------- | ------------------------------------ | -------------- |
| Normal           | `gcc file.c -o program`              | Fast, no debug |
| Debug            | `gcc -g file.c -o program`           | Debuggable     |
| Debug + warnings | `gcc -g -Wall file.c -o program`     | Recommended    |
| Static binary    | `gcc -static file.c -o program`      | Self-contained |
| Shared library   | `gcc -fPIC -shared file.c -o lib.so` | Reusable `.so` |
