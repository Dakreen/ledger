#include "ledger.h"
#include <openssl/sha.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define HEX_SIZE 65
#define BIN_SIZE 32

char* compute_hash(const char* input)
{
    // Allocate buffer for hash output.
    char* hash_output = malloc(HEX_SIZE);
    if(!hash_output)
    {
        return NULL;
    }
    // Compute SHA256 digest.
    unsigned char digest[BIN_SIZE];
    SHA256(input, strlen(input), digest);
    // Convert digest bytes to hex string.
    for(int i = 0; i < BIN_SIZE; i ++)
    {
        sprintf(hash_output + (i * 2), "%02x", digest[i]);
    }
    hash_output[64] = '\0';
    printf("\n");
    
    return hash_output;
}

int verify_hash(const char* input, const char* target)
{
    // Recompute hash using compute_hash().
    char* hash_output = compute_hash(input);
    // Compare it to the target hash.
    if(strcmp(hash_output, target) == 0)
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

void free_buffer(char* buffer)
{
    free(buffer);
}

// For unit test only
/* int main()
{

    return 0;
} */
