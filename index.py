
from datetime import datetime
import os

from apscheduler.schedulers.blocking import BlockingScheduler


def tick():
    print(' The time is: %s' % datetime.now())


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'cron', second='10')
    scheduler.add_job(tick, 'cron', second='20')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass