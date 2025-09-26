#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int only_digits(string s);
char rotate(char c, int k);

int main(int argc, string argv[])
{
    if (argc != 2 || !only_digits(argv[1])) // program name and +1 key
    {
        printf("UsageL ./caesar key\n");
        return 1;
    }

    int key = atoi(argv[1]); // atoi converts string to int so "13" becomes 13
    string p = get_string("plaintext:  ");

    printf("ciphertext: ");
    for (int i = 0; i < strlen(p); i = i + 1)
    {
        printf("%c", rotate(p[i], key));
    }
    printf("\n");
    return 0;
}

int only_digits(string s)
{
    if (s[0] == '\0')
        return 0;
    for (int i = 0; s[i] != '\0'; i = i + 1)
    {
        if (!isdigit(s[i]))
            return 0;
    }
    return 1; // success
}

char rotate(char c,
            int k) // rotate one characters at a time by k position and leave non letters unchanged
{
    int shift = k % 26;
    if (isupper(c))
        return 'A' + (c - 'A' + shift) % 26; // keeps uppercase even after being rotated
    else if (islower(c))
        return 'a' + (c - 'a' + shift) % 26; // keeps lowercase even after being rotated
    else                                     // things which arent letters
    {
        return c;
    }
}
