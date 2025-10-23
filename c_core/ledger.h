#ifndef LEDGER_H
#define LEDGER_H

// Function prototypes
char* compute_hash(const char* input);
int verify_hash(const char* input, const char* target);

#endif
