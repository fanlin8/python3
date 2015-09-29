import math

Primes = [] # an empty list to store prime number
Sieve = [-1,-1]
values = 10**3
Sieve += (values - 2) * [1]

k = 0

more = True
ceiling = math.sqrt(len(Sieve))

while more:
    if k == 1 or k == 0: # by definition 0 and 1 are NOT prime numbers
        k += 1 # go to next unchecked number
    elif k >= ceiling: # exceed the ceiling
        more = False # work is done
    elif Sieve[k] != -1: # make sure the number has NOT been checked
        idx = 2*k # start from 2*k
        while idx < len(Sieve):
            Sieve[idx] = -1 # marked as -1 if NOT prime
            idx += k
        k += 1
    else:
        k += 1

#print (Sieve)

for n in range(len(Sieve)):
    if Sieve[n] > 0:
        Primes += [n]

print (len(Primes), "primes found.")
print (Primes)
