# Fan Lin, A20271114
# Last Modified: Nov, 29, 2014

# The RSA Implementation in Python3

import random
import math
import time

# the Sieve of Eratosthenes
# Find all prime numbers less than 10000, and store them in a list


# fill Sieve with flags.
# -1 means this index is NOT prime
# 1 means this index is unchecked at initiation
# at last any left 1 means this index IS prime
# numbers 0 and 1 are not prime, by definition

Primes = [] # an empty list to store prime number
Sieve = [-1,-1]
values = 10**4
Sieve += (values - 2) * [1]

k = 0

more = True
limit = math.sqrt(len(Sieve)) # ceiling of k

while more:
    if k == 1 or k == 0: # by definition 0 and 1 are NOT prime numbers
        k += 1 # go to next unchecked number
    elif k >= limit: # exceed the ceiling
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

#print (len(Primes), "primes found.")
#print (Primes)

# Part 1: Prime Numbers
#
# A simple test to see if n is an even number, if even, return False
def test(n):
    #print (type(n))
    return n&1 == 0

# A program using Miller-Rabin test to check if n is prime
# Also, for efficiency, this part is combined with the Sieve of Eratosthenes
#
def primecheck(n):
    #print (type(n))

    if test(n):
        return False

# If n is a number in the sieve, return True
# If n is a multiple of a number in the sieve, return False
    for p in Primes:
        if (n == p):
            return True
        if (n%p == 0):
            return False

    d = n-1
    s = 0
    while test(d): #this will give n-1=(2**s)*d
        d = d//2
        s += 1
    k = 0
    while k<128: # The while loop is to ensure the accuracy
        a = random.randint(2, n-1)
        mod = pow(a, d, n) # mod = (a**d)%n, pow(num,exp,mod)
        if (mod != 1 and mod != n-1):
            i = 0
            while mod != (n-1):
              if i == s-1:
                  return False
              else:
                  i += 1
                  mod = (mod**2)%n
        k += 2
    return True

# Genarate a prime number with k bits
#
def primegen(k):

    start = time.time()
    ceiling = 2**(math.log2(k)+2) # ceiling of tries
    #print (ceiling)
    ceiling_ = int(ceiling)

    while ceiling>0:
        n = random.randint(2**(k-1),2**k) # generate a k bits random number
        #print (n)
        ceiling -= 1
        if not test(n): # Throw all even numbers
            if primecheck(n) == True:
                end = time.time()
                time_delta = end - start
                #print ('Elapsed Time: {:0.2f}s'.format(time_delta))
                return n
    end = time.time()
    time_delta = end - start
    #print ('Elapsed Time: {:0.2f}s'.format(time_delta))
    return ('Fail after {} tries, please try again'.format(ceiling_)) # For efficiency, limit the retrying times 

# Part 2
# Extended Euclidean algorithm
#
def extended_gcd(a, b):
    lastremainder, remainder = abs(a), abs(b)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        # divmod(a, b) returns quotient and remainder of (a, b) when using integer division
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx*(-1 if a < 0 else 1), lasty*(-1 if b < 0 else 1)

# find the modular multiplicative inverse of e while the mod number is n
# This will use the result of function extended_gcd(a, b)
#
def mod_inv(e, n):
	g, x, y = extended_gcd(e, n)
	if g != 1:
		return ('e is not invertible')
	return x % n
    
# generate a (public, private) key pair given two prime numbers
#
def keygen(p, q):
    if not primecheck(p):
        return ('p is not a prime.')
    if not primecheck(q):
        return ('q is not a prime.')
    n = p*q
    pha = (p-1)*(q-1)
    for p in Primes: # find the minimum relatively prime of pha, which will be e
        if pha%p != 0:
            e = p
            break
        elif p == Primes[len(Primes)-1]:
            print ('You need to increase the prime list size.')
    d = mod_inv(e,pha)
    print ('Public Key: ({}, {})'.format(n,e))
    print ('Private Key: ({}, {})'.format(n,d))

# generate a (public, private) key pair given two prime numbers and a given e
#
def keygen_e(p, q, e):
    if not primecheck(p):
        return ('p is not a prime.')
    if not primecheck(q):
        return ('q is not a prime.')
    n = p*q
    pha = (p-1)*(q-1)
    d = mod_inv(e,pha)
    print ('Public Key: ({}, {})'.format(n,e))
    print ('Private Key: ({}, {})'.format(n,d))
    

    #format conversion
def char2unicode_ascii(intext,length):
    outtext=[]
    for i in range(length):
        outtext.append(ord(intext[i]))
    return outtext
  
def unicode2bit(intext,length):
    outbit=[]
    for i in range(length*16):
        outbit.append((intext[int(i/16)]>>(i%16))&1)#one bit to left one time
    return outbit
  
def byte2bit(inchar,length):
    outbit=[]
    for i in range(length*8):
        outbit.append((inchar[int(i/8)]>>(i%8))&1)#one bit to left one time
    return outbit

def bit2unicode(inbit,length):
    out=[]
    temp=0
    for i in range(length):
        temp=temp|(inbit[i]<<(i%16))
        if i%16==15:            
            out.append(temp)
            temp=0
    return out

def bit2byte(inbit,length):
    out=[]
    temp=0
    for i in range(length):
        temp=temp|(inbit[i]<<(i%8))
        if i%8==7:            
            out.append(temp)
            temp=0
    return out

def unicode2char(inbyte,length):
    out=""
    for i in range(length):
        out=out+chr(inbyte[i])
    return out

# the encrpt and decrtpt part
#
def encrypt(n, e, c):
    return (c**e)%n

def decrypt(n, d, m):
    return (m**d)%n
