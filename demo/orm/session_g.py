# 在多线程下用全局 Session
# 结论：
# 全部线程下的 Session 都时同一个 Session
# 每个线程下的数据都被提交到了数据库

import threading, time
from sqlalchemy.orm import sessionmaker
from model import engine, Person

session_factory = sessionmaker(bind=engine)
Session = session_factory
session = Session()

def job(name):
    global session
    print(f"id session:{id(session)}")
    person = Person(name='frank-' + name, mobile='111111', id_card_number='123456789')
    print(f"{name} person is add..")
    session.add(person)
    time.sleep(1)
    if name == 'job3':
        # 线程3 提交, 其他线程不提交.
        session.commit()
        session.close()

if __name__ == '__main__':
    thread_list = []
    # 创建5个线程
    for i in range(5):
        name = 'job' + str(i)
        t = threading.Thread(target=job, name=name, args=(name,))
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
        