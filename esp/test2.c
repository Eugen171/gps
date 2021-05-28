#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUF_SIZE 1024

char *get_raw_nmea(FILE *f, char *buffer)
{
	char *start = buffer;
	char *ptr = buffer;

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
