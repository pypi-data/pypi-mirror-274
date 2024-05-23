# coding:utf-8
import time
import threading
from uuid import uuid1
import datetime


def one(name):
    print(name, 'begin')
    time.sleep(10)
    print(name, 'end')


def main():
    tp = ThreadPool(2)
    tp.run(one, ('1',))
    tp.run(one, ('2',))
    tp.run(one, ('3',))
    # tp.wait()


class ThreadPool():
    """ 维护一个线程池 """
    
    def __init__(self, size, save_result=False, while_wait_time=0.5, report=False):
        self.size = size
        self.thread_pool = []
        self.pool_status = [0]
        self.result_map = {}
        self.save_result = save_result
        self.while_wait_time = while_wait_time
        self.report = report
        
    def clear(self):
        self.pool_status = [0]
        self.result_map = {}

    def run(self, func, args, kwargs={}):
        """ 主线程命令当前线程池从空闲线程中取一个线程执行给入的方法，如果池满，则主线程等待 """
        if self.pool_status[0] < self.size:
            thread_id = uuid1()
            t = myThread(func, args=args, kwargs=kwargs, thread_id=thread_id, pool_status=self.pool_status, result_map=self.result_map, save_result=self.save_result)
            t.start()
            self.thread_pool.append(t)
            return thread_id
        else:
            while self.pool_status[0] >= self.size:
                time.sleep(self.while_wait_time)
            return self.run(func, args, kwargs)

    def get_results(self):
        return self.result_map
    
    def get_result(self, num):
        return self.result_map[num]
    
    def clear_result(self):
        self.result_map = {}

    def wait(self):
        """ 主线程等待，直到线程池不存在活动线程 """
        '''
        while self.pool_status[0] > 0:
            if self.report:
                print('ThreadPool running thread num is ' + str(self.pool_status[0]))
            time.sleep(self.while_wait_time)
        '''
        for t in self.thread_pool:
            if t.isAlive():
                run_time = t.get_run_time()
                print(run_time)
                t.join()


class myThread (threading.Thread):

    def __init__(self, func, args, kwargs, thread_id, pool_status, result_map, save_result):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.thread_id = thread_id
        self.pool_status = pool_status
        self.result_map = result_map
        self.save_result = save_result
        self.begin_time = datetime.datetime.now()

    def run(self):
        self.pool_status[0] = self.pool_status[0] + 1
        result = self.func(*self.args, **self.kwargs)
        if self.save_result:
            self.result_map[self.thread_id] = result
        self.pool_status[0] = self.pool_status[0] - 1
        
    def get_run_time(self):
        return datetime.datetime.now() - self.begin_time


if __name__ == '__main__':
    main()
