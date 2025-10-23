### Pointer Arithmetic — Note

1. **Definition**
   Pointer arithmetic lets you move through contiguous memory such as arrays.

2. **Operations**

   * `p + n` → pointer advanced by `n × sizeof(*p)` bytes.
   * `p - n` → pointer moved back by `n × sizeof(*p)` bytes.
   * `*(p + n)` → value at element `n` ahead.
   * `&a[n]` ≡ `a + n`.

3. **Example**

   ```c
   int a[3] = {10, 20, 30};
   int *p = a;
   printf("%d\n", *(p + 1)); // prints 20
   ```

4. **Iteration**

   ```c
   for (int *p = a; p < a + 3; p++)
       printf("%d ", *p);
   ```

5. **Rules**

   * Arithmetic valid only within same array (or one past end).
   * Step size depends on data type.
   * Access outside array → undefined behavior.

6. **Summary**

   | Expression    | Meaning                   |
   | ------------- | ------------------------- |
   | `p + n`       | address n elements ahead  |
   | `p - n`       | address n elements before |
   | `*(p + n)`    | element n ahead           |
   | `p++` / `p--` | move pointer one element  |
