#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "trie.h"
#define MAX_LENGTH 100

int main(int argc, char *argv[])
{
	if (argc != 4)
	{
		printf("Modo de uso: ./solver database.txt queries.txt output.txt\n");
		return 0;
	}
	FILE *database = fopen(argv[1], "r");
	FILE *queries  = fopen(argv[2], "r");
	FILE *output   = fopen(argv[3], "w");


	if (!database || !queries || !output)
	{
		printf("¡Error abriendo los archivos!");
		return 2;
	}

	// read the n value in our database file
	int n;
	fscanf(database, "%d\n", &n);

	// create our Trie
	TrieNode * root = trie_init();

	/* for each line, read the input and insert the word in our diccionary
	 * note that we are not reading the '\n' char at the end of the line
	 */
	for (int i = 0; i < n; i++)
	{
		char str[MAX_LENGTH];
		int freq; 
		int string_length;
		fscanf(database, "%d %d ", &freq, &string_length);
		for (int c = 0; c < string_length; c++)
		{
			fscanf(database, "%c", &str[c]);
		}
		str[string_length] = '\0';
		trie_insert(root, str, freq);
	}
	fclose(database);

	// read the n value in our queries file
	int m;
	fscanf(queries, "%d\n", &m);

	// for each line in our queries file, search the word in our Trie and write it to output
	for (int i = 0; i < m; i++)
	{
		char str[MAX_LENGTH];
		int string_length;
		fscanf(queries, "%d ", &string_length);
		for (int c = 0; c < string_length; c++)
		{
			fscanf(queries, "%c", &str[c]);
		}
		str[string_length] = '\0';
		trie_search(root, str, output);
	}
	// close the the queries and output files 
	fclose(queries);
	fclose(output);
	// free the memmory
	trie_destroy(root);
	return 0;
}
