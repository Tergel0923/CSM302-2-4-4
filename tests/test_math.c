#include <assert.h>
#include <stdio.h>
#include "../src/kernel/collatz_math.h"
int main(void) {
    unsigned long long out, n=15;
    const unsigned long long expected[]={15,46,23,70,35,106,53,160,80,40,20,10,5,16,8,4,2,1};
    unsigned int i;
    for(i=0;i<sizeof(expected)/sizeof(expected[0]);i++) {
        assert(n==expected[i]); if(n!=1) {assert(kds_next(n,&out)==0);n=out;}
    }
    assert(kds_next(0,&out)==-1);
    assert(kds_next(~0ULL,&out)==-1);
    assert(kds_next(2,&out)==0 && out==1);
    assert(kds_next(6148914691236517205ULL,&out)==-1);
    puts("PASS: shared kernel arithmetic, exact 15 sequence, zero and overflow guards");
    return 0;
}
