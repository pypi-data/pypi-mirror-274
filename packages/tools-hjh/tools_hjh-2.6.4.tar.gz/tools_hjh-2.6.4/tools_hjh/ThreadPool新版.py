# coding:utf-8
import time
import threading
from uuid import uuid1
import eventlet


def one(name):
    print(name, 'begin')
    time.sleep(3)
    print(name, 'end')
    return 'rs is ' + str(name)


def main():
    tp = ThreadPool(2)
    tp.run(one, ('1',), time_out=1)
    tp.wait()
    tp.run(one, ('2',), time_out=1)
    tp.wait()


class ThreadPool():
    """ 维护一个线程池 """
    
    def __init__(self, size, save_result=False, while_wait_time=0.5):
        self.size = size
        self.thread_pool = []
        self.result_map = {}
        self.save_result = save_result
        self.while_wait_time = while_wait_time
        
    def clear(self):
        self.pool_status = [0]
        self.result_map = {}

    def run(self, func, args, kwargs={}, time_out=float('inf')):
        """ 主线程命令当前线程池从空闲线程中取一个线程执行给入的方法，如果池满，则主线程等待 """
        thread_id = uuid1()
        if len(self.thread_pool) < self.size:
            t = myThread(func, args=args, kwargs=kwargs, thread_id=thread_id, result_map=self.result_map, save_result=self.save_result, time_out=time_out)
            t.start()
            self.thread_pool.append({'thread_obj':t, 'status':t.is_alive()})
        else:
            already_running = False
            while(not already_running):
                for tt in self.thread_pool:
                    if tt['status']:
                        tt['status'] = tt['thread_obj'].is_alive()
                    else:
                        tt['thread_obj'] = myThread(func, args=args, kwargs=kwargs, thread_id=thread_id, result_map=self.result_map, save_result=self.save_result, time_out=time_out)
                        tt['thread_obj'].start()
                        tt['status'] = tt['thread_obj'].is_alive()
                        already_running = True
                        break
                time.sleep(self.while_wait_time)
        return thread_id

    def get_results(self):
        return self.result_map
    
    def get_result(self, num):
        return self.result_map[num]
    
    def clear_result(self):
        self.result_map = {}
        
    def get_running_num(self):
        i = 0
        for tt in self.thread_pool:
            if tt['thread_obj'].is_alive():
                i = i + 1
        return i

    def wait(self):
        """ 主线程等待，直到线程池不存在活动线程 """
        for tt in self.thread_pool:
            if tt['thread_obj'].is_alive():
                tt['thread_obj'].join()


class myThread (threading.Thread):

    def __init__(self, func, args, kwargs, thread_id, result_map, save_result, time_out=float('inf')):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.thread_id = thread_id
        self.result_map = result_map
        self.save_result = save_result
        self.time_out = time_out
        threading.Thread.daemon = True

    def run(self):
        eventlet.monkey_patch()
        with eventlet.Timeout(self.time_out, False):
            result = self.func(*self.args, **self.kwargs)
            if self.save_result:
                self.result_map[self.thread_id] = result


if __name__ == '__main__':
    main()
