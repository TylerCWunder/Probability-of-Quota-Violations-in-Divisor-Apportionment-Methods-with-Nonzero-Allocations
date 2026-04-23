import random
import numpy as np

#Pick M
M=5

#defining divisor function
def divisor_funct (X):
     #return np.sqrt(X*(X+1)) #Huntington-Hill
     #return X #Adams
     #return X+0.5 #Webster
     return (2*X*(X+1))/(2*X +1) #Dean's
     #return X+1 #Jeffersons

#define random populations

alpha = 1  #Dirichlet Distribution Paramater
beta = 1  #Exponential Distribution Paramater
a_0 = 1   #Parameter for uniform (a_0, b_0)
b_0 = 100  #Parameter for uniform (a_0, b_0)
def randpops(m):
     #return [1,random.uniform(a_0,b_0), random.uniform(a_0,b_0) ] #uniform (1,x,y)
     #return [random.uniform(a_0,b_0),random.uniform(a_0,b_0), random.uniform(a_0,b_0) ]
     #return m*np.random.dirichlet([alpha,alpha,alpha])   
     return [np.random.exponential(beta),np.random.exponential(beta),np.random.exponential(beta) ]    #p_i IID, exponential



#Defining the apportionment
def app (R,A,B, m):             
    Rb=1
    Ab=1
    Bb=1
    pop=np.asarray([R,A,B])
    for i in range(0, m-3):
        seats=np.asarray([Rb,Ab,Bb])
        Pri = pop/divisor_funct(seats)
        if Pri[0]==Pri.max():
            Rb=Rb+1
        if Pri[1]==Pri.max():
            Ab=Ab+1
        if Pri[2]==Pri.max():
            Bb=Bb+1
    return np.asarray([Rb,Ab,Bb])

#defining stealing method apportionment
def stealapp (A,B,m):
    Ab=1
    Bb=1
    pop=np.asarray([A,B])
    for i in range(0, m-3+1):
        seats=np.asarray([Ab,Bb])
        Pri = pop/divisor_funct(seats)
        if Pri[0]==Pri.max():
            Ab=Ab+1
        if Pri[1]==Pri.max():
            Bb=Bb+1
    return np.asarray([1,seats[0], seats[1]])

#Running sample:



qvio_g=0

trials=100000

for i in range (0, trials):
    A_initial=randpops(M)
    A=[np.min(A_initial),np.median(A_initial), np.max(A_initial)]
    appt=app(A[0], A[1], A[2], M)
    P=A[0]+A[1]+A[2]
    Quotas= np.asarray([(M/P)*A[0],(M/P)*A[1], (M/P)*A[2] ])
    LQ = np.asarray([np.floor( Quotas[0]), np.floor( Quotas[1]), np.floor( Quotas[2]) ])
    if appt[0]<LQ[0] or appt[1]<LQ[1] or appt[2]<LQ[2]:
        if appt[0] == 1:
            appt_steal = stealapp(A[1],A[2],M)
            if appt_steal[1] == appt[1] and appt_steal[2] == appt[2]:
                qvio_g=qvio_g+1

#Sample Conclusions:
Prob=qvio_g/(trials)

#(note for confidence interval number of trials must be large to be accurate)

err = 1.96*(np.sqrt( (Prob*(1-Prob))/(trials)   ))

print("Sample probability is", Prob)
print("Confidence interval is:", "(", Prob-err, ",", Prob+err, ")")