import sys

def process_numbers(nums):
    total = 0
    for n in nums:
        # Based on the previous logic: sum of n**4 if n <= 0
        if n <= 0:
            total += n ** 4
    return total

def main():
    # Use a generator to fetch tokens (words) one by one
    def get_tokens():
        for line in sys.stdin:
            # Replace commas with spaces to handle "-1,3,1,10" inputs
            normalized_line = line.replace(',', ' ')
            for word in normalized_line.split():
                yield word
    
    tokens = get_tokens()
    
    try:
        first_token = next(tokens)
        n_cases = int(first_token)
    except (StopIteration, ValueError):
        return

    results = []
    for _ in range(n_cases):
        try:
            # Read x (number of elements in this case)
            x_str = next(tokens)
            x = int(x_str)
            
            nums = []
            for _ in range(x):
                nums.append(int(next(tokens)))
            
            results.append(process_numbers(nums))
        except (StopIteration, ValueError):
            # If we run out of tokens mid-case, we stop
            break

    if results:
        print('\n'.join(map(str, results)))

if __name__ == "__main__":
    main()