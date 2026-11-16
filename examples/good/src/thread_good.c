/* thread_good.c — CORRECT version (fixture for qnx-doctor).
 * Two threads with explicit scheduling and DIFFERENT priorities
 * (control 20, logger 10), memory locked, slog2f for logging.
 */
#include <pthread.h>
#include <sched.h>
#include <sys/slog2.h>
#include <sys/mman.h>
#include <stdlib.h>

static void *control_thread(void *arg)
{
    (void)arg;
    mlockall(MCL_CURRENT | MCL_FUTURE);
    for (;;) {
        /* Real-time control work — no printf, no heap, no blocking I/O. */
        slog2f(_SLOG_SETCODE(_SLOG_SYSMSG, 0), _SLOG_INFO, "control tick");
    }
    return NULL;
}

static void *logger_thread(void *arg)
{
    (void)arg;
    mlockall(MCL_CURRENT | MCL_FUTURE);
    for (;;) {
        slog2f(_SLOG_SETCODE(_SLOG_SYSMSG, 0), _SLOG_INFO, "log tick");
    }
    return NULL;
}

int main(void)
{
    pthread_attr_t attr_control, attr_logger;
    struct sched_param sp_control, sp_logger;

    pthread_attr_init(&attr_control);
    pthread_attr_setinheritsched(&attr_control, PTHREAD_EXPLICIT_SCHED);
    pthread_attr_setschedpolicy(&attr_control, SCHED_FIFO);
    sp_control.sched_priority = 20;
    pthread_attr_setschedparam(&attr_control, &sp_control);

    pthread_attr_init(&attr_logger);
    pthread_attr_setinheritsched(&attr_logger, PTHREAD_EXPLICIT_SCHED);
    pthread_attr_setschedpolicy(&attr_logger, SCHED_FIFO);
    sp_logger.sched_priority = 10;
    pthread_attr_setschedparam(&attr_logger, &sp_logger);

    pthread_t control, logger;
    if (pthread_create(&control, &attr_control, control_thread, NULL) != 0) {
        perror("pthread_create control");
        return EXIT_FAILURE;
    }
    if (pthread_create(&logger, &attr_logger, logger_thread, NULL) != 0) {
        perror("pthread_create logger");
        return EXIT_FAILURE;
    }
    pthread_join(control, NULL);
    pthread_join(logger, NULL);
    return 0;
}
