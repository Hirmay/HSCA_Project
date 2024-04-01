According to Moore's Law, CPU speeds have been increasing exponentially, while memory speeds have not been growing at a similar rate. This creates a significant disparity between CPU and memory speeds, resulting in a bottleneck situation where the CPU is ready to work but the memory cannot keep up. This disparity is evident from the figure provided [here](https://www.researchgate.net/profile/Katherine-Yelick/publication/3214931/figure/fig1/AS:669980936921091@1536747311324/Processor-Memory-Performance-GapHen96.png).

To address this gap, cache memory serves as smaller yet faster memory. However, due to its smaller size, cache misses may occur, leading to challenges in optimizing hit rate, hit time, miss rate, and miss time. We implemented set-associative mapping to map main memory with the cache for several reasons:
- Fully associative cache allows for placing blocks in any cache set line, maximizing cache utilization.
- This mapping generally results in a higher cache hit rate.
- It enables the use of a replacement algorithm, such as the Least Recently Used (LRU) algorithm, in case of a cache miss.

Cache pipelining is preferred over sequential execution for several reasons:
- Sequential execution processes one instruction at a time, resulting in single-cycle execution. In contrast, a pipelined structure executes in parallel once the pipeline is filled, particularly in the case of a cache hit.
- Pipelining substantially reduces hit time compared to serial execution.
