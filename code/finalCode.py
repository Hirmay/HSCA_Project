from random import randint, random
import time
import threading


def decimalToBinary(n):
    # fuction to convert decimal number to binary
    st = "{0:b}".format(int(n))
    return st


pip_time = [0, 0]
isMiss = False  # flag which will be set to true whenever there is a miss

mainMemory = []  # main memory (has size 1024 bytes)
for i in range(256):
    l = []
    for j in range(4):
        st = str(i*4 + j)
        l.append(st)
    mainMemory.append(l)
cacheMemory = [[], [], [], []]


def cacheMem():
    global cacheMemory
    # We are using 4-way set associative mapping
    # 4 sets and each set has 4 blocks

    for i in range(5, 69):
        # initializing the cache
        mainaddr = i
        tempdict = {}
        addrTemp = decimalToBinary((mainaddr))
        addrTemp = addrTemp.zfill(8)
        cacheTag = '1' + addrTemp[0:6]

        cacheSet = int(addrTemp[6:8], 2)
        if(len(cacheMemory[cacheSet]) == 4):
            continue
        cacheMemory[cacheSet].append({cacheTag: mainMemory[mainaddr]})

    # data structure which stores information regarding at which time an address is used last
    timedCache = cacheMemory
    for s in timedCache:
        for curdict in s:
            curdict["time"] = 0
    print(timedCache)
    return timedCache


timedCache = cacheMem()

addresses = []  # contains the sequence and details of addresses to be loaded

while(1):
    # Menu
    print('Select option:\na)If you want to add address manually\nb)If you want to add address in a range\nc)If you want to test actual scenario which utilizes both Temporal and Spatial localities')
    option = input()
    if(option == 'a'):
        n_instr = int(  # number of instructions
            input("Enter the number of instructions you want to enter: "))

        for i in range(n_instr):
            addr = input("Enter address (in hexadecimal): ")
            addresses.append(int(addr, 16))
        break
    elif(option == 'b'):
        start = int(input("Enter the starting address in *HEX*: "), 16)
        end = int(input("Enter the ending address in *HEX*: "), 16)
        for i in range(start, end+1):
            addresses.append(i)
        n_instr = len(addresses)
        break
    elif(option == 'c'):
        addresses = [0, 1, 2, 3, 4, 5, 6, 7, 0, 3, 7, 5, 10,
                     9, 4, 6, 8, 9, 10, 11, 7, 6, 2, 1, 0, 9, 10, 8]
        n_instr = len(addresses)
        break
    else:
        print("Invalid option")

pipeline_option = -1
while(1):
    pipeline_option = int(input(
        "Select an option: \n0 if you want to simulate using pipelined cache, \n1 if you want to simulate using non-pipelined cache, \n2 if you want to compare their results: "))
    if(pipeline_option != 0 and pipeline_option != 1 and pipeline_option != 2):
        print("Invalid input. try again\n")
    else:
        break


def check_valid_bit(instr_no, address, cycle_no, startTime):
    # function to check whether the required tag is present in cache or not
    global isMiss
    addrTemp = decimalToBinary((address))  # convert address to binary
    # pad the front with 0's till the length of the binary string is 10
    addrTemp = addrTemp.zfill(10)

    tag = addrTemp[0:6]  # the first 6 bits of address are the tag
    set_no = int(addrTemp[6:8], 2)  # the next 2 bits of the address are tag
    offset = addrTemp[8:10]  # the last 2 bits of the address are offset

    time.sleep(0.1)  # time taken for execution
    global timedCache
    for i in timedCache[set_no]:  # iterating over all blocks of that set
        for j in i:
            if(j == "time"):
                continue
            cacheTag = j[1:7]
            validBit = j[0]

            if(validBit == '1' and tag == cacheTag):  # checking the valid bit and comparing the tag
                # Cache HIT
                i["time"] = time.time() - startTime
                print("Instruction", instr_no, ": Data has been found in cache.",
                      "Current time is (in seconds): ", time.time() - startTime)
                return

    isMiss = True  # Cache MISS
    print("Instruction", instr_no,
          ": MISS occured. Current time is (in seconds): ", time.time() - startTime)


