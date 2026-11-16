/* probe.c — QNX Doctor runtime probe (QEMU x86_64).
 *
 * A tiny real QNX 8.0 program: prints uname, a CLOCK_MONOTONIC
 * timestamp and a prime checksum, then "done rc=0". It is the program
 * qnx-doctor's optional --qemu mode cross-compiles with qcc, packs
 * with mkifs and boots under qemu-system-x86_64.
 *
 * NOTE: this file has NOT been compiled or booted yet — QNX SDP 8.0
 * has not been downloaded (it needs Syarip's myQNX account). It is
 * provided so the QEMU path can be validated as soon as the SDP is
 * available; do not claim it has already run.
 *
 * Build (once SDP 8.0 is installed):
 *   qcc -V gcc_ntox86_64 probe.c -o probe
 *   mkifs probe.build probe.ifs
 *   qemu-system-x86_64 -cpu max -smp 1 -display none \
 *       -kernel probe.ifs -serial stdio
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/utsname.h>

static int prime_checksum(void)
{
    int sum = 0, count = 0;
    for (int n = 2; count < 1000; n++) {
        int prime = 1;
        for (int d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                prime = 0;
                break;
            }
        }
        if (prime) {
            sum += n;
            count++;
        }
    }
    return sum;
}

int main(void)
{
    struct utsname u;
    if (uname(&u) == 0) {
        printf("sysname=%s release=%s machine=%s\n",
               u.sysname, u.release, u.machine);
    }

    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) == 0) {
        printf("monotonic=%lld.%09ld\n",
               (long long)ts.tv_sec, ts.tv_nsec);
    }

    printf("prime_checksum=%d\n", prime_checksum());
    printf("done rc=0\n");
    return 0;
}
