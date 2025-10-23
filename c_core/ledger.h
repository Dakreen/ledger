#ifndef LEDGER_H
#define LEDGER_H

#include<stdlib.h>
#include<string.h>

// Function prototypes
char* compute_hash(const char* input);
int verify_hash(const char* input, const char* target);

#endif
