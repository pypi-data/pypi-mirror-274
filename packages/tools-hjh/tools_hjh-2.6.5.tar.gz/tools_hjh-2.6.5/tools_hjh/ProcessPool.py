# coding:utf-8
import time
import threading
from uuid import uuid1
import eventlet
from multiprocessing import Process


def one(name):
    print(name, 'begin')
    time.sleep(3)
    print(name, 'end')


def main():
    tp = ProcessPool(2)
    tp.run(one, ('1',))
    tp.run(one, ('2',))
    tp.wait()


class ProcessPool():
    """ 维护一个线程池 """
    
    def __init__(self, size, save_result=False, while_wait_time=0.5, report=False):
        self.size = size
        self.process_pool = []
        self.pool_status = [0]
        self.result_map = {}
        self.save_result = save_result
        self.while_wait_time = while_wait_time
        self.report = report
        
    def clear(self):
        self.pool_status = [0]
        self.result_map = {}

    def run(self, func, args, kwargs={}, time_out=None):
        """ 主线程命令当前线程池从空闲线程中取一个线程执行给入的方法，如果池满，则主线程等待 """
        if self.pool_status[0] < self.size:
            process_id = uuid1()
            t = myProcess(func, args=args, kwargs=kwargs, process_id=process_id, pool_status=self.pool_status, result_map=self.result_map, save_result=self.save_result, time_out=time_out)
            t.start()
            self.process_pool.append(t)
            return process_id
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
        while self.pool_status[0] > 0:
            time.sleep(self.while_wait_time)
    
    def get_running_num(self):
        return self.pool_status[0]


class myProcess (Process):

    def __init__(self, func, args, kwargs, process_id, pool_status, result_map, save_result, time_out):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.process_id = process_id
        self.pool_status = pool_status
        self.result_map = result_map
        self.save_result = save_result
        self.time_out = time_out

    def run(self):
        self.pool_status[0] = self.pool_status[0] + 1
        try:
            if self.time_out is None:
                result = self.func(*self.args, **self.kwargs)
                if self.save_result:
                    self.result_map[self.thread_id] = result
            else:
                # 实测效率很低
                eventlet.monkey_patch()
                with eventlet.Timeout(self.time_out, False):
                    result = self.func(*self.args, **self.kwargs)
                    if self.save_result:
                        self.result_map[self.thread_id] = result
        finally:
            self.pool_status[0] = self.pool_status[0] - 1


if __name__ == '__main__':
    main()
