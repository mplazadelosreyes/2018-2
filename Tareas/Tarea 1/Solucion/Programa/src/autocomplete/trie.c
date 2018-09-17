#include "trie.h"
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

/* Helper function to find the max between two numbers */
#define max(a, b) \
    ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })

/* Helper function to transform a char to int, managing the space */
int char_to_int(const char c)
{
    int i = c - 'a';
    if (i < 0) // in case of white space
        i = 26;
    return i;
}

/* Helper function to transform an int to char, managing the space */
char int_to_char(const int i)
{
    if (i == 26) // special case for a white space
        return ' ';
    else
        return i + 'a';
}

/* Function to initialize a trie node and return it */
TrieNode *trie_init()
{
    TrieNode *trie = malloc(sizeof(TrieNode));
    trie->freq = 0;
    trie->isEndOfWord = false;
    for (int i = 0; i < ALPHABET; i++)
    {
        trie->children[i] = NULL;
    }
    return trie;
}

/* Function to insert a new word into the trie stores
 * the biggest frequency on a node as well for searching
 */
void trie_insert(TrieNode *root, char *word, int freq)
{
    root->freq = max(root->freq, freq);
    for (int i = 0; i < strlen(word); i++)
    {
        int letter = char_to_int(word[i]);
        if (!root->children[letter])
            root->children[letter] = trie_init();
        root = root->children[letter];
        root->freq = max(root->freq, freq);
    }
    root->isEndOfWord = true;
}

/* searches the tree from root and prints the most 
 * frequent string path
 */
void dfs(TrieNode *root, FILE * output)
{
    for (int i = 0; i < 27; i++)
    {
        if (root->children[i] && root->children[i]->freq == root->freq)
        {
            fprintf(output, "%c", int_to_char(i));
            dfs(root->children[i], output);
            return;
        }
    }
}

/* searches the tree for the node of the give prefix
 * and returns it, returns if not found
 */
void trie_search(TrieNode *root, char *prefix, FILE * output)
{
    if (strlen(prefix) == 1) // in case we get an empty string
    {
        dfs(root, output);
        fprintf(output, "\n");
        return;
    }
    for (int i = 0; i < strlen(prefix); i++)
    {
        int letter = char_to_int(prefix[i]);
        // in case where prefix is not found, we write the prefix and return
        if (!root->children[letter]) 
        {
            fprintf(output, "%s\n", prefix);
            return;
        }
        root = root->children[letter];
    }
    fprintf(output, "%s", prefix);
    dfs(root, output);
    fprintf(output, "\n");
}

/* We recursively destroy the trie and free 
 * all of it's memmory from the heap
 */
void trie_destroy(TrieNode *root)
{
    for (int i = 0; i < 27; i++)
    {
        if (root->children[i])
            trie_destroy(root->children[i]);
    }
    free(root);
}