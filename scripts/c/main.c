#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int xy2d(int n, int x, int y);
void d2xy(int n, int d, int *x, int *y);
void rot(int n, int *x, int *y, int rx, int ry);

int main(int argc, char** argv) {
    int bit;
    uint8_t x = atoi(argv[1]);
    uint8_t y = atoi(argv[2]);
    printf("Computing n2 hilberts curve @ x: %d y: %d\n", x, y);
    bit = xy2d(64, x, y);
    printf("%d\n", bit);
    return 0;
}

// convert (x,y) to d
int xy2d(int n, int x, int y) {
    int rx, ry, s, d = 0;
    for (s = n/2; s > 0; s /= 2) {
        rx = (x & s) > 0;
        ry = (y & s) > 0;
        d += s * s * ((3 * rx) ^ ry);
        printf("iteration s: %d\trx: %d\try: %d\td: %d\n", s, rx, ry, d);
        rot(n, &x, &y, rx, ry);
    }
    return d;
}

// convert d to (x,y)
void d2xy(int n, int d, int *x, int *y) {
    int rx, ry, s, t = d;
    *x = *y = 0;
    for (s = 1; s < n; s*=2) {
        rx = 1 & (t/2);
        ry = 1 & (t ^ rx);
        rot(s, x, y, rx, ry);
        *x += s * rx;
        *y += s * ry;
        t /= 4;
    }
}

// rotate/flip a quadrant appropriately
void rot(int n, int *x, int *y, int rx, int ry) {
    if (ry == 0) {
        if (rx == 1) {
            *x = n-1 - *x;
            *y = n-1 - *y;
        }
        // Swap x and y
        int t  = *x;
        *x = *y;
        *y = t;
    }
}