def get_data_from_cache(instr_no, address, cycle_no, startTime):
    # function to print data retrieved from the cache
    time.sleep(0.1)  # time taken for execution of this function
    global isMiss
    addrTemp = decimalToBinary((address))
    addrTemp = addrTemp.zfill(10)

    tag = addrTemp[0:6]
    set_no = int(addrTemp[6:8], 2)
    offset = addrTemp[8:10]

    for i in timedCache[set_no]:
        for j in i:
            cacheTag = j[1:7]
            validBit = j[0]

            if(validBit == '1' and tag == cacheTag):
                print("Instruction", instr_no, ": Data fetched from cache is: " +
                      str(i[j]), ". Current time is (in seconds): ", time.time() - startTime)
                return


def data_to_cpu(instr_no, cycle_no, startTime):
    time.sleep(0.1)
    print("Instruction", instr_no, ": Data mentioned in the last step has been given to CPU. ",
          "Current time is (in seconds): ", time.time() - startTime)
    global n_instr, pip_time, pipeline_option
    pip_time[pipeline_option] = time.time() - startTime


def non_pipelined_cache():
    # function to simulate non-pipelined cache
    n = 0
    global isMiss
    startTime = time.time()  # current time
    while n < n_instr:
        check_valid_bit(n+1, addresses[n], n + 1, startTime)
        if isMiss:
            # time taken to fetch data from main memory and storing it into cache
            time.sleep(0.7)
            # here we are assuming that cache is two times faster than main memory (due to time constraints of the simulation)

            # insert in cache and print the data
            addrTemp = decimalToBinary((addresses[n]))
            addrTemp = addrTemp.zfill(10)
            tag = addrTemp[0:6]
            set_no = int(addrTemp[6:8], 2)

            # find the oldest timed block in set_no of timedCache
            oldInd, oldTime = 0, timedCache[set_no][0]["time"]
            for i in range(len(timedCache[set_no])):
                if(timedCache[set_no][i]["time"] < oldTime):
                    oldInd = i
                    oldTime = timedCache[set_no][i]["time"]

            # remove the oldest block
            timedCache[set_no].pop(oldInd)

            # insert the new block
            cacheTag = '1' + tag
            curAddress = addresses[n] // 4
            cacheMemory[set_no].append(
                {cacheTag: mainMemory[curAddress], "time": time.time() - startTime})
            print("\nInstruction", n + 1,
                  "had a miss in data. LRU implemented and inserted in cache, along with fetching and serving to the CPU. Current time is:", time.time() - startTime)
            if (n + 1) == n_instr:
                pip_time[1] = time.time() - startTime
            isMiss = False
        else:
            get_data_from_cache(n+1, addresses[n], n+1, startTime)
            data_to_cpu(n+1, n+1, startTime)
        n += 1
        print()


