# Dining Philosophers Comparison
# 2014-04-06
#
from threading import Thread, Semaphore, Condition
from random import uniform
import random, time

#NUM_PHIL = int(input('Number of philosophers='))
#MAX_TIMES_TO_EAT = int(input('Number of meals='))

# right() and left() return index of P_i's right and left forks
# right_T() and left_T() are for Tanenbaum's solution,
# which will return index of P_i's neighbour.
#
def right(i): return i
def left(NUM_PHIL, i): return (i+1) % NUM_PHIL
def right_T(NUM_PHIL, i): return (i+1) % NUM_PHIL
def left_T(NUM_PHIL, i): return (i-1) % NUM_PHIL

# Do we want to announce actions (eating, thinking, getting
# and releasing forks)?
#
ANNOUNCE_ACTIONS = False
ANNOUNCE_ACTIONS1 = False # This is for eating time counter 

# Sleep for uniformly random value between 0 and limit.
#
def pause(id, max_pause):
	sleeptime = random.uniform(0, max_pause)
	time.sleep(sleeptime)

# Philosopher thinks for <= think_time seconds then becomes hungry.
# Optionally announce these events.
#
def think(id, think_time):
	if ANNOUNCE_ACTIONS:
		print('P{} is thinking'.format(id), flush = True)
	pause(id, think_time)
	if ANNOUNCE_ACTIONS:
		print('P{} is hungry'.format(id), flush = True)

# Philosopher eats for <= eat_time seconds
#
def eat(id, times_eaten, eat_time):
	if ANNOUNCE_ACTIONS1:
		print('P{} is eating, time #{}'.format(id, times_eaten),\
			flush = True )
	pause(id, eat_time)

# Get fork to left of identified philosopher; optionally
# announce this.
#
def get_left(NUM_PHIL, id, forks):
	forks[left(NUM_PHIL, id)].acquire()
	if ANNOUNCE_ACTIONS:
		print('P{} got left fork'.format(id), flush = True)

# Get fork to right of identified philosopher; optionally
# announce this.
#
def get_right(id, forks):
	forks[right(id)].acquire()
	if ANNOUNCE_ACTIONS:
		print('P{} got right fork'.format(id), flush = True)

# Release both of philosopher's forks
#
def drop_forks(NUM_PHIL, id, forks):
	forks[right(id)].release()
	forks[left(NUM_PHIL, id)].release()
	if ANNOUNCE_ACTIONS:
		print('P{} dropped forks'.format(id), flush = True)

# General philosopher action: Repeatedly think and eat
#
def philosopher(NUM_PHIL, MAX_TIMES_TO_EAT, get_forks, \
	id, forks, action_time = 1, fork_pause = 1):
	times_eaten = 0
	while MAX_TIMES_TO_EAT < 0 or times_eaten < MAX_TIMES_TO_EAT:
		think(id, action_time)  # think and become hungry

		get_forks(NUM_PHIL, id, forks, fork_pause)

		times_eaten += 1
		eat(id, times_eaten, action_time)
		drop_forks(NUM_PHIL, id, forks)
	if ANNOUNCE_ACTIONS1:
		print('P{} is quitting <--------------------'.format(id), flush = True)
	return


# Strategy 1: No-Holding solution
#
def get_forks1(NUM_PHIL, id, forks, fork_pause = 1):
    while True:
        forks[left(NUM_PHIL, id)].acquire(True)
        pause(id, fork_pause)
        locked = forks[right(id)].acquire(False) 
        if locked: break
        forks[left(NUM_PHIL, id)].release() # if one fails to get the right fork,
        pause(id, fork_pause)               # he will put down the left one and wait a random time 
        if ANNOUNCE_ACTIONS:                # then try again.
            print('P{} will try again'.format(id), flush = True)


# Strategy 2: The napkin solution
#
# napkin = Semaphore(NUM_PHIL-1)
#
# Philosophers action with napkin, need to get a napkin before eating,
# after eating then release the napkin.
#
def philosopher_napkin(NUM_PHIL, MAX_TIMES_TO_EAT, get_forks, \
	id, forks, action_time = 1, fork_pause = 1):
        global napkin
        times_eaten = 0
        while MAX_TIMES_TO_EAT < 0 or times_eaten < MAX_TIMES_TO_EAT:
                think(id, action_time)  # think and become hungry

                get_forks(NUM_PHIL, id, forks, fork_pause)

                times_eaten += 1
                eat(id, times_eaten, action_time)
                drop_forks(NUM_PHIL, id, forks)
                napkin.release()  #release the napkin
        if ANNOUNCE_ACTIONS1:
        	print('P{} is quitting <--------------------'.format(id), flush = True)
        return


def get_forks2(NUM_PHIL, id, forks, fork_pause = 1):
        global napkin
        napkin.acquire() # grab a napkin before getting a fork.
        get_right(id, forks)
        pause(id, fork_pause)
        get_left(NUM_PHIL, id, forks)

# Strategy 3: The even/odd solution
#
def get_forks3(NUM_PHIL, id, forks, fork_pause = 1):
    if id%2 == 0: # righties will pick up right fork first
        get_right(id, forks)
        pause(id, fork_pause)
        get_left(NUM_PHIL, id, forks)
    else: # lefties will pick up left fork first
        get_left(NUM_PHIL, id, forks)
        pause(id, fork_pause)
        get_right(id, forks)

# Strategy 4: Tanenbaum's solution
#
def test(NUM_PHIL, id):  # Check neighbors鈥� states, when both are NOT eating, return True.
        global state, can_eat
        return state[id] == 'hungry' and state[right_T(NUM_PHIL, id)] != 'eating' \
               and state[left_T(NUM_PHIL, id)] != 'eating'

