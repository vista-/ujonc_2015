// ARC42 encryption v3

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

// Original ARC4 implementation:
// Brad Conte (brad AT bradconte.com)
// https://github.com/B-Con/crypto-algorithms/blob/master/arcfour.c
void arcfour_key_setup(unsigned char state[], const unsigned char key[], int len)
{
    int i, j;
    unsigned char t;

    for (i = 0; i < 256; ++i) {
        state[i] = i;
    }
    for (i = 0, j = 0; i < 256; ++i) {
        j = (j + state[i] + key[i % len]) % 256;
        j = (j + 1) % 256; // <- this the ARC42 magic
        t = state[i];
        state[i] = state[j];
        state[j] = t;
    }
}

int i = 0, j = 0;

void arcfour_generate_stream(unsigned char state[], unsigned char out[], size_t len)
{
    size_t idx;
    unsigned char t;

    for (idx = 0; idx < len; ++idx)  {
        i = (i + 1) % 256;
        j = (j + state[i]) % 256;
        t = state[i];
        state[i] = state[j];
        state[j] = t;
        out[idx] = state[(state[i] + state[j]) % 256];
    }
}

int file_exist(char* file) {
    char command[100];
    strcpy(command, "test -e ");
    strcpy(command + strlen(command), file);
    return !system(command);
}

int main(int argc, char **argv) {
    unsigned char buffer[101];
    unsigned char state[256];
    char* key = argv[1];

    // Checking license
    if (!file_exist("/etc/arc42_license")) {
        fprintf(stderr, "Sorry, your ARC42 copy is not licensed. :'(\n");
        return 1;
    }

    // Checking the key argument
    if (argc < 2) {
        fprintf(stderr, "Please provide a key as argument.\n");
        return 2;
    }
    if (strlen(key) > 255) {
        fprintf(stderr, "The key is too long. Maximum size is 255 characters.\n");
        return 3;
    }

    // Initialization
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    arcfour_key_setup(state, (unsigned char*)key, strlen(key));
    while (*key) *(key++) = 0;

    // Encryption
    int i, j, c = 0;
    while (c != -1) {
        // Read in max. 100 bytes
        for (i = 0; i < 100 && ((c = getchar()) != -1); i++) {
            buffer[i] = c;
        }

        // Encrypt the buffer
        for (j = 0; j < i; j++) {
            unsigned char xor;
            arcfour_generate_stream(state, &xor, 1);
            buffer[j] ^= xor;
        }

        // Print out the encrypted data
        buffer[j] = 0;
        printf((char*)buffer);
    }

    return 0;
}

