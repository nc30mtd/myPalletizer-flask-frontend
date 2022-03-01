from queue import Queue
from threading import Thread
from pymycobot.mypalletizer import MyPalletizer

class MyPalletizerProcess(Thread):
 
    def __init__(self, task_queue, result_queue, portname):
        self.myPalletizer = MyPalletizer(portname)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.signal = True
        self.radians = None

    def get_coords(self):
        print('get_coords()')
        return self.myPalletizer.get_coords()

    def run(self):

        while self.signal:
            # look for incoming mainthread request
            if not self.task_queue.empty():
                task = self.task_queue.get()
                
                if(task[0] == 'get_radians'):
                    self.result_queue.put(self.myPalletizer.get_radians())
                elif(task[0] == 'send_radians'):
                    self.result_queue.put(self.myPalletizer.send_radians(task[1], task[2]))
                elif(task[0] == 'sync_send_angles'):
                    self.result_queue.put(self.myPalletizer.sync_send_angles(task[1], task[2]))
                elif(task[0] == 'sync_send_coords'):
                    self.result_queue.put(self.myPalletizer.sync_send_coords(task[1], task[2], task[3]))
                elif(task[0] == 'gpio_init'):
                    pass
                elif(task[0] == 'gpio_output'):
                    pass
                elif(task[0] == 'wait'):
                    self.result_queue.put(self.myPalletizer.wait(task[1]))
                elif(task[0] == '_mesg'):
                    pass
                elif(task[0] == 'get_coords'):
                    self.result_queue.put(self.get_coords())
                else:
                    pass

    def get_angles(self):
        return self.myPalletizer.get_radians()