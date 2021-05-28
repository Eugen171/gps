#include <stdio.h>
#include <string.h>
#include <stdlib.h>

<<<<<<< HEAD
=======
#define BUF_SIZE 1024

>>>>>>> 81b13885c23cc6a781b13c79b1b37185e6286587
char *get_raw_nmea(FILE *f, char *buffer)
{
	char *start = buffer;
	char *ptr = buffer;
<<<<<<< HEAD
	int i = 0;
	while (i < 550)
		buffer[i++] = fgetc(f);
	buffer[i] = 0;
	i = 0;
	do {
		ptr = start;
		*start = buffer[i++];
		while (*start == '$' && ptr - start < 4)
			*++ptr = buffer[i++];
	} while (start[4] != 'G');
	start = ptr;
	i = 0;
	do {
		if ((*++ptr = buffer[i++] == '$')
			start = ptr;
		while (*start == '$' && ptr - start < 5)
			*++ptr = buffer[i++];
=======

	do {
		ptr = start;
		*start = fgetc(f);
		while (*start == '$' && ptr - start < 4)
			*++ptr = fgetc(f);
	} while (start[4] != 'G');
	start = ptr;
	do {
		if ((*++ptr = fgetc(f)) == '$')
			start = ptr;
		while (*start == '$' && ptr - start < 5)
			*++ptr = fgetc(f);
>>>>>>> 81b13885c23cc6a781b13c79b1b37185e6286587
	} while (start[4] != 'G');
	*start = 0;
	return (buffer);
}

int main()
{
	FILE *f;
	char buffer[2048];

	f = fopen("./test.txt", "r");
	printf("%s\n\n", get_raw_nmea(f, buffer));
	fclose(f);
}
