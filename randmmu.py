from mmu import MMU
import random

class Page:
    def __init__(self,number: int, dirty: bool):
        self.number = number
        self.dirty = dirty
        

class RandMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for RandMMU
        self.frames = frames
        self.memory = {}
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug_mode = False

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self.debug_mode = True
        pass

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self.debug_mode = False
        pass

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        if page_number not in self.memory:
            self.page_faults += 1

            if len(self.memory) >= self.frames:
                page_to_replace = random.choice(list(self.memory.keys()))
                if self.memory[page_to_replace].dirty:
                    self.disk_writes += 1
                del self.memory[page_to_replace]
                if self.debug_mode:
                    print(f"Replace page {page_to_replace} (random)")
            self.memory[page_number] = Page(page_number, False)
        
        if self.debug_mode:
            print(f"Reading page {page_number}")

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        self.read_memory(page_number)
        self.memory[page_number].dirty = True
        if self.debug_mode:
            print(f"Write page {page_number}")

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.page_faults
