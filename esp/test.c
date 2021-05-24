#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUF_SIZE 1024

char *get_raw_nmea(FILE *f)
{
	// gpgsa is begining
	int i;
	int prev_line_start = -10;
	char *buffer = (char *)malloc(sizeof(char) * BUF_SIZE);

	i = 0;
	while (i != 6 || strncmp(buffer, "$GPGGA", 6) != 0) {
		buffer[i] = fgetc(f);
		if (buffer[i] == '$') {
			i = 0;
			buffer[0] = '$';
		}
		++i;
	}
	while (i - prev_line_start != 6 || strncmp(&buffer[prev_line_start], "$GPGGA", 6) != 0) {
		buffer[i] = fgetc(f);
		if (buffer[i] == '$')
			prev_line_start = i;
		++i;
	}
	buffer[prev_line_start] = 0;
	return (buffer);
}

int main()
{
	FILE *f;

	f = fopen("./test.txt", "r");
	printf("%s\n\n", get_raw_nmea(f));
	fclose(f);
}
