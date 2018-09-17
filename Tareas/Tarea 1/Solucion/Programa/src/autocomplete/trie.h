#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#define ALPHABET 27 // 26 letters + space

typedef struct trie_node TrieNode;

struct trie_node
{
    int freq;
    TrieNode *children[ALPHABET];
    bool isEndOfWord;
};

TrieNode *trie_init();
void trie_insert(TrieNode *root, char *word, int freq);
void trie_search(TrieNode *root, char *word, FILE *output);
void trie_destroy(TrieNode *root);