def get_forks4(NUM_PHIL, id):
        global state, can_eat
        state[id] = 'hungry'  # when a philosopher is hungry, he will try to acquire 2 forks 
        with can_eat[id]:
                while not test(NUM_PHIL, id):
                        can_eat[id].wait()  # Block if forks were not acquired 
                state[id] = 'eating'  # if both forks are acquired, starts eating 

def put_forks(NUM_PHIL, id):
        global state, can_eat
        state[id]= 'thinking'  # finish eating
        with can_eat[id]:
                can_eat[id].notify()
                with can_eat[right_T(NUM_PHIL, id)]:  # See if right neighbour can now eat
                        if test(NUM_PHIL, right_T(NUM_PHIL, id)):
                                can_eat[right_T(NUM_PHIL, id)].notify()
                with can_eat[left_T(NUM_PHIL, id)]:  # See if left neighbour can now eat 
                        if test(NUM_PHIL, left_T(NUM_PHIL, id)):
                                can_eat[left_T(NUM_PHIL, id)].notify()
            
# state = ['thinking']*(NUM_PHIL)
# can_eat = [Condition() for i in range(NUM_PHIL)]
# Philosophers action for Tanenbaum's solution. A philosopher tests his neighbours rather 
# than left and right forks to see if he could eat.
#
def philosopher_Tanenbaum(NUM_PHIL, MAX_TIMES_TO_EAT, \
	id, action_time = 1, fork_pause = 1):
        times_eaten = 0
        while MAX_TIMES_TO_EAT < 0 or times_eaten < MAX_TIMES_TO_EAT:
                think(id, action_time)  # think and become hungry

                get_forks4(NUM_PHIL, id)

                times_eaten += 1
                eat(id, times_eaten, action_time)
                put_forks(NUM_PHIL, id)
        if ANNOUNCE_ACTIONS1:
        	print('P{} is quitting <--------------------'.format(id), flush = True)
        return


# Run a trial of dining philosophers given a particular function
# for getting forks.
#
# Params:
#   get_forks: get_forks1 ~ get_forks3; a function
#       that takes arguments (NUM_PHI, id, forks, fork_pause = 1) and
#       implements a strategy for getting the right and left
#       forks.
#   action_time: max seconds to eat or think
#   fork_pause: max seconds to pause between getting forks
#
def go(NUM_PHIL, MAX_TIMES_TO_EAT, name = 'No Holding', phil_act = philosopher, \
       get_forks = get_forks1, action_time = 1, fork_pause = 1):
    start = time.time()

    random.seed(123)
    forks = [Semaphore(1) for i in range(NUM_PHIL)]
    phils = [Thread(target = phil_act, \
				args = [NUM_PHIL, MAX_TIMES_TO_EAT, get_forks, \
				id, forks, action_time, fork_pause] )
				for id in range(NUM_PHIL) ]

    for phil in phils:
        phil.start()
    for phil in phils:
        phil.join()

    end = time.time()
    time_delta = end-start
    #print ('{:0.4f}'.format(time_delta))
    print ('<{}> Time Elapsed: {:0.2f} s'.format(name, time_delta), flush = True)

# Run a trial of dining philosophers with Tanenbaum's solution.
# A little different with the regular one.
#
def go_Tanenbaum(NUM_PHIL, MAX_TIMES_TO_EAT, action_time = 1, fork_pause = 1):
    start = time.time()

    random.seed(123)
    phils = [Thread(target = philosopher_Tanenbaum, \
				args = [NUM_PHIL, MAX_TIMES_TO_EAT, \
				id, action_time, fork_pause] )
				for id in range(NUM_PHIL) ]

    for phil in phils:
        phil.start()
    for phil in phils:
        phil.join()

    end = time.time()
    time_delta = end-start
    #print ('{:0.4f}'.format(time_delta))
    print ('<Tanenbuam> Time Elapsed: {:0.2f} s'.format(time_delta), flush = True)
    
def main(NUM_PHIL = 5, MAX_TIMES_TO_EAT = 10):
        global napkin, state, can_eat

        print('Please wait patiently.')
        # No-holding
        go(NUM_PHIL, MAX_TIMES_TO_EAT)
        # Napkin
        napkin = Semaphore(NUM_PHIL-1) # napkin is set to NUM_PHIL-1
        go(NUM_PHIL, MAX_TIMES_TO_EAT, name = 'Napkin', \
        	phil_act = philosopher_napkin, get_forks = get_forks2)
        # Even/Odd
        go(NUM_PHIL, MAX_TIMES_TO_EAT, name = 'Even/Odd', \
        	phil_act = philosopher, get_forks = get_forks3)
        # Tanenbaum
        state = ['thinking']*(NUM_PHIL) # we will define 3 states as 'thinking''eating'and'hungry'
        can_eat = [Condition() for i in range(NUM_PHIL)] # set condition variables.
        go_Tanenbaum(NUM_PHIL, MAX_TIMES_TO_EAT)

# A for-loop to run diffent combinations of N and M.
def loop_try():
	for n in range(2,11):
		for m in range(11):
			print ('number of philosophers = {}, number of meals = {}.'.format(n, 2*m))
			main (NUM_PHIL = n, MAX_TIMES_TO_EAT = 2*m)

def loop_try_more():
	for n in range(3, 9):
		for m in range(5):
			print ('number of philosophers = {}, number of meals = {}.'.format(5*n, 5*m))
			main (NUM_PHIL = 5*n, MAX_TIMES_TO_EAT = 5*m)
