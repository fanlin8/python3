# An RSA Implementation by Python3
In this program, the generation of large prime numbers and the implementation of the RSA algorithm are realized.

# Program listing
## `primecheck (n)` 
Check if number n is prime, if it is, then the function will return True.
## `primegen (k)`
Generate a k-bit prime number.
## `keygen (p, q)`
Generate a (public, private) key pair with two given prime numbers (p, q).
## `encrypt (n, e, c)`
Encrypt a single character c with a public key (n, e), then return the cyphertext.
## `decrypt (n, d, m)`
Take a private key (n, d) and the encrypted character m, then return the corresponding plaintext.

