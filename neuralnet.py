import numpy as np
import random
# from geneticalgo import main
#because a lot of data will be needed, we will use a class approach.
class Full_NN(object):
#A Multi Layer Neural Network class. We use this as for the way we need to handle the variables is better suited.
    def __init__(self, X=24, HL=[128,64,32], Y=24): #a constructor for some default values.
        self.X=X    #inputs
        self.HL=HL  #hidden layers  
        self.Y=Y    #outputs
        
        #we are setting up some class variables for our inputs.
        
        L=[X]+HL+[Y]
        
        #total number of layers. This creates a representation of the network in the format we need it. 
        # i.e array of the format [how many inputs, how mnay hidden layers. how many outputs]
        
        W=[] #initialize a weight array
        
        # may need to change weight initialization method here if doesnt work with outputs

        for i in range(len(L)-1): #we want to be able go to the next layer up so we set one minus
            w=np.random.rand(L[i], L[i+1])      #fill them up with random values, that is why we need the numpy library
            W.append(w)         #add the new values to the array.
        self.W=W    #link the class variable to the current variable.
        Der=[]      #initialize a derivative array. These are needed to calculate the back propagation.
                    # they are the derivatives of the activation function.
        
        
        for i in range(len(L)-1): #same reason as above for every line
            d=np.zeros((L[i], L[i+1])) #we don't need random values, just to have them ready to be used. we fill up with zeros.
        
            Der.append(d)
        
        self.Der=Der
        
        #we will be passing these here as that way the class variable will keep them for us until we need them.
        
        out=[] #initialize output array
        
        for i in range(len(L)): #We don't need to go +1. The outputs are straightforward.
            o=np.zeros(L[i]) #we don't need random values, just to have them ready to be used. we fill up with zeros.
            out.append(o)
        
        self.out=out
    
    def FF(self,x):     #This method will run the network forward
        out=x           #the input layer output is just the input
        self.out[0]=x   #begin the linking of outputs to the class variable for back propagation. (begin with the input layer.)
        for i, w in enumerate(self.W):  # go through (iterate) the network layers via the weights variable
            Xnext = np.dot(out, w)        # calculate product between weights and output for the next output
            # Use leaky relu on hidden layers, but keep output layer linear so negative targets are representable
            if i == len(self.W) - 1:
                out = Xnext
            else:
                out = self.leaky_relu(Xnext)
            self.out[i+1] = out           # pass the result to the class variable to preserve for later (when we do the back propagation).
        return out                      #return the outputs of the layers.
    def BP(self, Er):                   #back propagation method. this works by using theOutput Error (Er)  
                                        #to go backwards through the layers and calculate the errors needed to update the Weights.
                                        #this will return the final error of the input.
        for i in reversed(range(len(self.Der))): # iterate backwards through the layers
            # For the output layer we use a linear activation (derivative = 1).
            # For hidden layers we use the leaky relu derivative.
            out = self.out[i+1]  # layer output for this stage
            if i == len(self.Der) - 1:
                D = Er  # linear output layer: derivative = 1
            else:
                D = Er * self.leaky_relu_der(out)  # apply derivative of activation function to get Delta
            D_fixed = D.reshape(D.shape[0], -1).T  # turn Delta into an array of appropriate size
            this_out = self.out[i]  # current layer output.
            this_out = this_out.reshape(this_out.shape[0], -1)  # reshape to column array for multiplication
            self.Der[i] = np.dot(this_out, D_fixed)  # matrix multiplication and store result
            Er = np.dot(D, self.W[i].T)  # backpropagate error for next iteration
 
    def train_nn(self, x, target, epochs, lr): #training the network. The x is an array, the target is an array the epochs is a number and the lr is a number.
        
        for i in range (epochs): #training loop for as many epochs as we need
        
            S_errors=0 #variable to carry the error we need to report to the user
        
            for j, input in enumerate (x): #iterate through the traning data and inputs
                t=target[j]
                output=self.FF(input) #use the network calculations for forward calculations.
                e=t-output #obtain the overall Network output error
                self.BP(e) # use that error to do the back propagation
                self.GD(lr) #Do gradient descent
      
                S_errors+=self.msqe(t,output) #update the overall error to show the user.
    
    def GD(self, lr=0.05): #Gradient descent
    
        for i in range(len(self.W)): #go through the weights
            W=self.W[i]
            Der=self.Der[i]
            W+= Der*lr #update the weights by applying the learning rate
    
    def leaky_relu(self,x): # activation function (leaky ReLU) alpha 0.01
        return np.maximum(0.01*x, x)
    
    def leaky_relu_der(self, x): #leaky relu function derivative
        return np.where(x>0, 1, 0.01) 
    
    def msqe(self, t, output): #mean square error
        msq=np.average((t-output)**2)
    
        return msq
    
def data_generation():
    # random data generation within some limits
    frame = []
    for i in range(8):
        frame.append(round(random.uniform(-0.38,0.38),3)) # 43 degrees of freedom
        frame.append(round(random.uniform(-2,-0.5),3)) # 143 degrees of freedom below 0 means it cannot angle above coxa
        frame.append(round(random.uniform(-0.5,0),3)) # 28 degrees of freedom 0 means it cannot angle above femer
    return frame

if __name__ == "__main__": 
    sequence = [data_generation() for _ in range(300)]  # generate 301 frames
    
    training_inputs = np.array(sequence[:-1])  # frames 1 to 299 (shape: 300 x 24)
    targets = np.array(sequence[1:])           # frames 2 to 300 (shape: 300 x 24)
    
    print("Sequence-based frame prediction:")
    print("  Sequence length:", len(sequence))
    print("  training_inputs.shape:", training_inputs.shape, "(current frames at time t)")
    print("  targets.shape:", targets.shape, "(next frames at time t+1)")
    # create network with 24 outputs to match target vectors
    nn = Full_NN(24, [128,64,32], 24)

    # prints for testing
    training_inputs = np.asarray(training_inputs)
    print("training_inputs.shape:", training_inputs.shape, "dtype:", training_inputs.dtype)
    print("targets.shape:", np.asarray(targets).shape, "dtype:", np.asarray(targets).dtype)
    if training_inputs.size:
        print("first sample shape:", np.asarray(training_inputs[0]).shape)

    nn.train_nn(training_inputs, targets, 100, 0.01) #trains the network with 0.1 learning rate for 10 epochs
    
    # Testing data to identify if Network trained well.
    # Use a sample that matches the network input size (24).
    test_input = training_inputs[150]
    test_target = targets[150]  # now a 24-element vector
    NN_output = nn.FF(test_input)



print("=============== Testing the Network Screen Output===============")
print("Test input shape:", test_input)
print() 
print("Target output is ", test_target)
print()
print("Neural Network actual output is ", NN_output, "there is an error (not MSQE) of ", test_target-NN_output)
print("=================================================================")

