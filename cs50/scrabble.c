#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int computer_score(string word);

int main(void)
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");
    if (computer_score(word1) > computer_score(word2))
    {
        printf("Player 1 wins!\n");
    }
    else if (computer_score(word1) < computer_score(word2))
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}
int computer_score(string word)
{
    int score = 0;
    for (int i = 0, len = strlen(word); i < len; i = i + 1)
    {
        if (isupper(word[i]))
        {
            score = score + POINTS[word[i] - 65];
        }
        else if (islower(word[i]))
        {
            score = score + POINTS[word[i] - 97];
        }
    }
    return score;
}
