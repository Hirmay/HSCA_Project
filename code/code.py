from random import random
import time
import threading

# we are using 4-way set associative mapping

mainMemory = ["Data no. " + str(i + 1)
              for i in range(1024)]  # data of main memory

cacheMemory = []  # 4 sets and each set has 4 blocks

# now the cache is filled
for i in range(4):
    tempdict = {}
    start = i
    for j in range(4):
        tempdict[start] = mainMemory[start]
        start += 4
    cacheMemory.append(tempdict)


n_instr = int(input("Enter the number of instructions you want to enter: "))
addresses = []
for i in range(n_instr):
    addr = input("Enter address (in hexadecimal): ")
    addresses.append(int(addr, 16))


def check_valid_bit(instr_no, address, cycle_no, startTime):
    if(True):  # assuming valid bit is always true
        time.sleep(1)
        print("Instruction", instr_no,
              ": valid bit is true. Current time is (in seconds): ", time.time() - startTime)
        return True


def get_data_from_cache(instr_no, address, cycle_no, startTime):
    set_no = (address // 4) % 4
    tag = address // 16
    # check all keys of cacheMemory[set_no]
    for key in cacheMemory[set_no]:
        if((key // 16) == tag):
            time.sleep(1)
            print("Instruction", instr_no, ": Data in cache is: " +
                  str(cacheMemory[set_no][key]), ". Current time is (in seconds): ", time.time() - startTime)
            break


def data_to_cpu(instr_no, cycle_no, startTime):
    time.sleep(1)
    print("Instruction", instr_no, ": Data mentioned in the last step has been given to CPU. ",
          "Current time is (in seconds): ", time.time() - startTime)


def non_pipelined_cache():
    n = 0
    startTime = time.time()
    while n < n_instr:
        check_valid_bit(n+1, addresses[n], n + 1, startTime)
        get_data_from_cache(n+1, addresses[n], n+1, startTime)
        data_to_cpu(n+1, n+1, startTime)
        n += 1
        print()


def pipelined_cache():
    n = 0
    startTime = time.time()
    while n < n_instr + 2:
        t1, t2, t3 = threading.Thread(), threading.Thread(), threading.Thread()
        f1, f2, f3 = 0, 0, 0
        if(n < n_instr):
            t1 = threading.Thread(target=check_valid_bit,
                                  args=(n+1, addresses[n], n + 1, startTime))
            t1.start()
            f1 = 1
        if(n > 0 and n < n_instr + 1):
            t2 = threading.Thread(target=get_data_from_cache, args=(
                n, addresses[n-1], n+1, startTime))
            t2.start()
            f2 = 1
        if(n > 1):
            t3 = threading.Thread(target=data_to_cpu,
                                  args=(n-1, n + 1, startTime))
            t3.start()
            f3 = 1

        if(f1 == 1):
            t1.join()
        if(f2 == 1):
            t2.join()
        if(f3 == 1):
            t3.join()
        print()
        n += 1


pipelined_cache()
