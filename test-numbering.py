import itertools

def generate_sequences():
    start = 'aa'
    end = 'le'
    letters = 'abcdefghijklmnopqrstuvwxyz'
    count = 1
    
    for first, second in itertools.product(letters[:12], letters):  # 'l' is the 12th letter
        pair = first + second
        print(f"{pair} {count}")
        count += 1
        
        if pair == end:
            break

# Run the function
generate_sequences()
