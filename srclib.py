'''
A library of some useful functions that don't necessarily have anything to do with graphs.
'''

#Wrapper function for timing purposes.
import timeit
def timer(label=None):
    def decorate(func):
        def wrapper(*args, **kwargs):
            before = timeit.default_timer()
            returnVal = func(*args, **kwargs)
            after = timeit.default_timer()
            if label == None:
                print('Elapsed:', after - before, "seconds.")
            elif isinstance(label, str):
                print('Elapsed:', after - before, "seconds.", '(' + label + ')')
            return returnVal
        return wrapper
    return decorate

#The functions indexOfLastOne and binarySequences are slightly modified based on the work of a kind reddit user who did not ask to be credited personally.

#Finds index of last one in an array.
def indexOfLastOne(arr, below):
    for i in range(below,-1,-1):
        if(arr[i] == 1):
            return i;
    return -1;

#Create all n-tuples with k ones and n-k zeros.
def binarySequences(n,k):
    if(k > n or k < 0 or n < 0):
        raise ValueError;
    choice = [1]*k + [0]*(n-k);
    yield choice;
    while(True):
        #find last zero and count ones
        oneCount = 0;
        lastZero = -1;
        for i in range(len(choice)-1,-1,-1):
            if(choice[i] == 1):
                oneCount += 1;
            elif(choice[i] == 0):
                lastZero = i;
                break;
        #find last one before the zero
        lastOne = indexOfLastOne(choice, lastZero);
        if(lastOne == -1):
            break;
        #move 1 forward and bring back all 1s
        choice[lastOne] = 0;
        choice = choice[:lastOne+1]+[1]*(1+oneCount)+[0]*(n-(2+lastOne+oneCount));
        yield choice;
