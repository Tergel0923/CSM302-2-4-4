/* Shared pure arithmetic, compiled by both kernel and user-space tests. */
#ifndef KDS_COLLATZ_MATH_H
#define KDS_COLLATZ_MATH_H
static inline int kds_next(unsigned long long n, unsigned long long *out)
{
    if (!n) return -1;
    if (!(n & 1ULL)) { *out = n / 2; return 0; }
    if (n > (~0ULL - 1ULL) / 3ULL) return -1;
    *out = n * 3ULL + 1ULL;
    return 0;
}
#endif
