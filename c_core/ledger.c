#include "ledger.h"
#include <openssl/sha.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define HEX_SIZE 65
#define BIN_SIZE 32

// Function: compute_hash
// Input: string of event data+
// Output: SHA-256 hex string
char* compute_hash(const char* input)
{
    // 1. Allocate buffer for hash output.
    char* hash_output = malloc(HEX_SIZE);
    if(!hash_output)
    {
        return NULL;
    }
    // 2. Compute SHA256 digest.
    unsigned char digest[BIN_SIZE];
    SHA256(input, strlen(input), digest);
    // 3. Convert digest bytes to hex string.
    for(int i = 0; i < BIN_SIZE; i ++)
    {
        sprintf(hash_output + (i * 2), "%02x", digest[i]);
    }
    hash_output[64] = '\0';
    printf("\n");
    // 4. Return pointer to hash string.
    return hash_output;
}

// Function: verify_hash
// Input: data string + target hash
// Output: 1 if identical, 0 otherwise
int verify_hash(const char* input, const char* target)
{
    // 1. Recompute hash using compute_hash().
    char* hash_output = compute_hash(input);
    // 2. Compare it to the target hash.
    if(strcmp(hash_output, target) == 0)
    // 3. Return 1 if match, 0 if not.
    {
        free(hash_output);
        return 1;
    }
    else
    {
        free(hash_output);
        return 0;
    }
}
