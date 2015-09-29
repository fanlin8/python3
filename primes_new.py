# codes must run in linux evironment!!!
# Fan Lin, A20271114
# Feb, 24, 2014

# the Sieve of Eratosthenes
# multiprocessing version
# Find all prime numbers less than 100000, and return the runtimes.

import multiprocessing.sharedctypes

# set up global variables
psize = int(input('Poolsize='))
chsize = int(input('Chunksize='))

# import math # for the function math.sqrt()

# find prime numbers in a given list (the sieve), with length n
# a single run will remove all multiples of k, k+1, k+2, 鈥�, k+chunksize-1 (or n/2) 
def findprimes(m):
    global Sieve, chsize
    
    k = m*chsize  # starting value of k is decided by chunksize

    more = True
    ceiling = len(Sieve)//2 # ceiling of k
    # ceiling = math.sqrt(len(Sieve)) # ceiling of k, now is limited by sqrt(n)

    while more:

        if k == 1 or k == 0: # by definition 0 and 1 are NOT prime numbers
            k += 1 # go to next unchecked number
        elif k >= ceiling or k >= (m+1)*chsize: # exceed the ceiling or the chunksize
            more = False # work is done
        elif Sieve[k] != -1: # make sure the number has NOT been checked
            idx = 2*k # start from 2*k
            while idx < len(Sieve):
                Sieve[idx] = -1 # marked as -1 if NOT prime
                idx += k
            k += 1
        else:
            k += 1

#---
    #return Sieve

        
    #print (Sieve)

    #for n in range(len(Sieve)):
        #if Sieve[n] > 0:
            #Primes += [n]

    #print (len(Primes), "primes found.")
    #print (Primes)
#---

            
from multiprocessing import Pool 

def mult_find(poolsize = psize, chunksize = chsize): # multiprocessing part
    global Sieve, Primes, values, chsize, psize

    #m = values//chunksize

    # fill Sieve with flags.
    # -1 means this index is NOT prime
    # 1 means this index is unchecked at initiation
    # at last any left 1 means this index IS prime
    # numbers 0 and 1 are not prime, by definition
    
    Primes = [] # an empty list to store prime numbers
    Sieve = [-1,-1]
    values = 10**5
    Sieve += (values - 2) * [1]
    Sieve = multiprocessing.sharedctypes.RawArray('l', Sieve) # a shared array

    pool = Pool(processes = poolsize) # start multiprocessing
    C = pool.map(findprimes, range(values//chunksize)) # the whole list is divided into chunks 
    pool.close()                                       # then run the findprimes() function parallelly in different chunks
    pool.join()                                        # each run start from 0, chunksize, 2*chunksize...

    for n in range(len(Sieve)): # put all 1s into the list Primes
        if Sieve[n] > 0:
            Primes += [n] 

    print (len(Primes), "primes found.")

#---
    #print (sum(Primes))
    #print (Primes)
#---

from time import time 

def timer(poolsize = psize, chunksize = chsize): # start a timer
	start = time()
	C_timer = mult_find(poolsize, chunksize)
	end = time()
	time_delta = 1000*(end-start)
	print ('(MAP) Elapsed: {:0.1f} ms'.format(time_delta))
	return time_delta

def ave_time(poolsize = psize, chunksize = chsize, nbr_trials = 5): # Run nbr_trials times and print average runtimes.
	print ('(MAP) With {} processes'.format(poolsize))
	times = [timer(poolsize,chunksize) for i in range(0, nbr_trials)]
	average = sum(times)/len(times)
	print ('(MAP) Average of {} runs is {:0.1f} ms'.\
		format(nbr_trials, average))

ave_time()

#---
	#return average
#---

#for i in range(1,21): # a for-loop to run different poolzises and chunksizes
    #for n in range(6):
        #print(i)
        #print(10**n)
        #ave_time(poolsize = i, chunksize = 10**n)
 
