from datetime import datetime
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.blocking import BlockingScheduler

def tick(name):
	print('Tick! name: 【%s】 the time is: %s' % (name, datetime.now()))

def tick_error(name):
	print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), name)
	print (1/0)

# 进行事件监听
def my_listener(event):
	if event.exception:
		print("task is error", event.exception)
		# print("task is error", event.exception, event.traceback)
		# 出错进行邮件发送等操作
	else:
		print('task is ok!')

if __name__ == '__main__':
	scheduler = BlockingScheduler()
	# scheduler.add_job(tick, 'interval', seconds=8, args=['interval'])
	# scheduler.add_job(tick, 'cron', minute=33, args=['cron'])
	scheduler.add_job(tick_error, 'cron', second='*/5', args=['cron'])
	scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
	try:
		scheduler.start()
	except Exception as ex:
		print("Error:", ex)
		