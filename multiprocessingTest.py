import multiprocessing
import time

# 创建进程三个参数
# garget     执行的目标任务名，这里指函数名（方法名）
# name       进程名，一般不用设置
# group      进程组，目前只是用None

# mult = multiprocessing.Process(target=test)

# mult.start()

def sing():
    for i in range(3):
        print("唱歌...")
        time.sleep(0.5)

def dance():
    for i in range(3):
        print("跳舞...")
        time.sleep(0.5)

if __name__ == '__main__':
    sing_process = multiprocessing.Process(target=sing)
    dance_process = multiprocessing.Process(target=dance)

    sing_process.start()
    dance_process.start()