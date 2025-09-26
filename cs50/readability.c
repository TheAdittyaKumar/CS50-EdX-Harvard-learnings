#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text= get_string("Text: ");
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    float L=(letters*100.0f)/words;
    float S=(sentences*100.0f)/words;

    float ColemanLiau_index= 0.0588*L-0.296*S-15.8;
    int grade= (int) roundf(ColemanLiau_index);
    //L is the average number of letters and S is the average number of sentences per 100 words in the text.
    if (grade<1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade>=16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

int count_letters(string text)
{
    int counter3=0;
    for (int i=0; i<strlen(text); i=i+1)
    {
        if (isalpha(text[i]))
            counter3=counter3+1;
    }
    return counter3;
}

int count_words(string text)
    {
        int counter2=0;
        for (int k=0; k<strlen(text); k=k+1)
            {
                if (text[k]==' ')
                    counter2=counter2+1;
            }
            return counter2 + 1;

    }
int count_sentences(string text)
    {
        int counter = 0; // number of . means number of sentences used
        for (int j=0; j<strlen(text); j=j+1)
            {
            if (text[j]=='.' || text[j]=='!' || text[j]== '?')
                {
                    counter=counter+1;
                }
            }
        return counter;
    }
