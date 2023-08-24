from mmu import MMU

class Page:
    def __init__(self, number: int, dirty: bool, lru: int):
        self.number = number
        self.dirty = dirty
        self.lru = lru
        
    
class LruMMU(MMU):
    def __init__(self, frames):
        self.max_frames = frames # the size of the array to store all of the elements
        self.debug = False
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        
        # will store an array of Pages
        self.page_table = []
        
    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False
        
    # after every insert ill update the counters
    # of each element in the page table so i know which is LRU        
    def update_page_table(self):
        for p in self.page_table:
            p.lru += 1
        #print([obj.number for obj in self.page_table])
        #print([obj.lru for obj in self.page_table])
            

    def read_memory(self, page_number):
        #if self.debug: print(f"Page Table: {self.pageTable}")
        
        # check if it is already in the pagetable
        for p in self.page_table:
            if p.number == page_number:
                if self.debug: print(f"Reading: {page_number}")
                p.lru = -1
                self.update_page_table()
                
                return
            
        self.disk_reads += 1
            
        # else it is a page fault and i need to add it
        self.page_faults += 1
        if self.debug: print(f"Page Fault: {page_number}")
        
        # if the page table isnt full then add it
        if len(self.page_table) < self.max_frames:
                # add and update page table
                self.page_table.append(Page(page_number, False, -1)) # adds at -1 because ill immedatly increase all by 1
                self.update_page_table()
                if self.debug: print(f"Reading: {page_number}")
                return
        
        # find the page with the largest lru (it has been there the longest)
        oldestp = self.page_table[0]
        for p in self.page_table:
            if p.lru > oldestp.lru:
                oldestp = p
        
        # now i delete oldest p and replace it with the new one
        # first check if it is dirty
        if oldestp.dirty:
            # then i would write it to disk
            self.disk_writes += 1
            if self.debug: print(f"Disk Write: {oldestp.number}")
        else:
            if self.debug: print(f"Discard: {oldestp.number}")
            
        # remove it from page_Table
        self.page_table.remove(oldestp)
        
        # add the new one
        self.page_table.append(Page(page_number, False, -1))
        self.update_page_table()
        if self.debug: print(f"Reading: {page_number}")
        return
    

    def write_memory(self, page_number):
        #if self.debug: print(f"Page Table: {self.pageTable}")
        
        # check if it is already in the pagetable
        for p in self.page_table:
            if p.number == page_number:
                p.dirty = True # make it a dirty value since this is a write
                if self.debug: print(f"Writing: {page_number}")
                p.lru = -1
                self.update_page_table()
                return
            
        self.disk_reads += 1
            
        # else it is a page fault and i need to add it
        self.page_faults += 1
        if self.debug: print(f"Page Fault: {page_number}")
        
        # if the page table isnt full then add it
        if len(self.page_table) < self.max_frames:
                self.page_table.append(Page(page_number, True, -1))
                self.update_page_table()
                if self.debug: print(f"Writing: {page_number}")
                return
        
        # else
        # find the page with the largest lru (it has been there the longest)
        oldestp = self.page_table[0]
        for p in self.page_table:
            if p.lru > oldestp.lru:
                oldestp = p
        
        # now i delete oldest p and replace it with the new one
        # first check if it is dirty
        if oldestp.dirty:
            # then i would write it to disk
            self.disk_writes += 1
            if self.debug: print(f"Disk Write: {oldestp.number}")
        else:
            if self.debug: print(f"Discard: {oldestp.number}")
            
            
        # remove it from page_Table
        self.page_table.remove(oldestp)
        
        # add the new one
        self.page_table.append(Page(page_number, True, -1))
        self.update_page_table()
        if self.debug: print(f"Writing: {page_number}")
        return
        
        
            


    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
