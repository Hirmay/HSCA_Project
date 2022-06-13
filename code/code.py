from random import *
import time
import threading

# we are using 4-way set associative mapping


def decimalToBinary(n):
    st = "{0:b}".format(int(n))
    return st


mainMemory = ["Data no. " + str(i + 1)
              for i in range(1024)]  # data of main memory
mainMemory2 = []
for i in range(256):
    l = []
    for j in range(4):
        st = str(i*4 + j)
        l.append(st)
    mainMemory2.append(l)
# print(mainMemory2)

cacheMemory = [[], [], [], []]  # 4 sets and each set has 4 blocks
print(cacheMemory)
# now the cache is filled random data
totFilled = 0
while(totFilled < 16):
    mainaddr = randint(0, 255)
    # print(mainaddr)
    tempdict = {}
    # start = i*10
    # l = []
    addrTemp = decimalToBinary((mainaddr))
    addrTemp = addrTemp.zfill(8)
    cacheTag = '1' + addrTemp[0:6]
    print('adsfasfasdfwefwe', mainaddr, cacheTag)
    print('adsfadsfds', addrTemp[6:8])
    # perfect
    cacheSet = int(addrTemp[6:8], 2)
    # time.sleep(1)
    if(len(cacheMemory[cacheSet]) == 4):
        continue
    cacheMemory[cacheSet].append({cacheTag: mainMemory2[mainaddr]})
    totFilled += 1
    print(totFilled)

print(cacheMemory)

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
    # address = int(address, 16)
    addrTemp = decimalToBinary((address))

    addrTemp = addrTemp.zfill(10)

    offset = addrTemp[8:10]
    tag = addrTemp[0:6]
    set_no = int(addrTemp[6:8], 2)
    f = 0
    for i in cacheMemory[set_no]:
        for j in i:
            cacheTag = j[1:7]
            validBit = j[0]

            if(validBit == '1' and tag == cacheTag):
                f = 1
                print('HITTTTTTTTTTT')
    if(f == 0):
        print('MISS!!')
    # check all keys of cacheMemory[set_no]
    # for key in cacheMemory[set_no]:
    #     if((key // 16) == tag):
    #         time.sleep(1)
    #         print("Instruction", instr_no, ": Data in cache is: " +
    #               str(cacheMemory[set_no][key]), ". Current time is (in seconds): ", time.time() - startTime)
    #         break


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
