#include "ledger.h"
#include <openssl/sha.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Function: compute_hash
// Input: string of event data+
// Output: SHA-256 hex string
char* compute_hash(const char* input)
{
    // 1. Allocate buffer for hash output.
    char* hash_str = malloc(65);
    // 2. Compute SHA256 digest.
    unsigned char digest[32];
    SHA256(input, strlen(input), digest);
    // 3. Convert digest bytes to hex string.
    for(int i = 0; i < 32; i ++)
    {
        sprintf(hash_str + (i * 2), "%02x", digest[i]);
    }
    hash_str[64] = '\0';
    printf("\n");
    // 4. Return pointer to hash string.
    return hash_str;
}

// Function: verify_hash
// Input: data string + target hash
// Output: 1 if identical, 0 otherwise
int verify_hash(const char* input, const char* target)
{
    // 1. Recompute hash using compute_hash().
    // 2. Compare it to the target hash.
    // 3. Return 1 if match, 0 if not.
}
