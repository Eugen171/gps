#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *get_raw_nmea(FILE *f, char *buf)
{
	int i = 0;
	while (i < 1100 - 1)
		buf[i++] = fgetc(f);
	buf[i] = 0;
	char *start = strstr(buf, "$GPGGA");
	if (start == NULL)
		return ("");
	char *end = strstr(start + 1, "$GPGGA");
	if (end == NULL)
		return ("");
	*end = 0;
	return (start);
}

int main()
{
	FILE *f;
	char buffer[2048];

	f = fopen("./test.txt", "r");
	printf("%s\n\n", get_raw_nmea(f, buffer));
	fclose(f);
}
