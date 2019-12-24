# 使用 scoped_session, 多线程下不设置 Session 为全局变量
# 结论：
# 每个线程下的 Session 都不相同
# 只有线程3下的数据被提交到了数据库
# 为每个应用线程 保持着一个不同的对象，即不同的线程 拿到的session 是不一样的

import threading, time
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session
from model import engine, Person

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

@contextmanager
def session():
    # sess = scoped_session(Session)()
    sess = Session()
    try:
        yield sess
        sess.commit()
    except Exception as ex:
        sess.rollback()
        logger.exception(ex)
    finally:
        sess.close()

class Operation:
    def get_a(self):
        with session() as sess:
            print('get_a:', id(sess))

    def get_b(self):
        with session() as sess:
            print('get_b:', id(sess))

    def get_c(self):
        with session() as sess:
            print('get_c:', id(sess))

    def info(self):
        self.get_a()
        self.get_b()
        self.get_c()

def job(name):
    # s1 = Session()
    # s2 = Session()
    # print(name, id(s1), id(s2), s1 is s2)
    session = Session()
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
    s1.close()
    s2 = Session()
    print(id(s1), id(s2), s1 is s2)
    ope = Operation()
    ope.info()
    thread_list = []
    # 创建5个线程
    for i in range(100000):
        name = 'job' + str(i)
        t = threading.Thread(target=job, name=name, args=(name,))
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
        