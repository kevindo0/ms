# 多线程下不设置 Session 为全局变量
# 结论：
# 每个线程下的 Session 都是不同的 Session
# 数据库成功新增了线程3提交的数据，其他的线程中的数据并没有提交到数据库中去。

import threading, time
from sqlalchemy.orm import sessionmaker
from model import engine, Person

session_factory = sessionmaker(bind=engine)
Session = session_factory

def job(name):
    session = Session()
    s1 = Session()
    s2 = Session()
    print(name, id(s1), id(s2), s1 is s2)

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
    s1 = Session()
    s2 = Session()
    print(id(s1), id(s2), s1 is s2)
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
