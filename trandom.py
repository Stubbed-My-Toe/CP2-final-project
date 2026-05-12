import collections.abc
import hashlib
import os
import time
import threading

class alternate_random(collections.abc.Iterator):
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val
        self.lock = threading.Lock() # Prevents threads from messing up data
    def __next__(self):
        return self.generate_number()
    def _collect_entropy(self):
        noise1 = os.urandom(32)
        nums = []
        nums.append(getattr(os, 'CLD_CONTINUED', 1))
        nums.append(getattr(os, 'CLD_DUMPED', 2))
        nums.append(getattr(os, 'CLD_EXITED', 3))
        nums.append(getattr(os, 'CLD_KILLED', 4))
        nums.append(getattr(os, 'CLD_TRAPPED', 5))
        nums.append(getattr(os, 'EX_CANTCREAT', 73))
        if hasattr(os, 'CLD_STOPPED'): 
            nums.append(os.CLD_STOPPED)
        for attr in dir(os):
            if attr.startswith('EX_') and isinstance(getattr(os, attr), int):
                nums.append(getattr(os, attr))
        if os.cpu_count() is not None:
            nums.append(os.cpu_count())
        for func_name in ['geteuid', 'getegid', 'getpgrp', 'getpid', 'getppid', 'getuid']:
            if hasattr(os, func_name):
                func = getattr(os, func_name)
                nums.append(func())
        if hasattr(os, 'getloadavg'):
            load_1, load_5, load_15 = os.getloadavg()
            nums.append(load_1)
            nums.append(load_5)
            nums.append(load_15)
        if hasattr(os, 'getpriority') and hasattr(os, 'PRIO_PROCESS'):
            nums.append(os.getpriority(os.PRIO_PROCESS, 0))
        noise2 = str(nums).encode('utf-8')
        noise3 = str(time.perf_counter_ns()).encode('utf-8')
        return noise1 + noise2 + noise3
    def _crunch_data(self):
        chaos = self._collect_entropy()
        hasher = hashlib.sha256()
        hasher.update(chaos)
        return hasher.digest()

    def generate_number(self):
        with self.lock:
            secure_bytes = self._crunch_data()[:16]
            large_integer = int.from_bytes(secure_bytes, byteorder='big')
            range_size = (self.max_val - self.min_val) + 1
            scaled_value = self.min_val + (large_integer % range_size)
            return scaled_value