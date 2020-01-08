from datetime import datetime
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

def tick(name):
    print('Tick! name: 【%s】 the time is: %s' % (name, datetime.now()))

def tick_error(name):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), name)
    print (1/0)

@scheduler.scheduled_job('cron', second='*/5')
def test_p():
    print("test_p", datetime.now())

# 进行事件监听
def my_listener(event):
    if event.exception:
        print("task is error", event.exception)
        # print("task is error", event.exception, event.traceback)
        # 出错进行邮件发送等操作
    else:
        print('task is ok!')

if __name__ == '__main__':
    # scheduler.add_job(tick, 'interval', seconds=8, args=['interval'])
    # scheduler.add_job(tick, 'cron', minute=33, args=['cron'])
    scheduler.add_job(tick, 'cron', second='*/7', args=['cron'])
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    try:
        print('server is start...')
        scheduler.start()
    except Exception as ex:
        print("Error:", ex)

"""
second=“*/7”的执行结果：
Tick! name: 【cron】 the time is: 2019-12-25 14:56:56.002336
task is ok!
Tick! name: 【cron】 the time is: 2019-12-25 14:57:00.005616
task is ok!
Tick! name: 【cron】 the time is: 2019-12-25 14:57:07.006720
task is ok!
"""
        