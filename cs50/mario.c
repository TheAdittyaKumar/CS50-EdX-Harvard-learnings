#include <cs50.h>
#include <stdio.h>

void print_row(int spaces, int bricks);
int main(void)
{
    int n;
    do {
        n=get_int("Height: ");
    }
    while (n<1);
    for (int i=0; i<n; i= i+1)
    {
        int spaces= n-1-i;
        int bricks=i+1;
        print_row(spaces, bricks);
    }
}
void print_row(int spaces, int bricks)
{
    for (int s=0; s<spaces; s=s+1)
    {
        printf(" ");
    }
    for (int b=0; b<bricks; b=b+1)
    {
        printf("#");
    }
    printf("\n");
}

