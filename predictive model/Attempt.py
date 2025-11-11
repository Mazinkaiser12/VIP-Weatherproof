#Attempting to create predictive model maths
#VIP Weatherproof
#10/11/2025

print()
print("Attemtping to create predictive model maths")


def commentBlock():
    '''
    I'm thinking of many ways to predict the outcome of the analysis as well as how to make it more efficient
    First, to make the coordinates easier to use we could pool the coorinates into bigger boxes. 
    I actually have two ideas for this
    The better one is actually to treat the coordinates like a big matrix and use a pooling layer to apprioximate
    the most relevant data from entire days in bigger areas
    Think of it like this,
    let's assign every cause a value - In this case I'm going to use the 'Direct cause category' since there are less of them
    we have four grid locations : [ 1,2    1,3 ]  with four identifiers [ 1    1 ] where 1 is companies and 2 is 
                                  [ 2,2    2,3 ]                        [ 2    1 ]
    weather. The idea is this, before our program does the time series analysis it pools together grid data, first day by day,
    and second by cause. https://www.geeksforgeeks.org/deep-learning/cnn-introduction-to-pooling-layer
    Then, we can cut down on how long it takes to process the 50 hours.
    Naturally, in the final deliverable the computer's prediction would be based on the larger area as opposed to the smaller one   
    '''
    

