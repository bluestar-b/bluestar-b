#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void test_ram_speed() {
    int buffer_size = 10000000;
    unsigned char *data = (unsigned char *)malloc(buffer_size * sizeof(unsigned char));
    int i;

    for (i = 0; i < buffer_size; i++) {
        data[i] = i % 256;
    }

    clock_t start_time = clock();
    for (i = 0; i < 100; i++) {
        unsigned char *buffer_copy = (unsigned char *)malloc(buffer_size * sizeof(unsigned char));
        memcpy(buffer_copy, data, buffer_size);
        free(buffer_copy);
    }
    clock_t end_time = clock();

    double write_speed = (double)buffer_size * 100 / (double)(end_time - start_time) * CLOCKS_PER_SEC / 1e6;

    start_time = clock();
    for (i = 0; i < 100; i++) {
        unsigned char *buffer_copy = (unsigned char *)malloc(buffer_size * sizeof(unsigned char));
        memcpy(buffer_copy, data, buffer_size);
        free(buffer_copy);
    }
    end_time = clock();

    double read_speed = (double)buffer_size * 100 / (double)(end_time - start_time) * CLOCKS_PER_SEC / 1e6;

    printf("RAM Write Speed: %.2f MB/s\n", write_speed);
    printf("RAM Read Speed: %.2f MB/s\n", read_speed);

    free(data);
}

int main() {
    test_ram_speed();
    return 0;
}
