// ARC42 encryption v1

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

int main(int argc, char **argv) {
    unsigned char key[256];
    unsigned char text[256];
    unsigned char state[256];
    size_t key_length;
    size_t text_length;

    // Preparing the key and the text
    if (argc < 3) {
        fprintf(stderr, "Please provide a key as the first argument and a text to encrypt as the second argument.\n");
        return 1;
    }
    key_length = strlen(argv[1]);
    if (key_length > 255) {
        fprintf(stderr, "The key is too long. Maximum size is 255 characters.\n");
        return 2;
    }
    text_length = strlen(argv[2]);
    if (text_length > 255) {
        fprintf(stderr, "The text is too long. Maximum size is 255 characters.\n");
        return 3;
    }
    strcpy((char*)key, argv[1]);
    strcpy((char*)text, argv[2]);

    // Initialization
    fprintf(stderr, "Initializing state...\n");
    arcfour_key_setup(state, key, key_length);
    fprintf(stderr, "Initialization complete\n");

    // Encryption
    fprintf(stderr, "Encrypting text: ");
    fprintf(stderr, (char*)text);
    fprintf(stderr, "\n");
    for (int i = 0; i < text_length; i++) {
        unsigned char xor;
        arcfour_generate_stream(state, &xor, 1);
        text[i] ^= xor;
    }
    fprintf(stderr, "Encryption complete\n");

    // Printing output
    for (int j = 0; j < text_length; j++) {
        fprintf(stdout, "%02X", text[j]);
    }
    fprintf(stdout, "\n");

    return 0;
}

