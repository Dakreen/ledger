### Note — `sprintf()` for Binary-to-Hex Conversion

1. **Purpose**
   `sprintf()` formats binary byte values into readable hexadecimal text.
   Each byte (0–255) becomes two printable characters (`00`–`ff`).

2. **Syntax**

   ```c
   int sprintf(char *str, const char *format, ...);
   ```

   * Writes formatted data into the string `str`.
   * Returns number of characters written (excluding `'\0'`).

3. **Typical Pattern**

   ```c
   for (size_t i = 0; i < len; i++)
       sprintf(hex + (i * 2), "%02x", bin[i]);
   hex[len * 2] = '\0';
   ```

   * `"%02x"` → print as 2-digit lowercase hex, pad with `0` if needed.
   * `hex + (i * 2)` → start writing 2 characters at offset `i*2`.
   * `bin[i]` → current byte value.

4. **Example**

   ```c
   unsigned char data[] = {0xde, 0xad, 0xbe, 0xef};
   char hex[9];
   for (size_t i = 0; i < 4; i++)
       sprintf(hex + (i * 2), "%02x", data[i]);
   hex[8] = '\0';
   printf("%s\n", hex); // Output: deadbeef
   ```

5. **Explanation**

   | Binary byte | sprintf() output | Hex string indices |
   | ----------- | ---------------- | ------------------ |
   | `0xde`      | `"de"`           | `[0] [1]`          |
   | `0xad`      | `"ad"`           | `[2] [3]`          |
   | `0xbe`      | `"be"`           | `[4] [5]`          |
   | `0xef`      | `"ef"`           | `[6] [7]`          |

6. **Result**
   Binary (4 bytes) → Hex string (8 chars + null terminator).
   Output is readable and safe for printing or file storage.
