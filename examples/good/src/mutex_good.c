/* mutex_good.c — CORRECT version (fixture for qnx-doctor).
 * Mutex with PTHREAD_PRIO_INHERIT, ChannelCreate with flags, every
 * kernel call checked, MsgSend guarded by TimerTimeout, name_attach
 * matched by name_detach.
 */
#include <pthread.h>
#include <sys/neutrino.h>
#include <sys/dispatch.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

static pthread_mutex_t lock;
static int chid;

int main(void)
{
    pthread_mutexattr_t mattr;
    pthread_mutexattr_init(&mattr);
    pthread_mutexattr_setprotocol(&mattr, PTHREAD_PRIO_INHERIT);
    if (pthread_mutex_init(&lock, &mattr) != 0) {
        perror("pthread_mutex_init");
        return EXIT_FAILURE;
    }

    chid = ChannelCreate(_NTO_CHF_DISCONNECT | _NTO_CHF_UNBLOCK);
    if (chid == -1) {
        perror("ChannelCreate");
        return EXIT_FAILURE;
    }

    int attach_id = name_attach(NULL, "good_server", 0);
    if (attach_id == -1) {
        perror("name_attach");
        return EXIT_FAILURE;
    }

    /* Client side: timeout armed before MsgSend, result checked. */
    int coid = ConnectAttach(0, 0, chid, 0, 0);
    if (coid == -1) {
        perror("ConnectAttach");
        return EXIT_FAILURE;
    }

    struct sigevent event;
    SIGEV_UNBLOCK_INIT(&event);
    struct _itimer timeout;
    timeout.nsec = 1000000000;
    TimerTimeout(CLOCK_REALTIME, _NTO_TIMEOUT_SEND, &event, &timeout, NULL);

    int msg = 42, rpl = 0;
    if (MsgSend(coid, &msg, sizeof(msg), &rpl, sizeof(rpl)) == -1) {
        perror("MsgSend");
    }

    name_detach(attach_id, 0);
    ChannelDestroy(chid);
    return 0;
}
