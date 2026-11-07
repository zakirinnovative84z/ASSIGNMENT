import time
from functools import wraps

def ttl_cache(seconds):

    # Your code here

    pass


@ttl_cache(seconds=5)
def add(x, y):
    print("Calculating...")
    return x + y


print(add(x=2, y=3))
print(add(y=3, x=2))

time.sleep(6)

print(add(x=2, y=3))