def pipelined_cache():
    # function to simulate pipelined cache
    pipeline = []  # data structure used to maintain the pipeline of instructions
    # each element of pipeline would be a list having two elements
    # first element would be the instruction number
    # second element would be the of cycles that instruction has executed so far

    n = 0  # current instruction number
    skip = []
    startTime = time.time()  # current time
    while (n < n_instr or len(pipeline) > 0):
        # while there are instructions remaining to be executed and instructions in the pipeline
        if(skip.count(n) > 0):  # if the nth instruction is to be skipped
            n += 1
            continue

        t1, t2, t3 = threading.Thread(), threading.Thread(), threading.Thread()
        # t1, t2 and t3 will be used to execute the check_valid_bit, get_data_from_cache and
        # data_to_cpu functions for the instructions present in the cache
        f1, f2, f3 = 0, 0, 0
        # flags to check whether t1, t2 and t3 have been executed or not
        if(len(pipeline) == 0):
            # if there are no instructions in the pipeline
            if (n < n_instr):
                t1 = threading.Thread(target=check_valid_bit, args=(
                    n+1, addresses[n], n+1, startTime))
                t1.start()
                f1 = 1
                pipeline.append([n, 1])
        elif(len(pipeline) == 1):
            # if there is 1 instruction in the pipeline
            # instruction number of the first element in pipeline
            temp = pipeline[0][0]
            if(pipeline[0][1] == 2):  # if the first instruction has executed 2 cycles
                t3 = threading.Thread(target=data_to_cpu,
                                      args=(temp+1, temp+1, startTime))
                t3.start()
                f3 = 1
            else:  # if the first instruction has executed 1 cycle
                t2 = threading.Thread(target=get_data_from_cache, args=(
                    temp + 1, addresses[temp], temp+1, startTime))
                t2.start()
                f2 = 1
            # increasing the number of cycles that the first instruction has executed
            pipeline[0][1] += 1
            if (n < n_instr):  # if the current cycle is yet to be executed
                t1 = threading.Thread(target=check_valid_bit, args=(
                    n+1, addresses[n], n+1, startTime))
                t1.start()
                f1 = 1
                pipeline.append([n, 1])
        elif(len(pipeline) == 2):
            # if there are two instructions in the pipeline
            # instruction numbers of the first and second elements in pipeline
            temp1, temp2 = pipeline[0][0], pipeline[1][0]
            t3 = threading.Thread(target=data_to_cpu, args=(
                temp1 + 1, temp1+1, startTime))
            t3.start()
            f3 = 1
            t2 = threading.Thread(target=get_data_from_cache, args=(
                temp2 + 1, addresses[temp2], temp2+1, startTime))
            t2.start()
            f2 = 1
            # increasing the number of cycles that the first instruction has executed
            pipeline[0][1] += 1
            # increasing the number of cycles that the second instruction has executed
            pipeline[1][1] += 1
            if (n < n_instr):
                pipeline.append([n, 1])
                t1 = threading.Thread(target=check_valid_bit, args=(
                    n+1, addresses[n], n+1, startTime))
                t1.start()
                f1 = 1

        if(f1 == 1):
            t1.join()
        if(f2 == 1):
            t2.join()
        if(f3 == 1):
            t3.join()
        if(pipeline[0][1] == 3):
            # if the oldest instruction in the pipeline has finished executing all three steps, it is popped
            pipeline.pop(0)

        global isMiss
        if(isMiss):
            missed_n = 0  # this is the instruciton for which miss occurred
            for pair in pipeline:
                if(pair[1] == 1):
                    missed_n = pair[0]
                    break
            time.sleep(0.7)  # time taken to flush the cache
            # insert in cache and print the data
            addrTemp = decimalToBinary((addresses[missed_n]))
            addrTemp = addrTemp.zfill(10)
            offset = addrTemp[8:10]
            tag = addrTemp[0:6]
            set_no = int(addrTemp[6:8], 2)

            # find the oldest timed block in set_no of timedCache
            oldInd, oldTime = 0, timedCache[set_no][0]["time"]
            for i in range(len(timedCache[set_no])):
                if(timedCache[set_no][i]["time"] < oldTime):
                    oldInd = i
                    oldTime = timedCache[set_no][i]["time"]

            # remove the oldest block
            timedCache[set_no].pop(oldInd)

            # insert the new block
            cacheTag = '1' + tag
            curAddress = addresses[missed_n] // 4
            cacheMemory[set_no].append(
                {cacheTag: mainMemory[curAddress], "time": time.time() - startTime})

            print()
            print(timedCache)

            # skip this instruction if encountered in future (as it was already executed)
            skip.append(missed_n)
            n = missed_n - 2
            print("\nInstruction", missed_n + 1,
                  "had a miss in data. LRU implemented and inserted in cache. Current time is:", time.time() - startTime)
            pipeline.clear()  # flushing out the pipeline
            isMiss = False
        print()
        n += 1
        n = max(n, 0)


if(pipeline_option == 0):
    pipelined_cache()
elif(pipeline_option == 1):
    non_pipelined_cache()
else:
    # this is to compute the time comparision between pipelined and non-pipelined cache
    pipeline_option = 0
    pipelined_cache()
    # before we have to empty the cache
    pipeline_option = 1
    cacheMemory = [[], [], [], []]
    timedCache = cacheMem()
    isMiss = False
    non_pipelined_cache()
    # 1 is for non pipeline & 0 is for pipeline
    time_imp = 100.0 * (pip_time[1]-pip_time[0])/pip_time[0]
    print(f"\nThere is a time improvement of {time_imp:.2f} %: \n")
