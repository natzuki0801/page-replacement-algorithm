import random

def generate_reference_string(length, max_page=9):
    """Generate a random page reference string with pages from 0 to max_page."""
    return [random.randint(0, max_page) for _ in range(length)]

def fifo(reference_string, frames):
    """FIFO page replacement algorithm."""
    memory = []
    page_faults = 0





    

    for page in reference_string:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)  # Remove oldest page
                memory.append(page)
            page_faults += 1
    return page_faults

def lru(reference_string, frames):
    """LRU page replacement algorithm."""
    memory = []
    page_faults = 0

    for page in reference_string:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                # Remove least recently used page
                memory.pop(0)
                memory.append(page)
            page_faults += 1
        else:
            # Move the accessed page to the end to mark it recently used
            memory.remove(page)
            memory.append(page)
    return page_faults

def opt(reference_string, frames):
    """Optimal page replacement algorithm."""
    memory = []
    page_faults = 0

    for i, page in enumerate(reference_string):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                # Find the page in memory that is not used for longest future time
                future_uses = []
                for mem_page in memory:
                    if mem_page in reference_string[i+1:]:
                        future_uses.append(reference_string[i+1:].index(mem_page))
                    else:
                        # If page not used again, select it immediately
                        future_uses.append(float('inf'))
                # Replace page with the farthest next use
                index_to_replace = future_uses.index(max(future_uses))
                memory[index_to_replace] = page
            page_faults += 1
    return page_faults

def main():
    print("Page Replacement Algorithms: FIFO, LRU, OPT")
    try:
        frames = int(input("Enter number of page frames: "))
        length = int(input("Enter length of page reference string: "))
        if frames <= 0 or length <= 0:
            print("Please enter positive integers for frames and length.")
            return
    except ValueError:
        print("Invalid input. Please enter integers.")
        return

    ref_string = generate_reference_string(length)
    print("\nGenerated Page Reference String:")
    print(ref_string)

    fifo_faults = fifo(ref_string, frames)
    lru_faults = lru(ref_string, frames)
    opt_faults = opt(ref_string, frames)

    print("\nNumber of Page Faults:")
    print(f"FIFO: {fifo_faults}")
    print(f"LRU: {lru_faults}")
    print(f"OPT: {opt_faults}")

if __name__ == "__main__":
    main()


