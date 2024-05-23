import numpy as np
import time
from colorama import Fore,Style
from typing import List, Union
import math
# BUILD -----
def TrainPLAN(
    Inputs: List[Union[int, float]], 
    Labels: List[Union[int, float, str]], # At least two.. and one hot encoded
    ClassCount: int,
    Layers: List[str],
    Neurons: List[Union[int, float]],
    ThresholdSigns: List[str],
    ThresholdValues: List[Union[int, float]],
    Normalizations: List[str],
    Activations: List[str]
) -> str:
        
    infoPLAN = """
    Creates and configures a PLAN model.
    
    Args:
        Inputs (list[num]): List of input data.
        Labels (list[num]): List of labels. (one hot encoded)
        ClassCount (int): Number of classes.
        Layers (list[str]): List of layer names. (options: 'fex' (Feature Extraction), 'cat' (Catalyser))
        Neurons (list[num]): List of neuron counts for each layer.
        ThresholdSigns (list[str]): List of threshold signs.
        ThresholdValues (list[num]): List of threshold values.
        Normalizations (List[str]): Whether normalization will be performed at indexed layers ("y" or "n").
        Activations (list[str]): List of activation functions.
    
    Returns:
        list([num]): (Weight matrices list, TrainPredictions list.).
        error handled ?: Process status ('e')
"""
        
    LastNeuron = Neurons[-1:][0]
    if LastNeuron != ClassCount:
            print(Fore.RED + "ERROR108: Last layer of neuron count must be equal class count. from: TrainPLAN",infoPLAN)
            return 'e'
    
    if len(Normalizations) != len(ThresholdValues):
        
            print(Fore.RED + "ERROR307: Normalization list length must be equal to length of ThresholdSigns List,ThresholdValues List,Layers List,Neurons List. from: TrainPLAN",infoPLAN)
            return 'e'
    
    if len(Inputs) != len(Labels):
        print(Fore.RED + "ERROR301: Inputs list and Labels list must be same length.",infoPLAN)
        return 'e'
    
    for i, Value in enumerate(ThresholdValues):
        
        if Normalizations[i] != 'y' and Normalizations[i] != 'n':
                print(Fore.RED + "ERROR105: Normalization list must be 'y' or 'n'.",infoPLAN)
                return 'e'
            
        if ThresholdSigns[i] == 'none':
            print(Fore.MAGENTA + "WARNING102: We are advise to do not put 'none' Threshold sign. But some cases improves performance of the model from: TrainPLAN",infoPLAN  + Style.RESET_ALL)
            time.sleep(3)
            
        if isinstance(Value, str):
            print(Fore.RED + "ERROR201: Threshold values must be numeric. from: TrainPLAN")
            return 'e'
        
        if isinstance(Neurons[i], str):
            print(Fore.RED + "ERROR202: Neurons list must be numeric.")
            return 'e'
    
    if len(ThresholdSigns) != len(ThresholdValues):
        print(Fore.RED + "ERROR302: Threshold signs list and Threshold Values list must be same length. from: TrainPLAN",infoPLAN)
        return 'e'
    
    if len(Layers) != len(Neurons):
        print(Fore.RED + "ERROR303: Layers list and Neurons list must same length. from: TrainPLAN",infoPLAN)
        return 'e'
    
    if len(ThresholdValues) != len(Layers) or len(ThresholdSigns) != len(Layers):
        print(Fore.RED + "ERROR306: Threshold Values and Threshold Signs lists length must be same Layers list length. from: TrainPLAN",infoPLAN)
        return 'e'
    
    
    for Activation in Activations:
        if Activation != 'softmax' and Activation != 'sigmoid' and Activation != 'relu' and Activation != 'none':
            print(Fore.RED + "ERROR108: Activations list must be 'sigmoid' or 'softmax' or 'relu' or 'none' from: TrainPLAN",infoPLAN)
            return 'e'
    

    for index, Neuron in enumerate(Neurons):
        if Neuron < 1:
            print(Fore.RED + "ERROR101: Neurons list must be positive non zero integer. from: TrainPLAN",infoPLAN)
            return 'e'
        
        if index + 1 != len(Neurons) and Neuron % 2 != 0:
            print(Fore.MAGENTA + "WARNING101: We strongly advise to do Neuron counts be should even numbers. from: TrainPLAN",infoPLAN)
            time.sleep(3)
            
        if Neuron < ClassCount:
            print(Fore.RED + "ERROR102: Neuron count must be greater than class count(For PLAN). from: TrainPLAN")
            return 'e'
        
        if Layers[index] != 'fex' and Layers[index] != 'cat':
            print(Fore.RED + "ERROR107: Layers list must be 'fex'(Feature Extraction Layer) or 'cat' (Catalyser Layer). from: TrainPLAN",infoPLAN)
            return 'e'
    
    if len(ThresholdSigns) != len(ThresholdValues):
        print(Fore.RED + "ERROR305: Threshold signs list and Threshold values list must be same length. from: TrainPLAN",infoPLAN)
        return 'e'
    
    
    for i, Sign in enumerate(ThresholdSigns):
        if Sign != '>' and Sign != '<' and Sign != '==' and Sign != '!=' and Sign != 'none':
            print(Fore.RED + "ERROR104: Threshold signs must be '>' or '<' or '==' or '!='. or 'none' from: TrainPLAN",infoPLAN)
            return 'e'
        
        if Layers[i] == 'fex' and Sign == 'none':
            print(Fore.RED + "ERROR109: at layer type 'fex', pairing with 'none' Threshold is not acceptlable. if you want to 'none' put '==' and make threshold value '0'. from: TrainPLAN ",infoPLAN)
            return 'e'
        
    UniqueLabels = set()
    for sublist in Labels:
      
        UniqueLabels.add(tuple(sublist))
    
    
    UniqueLabels = list(UniqueLabels)
    
    Labels = [tuple(sublist) for sublist in Labels]
    
    
    if len(UniqueLabels) != ClassCount:
        print(Fore.RED + "ERROR106: Label variety length must be same Class Count. from: TrainPLAN",infoPLAN)
        return 'e'
    
    Inputs[0] = np.array(Inputs[0])
    Inputs[0] = Inputs[0].ravel()
    InputSize = len(Inputs[0])
    
    W = WeightIdentification(len(Layers) - 1,ClassCount,Neurons,InputSize)
    Divides = SynapticDividing(ClassCount,W)
    TrainedWs = [1] * len(W)
    print(Fore.GREEN + "Train Started with 0 ERROR" + Style.RESET_ALL,)
    TrainPredictions = [1] * len(Labels)
    true = 0
    Inputs, Labels = AutoBalancer(Inputs, Labels, ClassCount)
    StartTime = time.time()
    for index, inp in enumerate(Inputs):
        UniStartTime = time.time()
        inp = np.array(inp)
        inp = inp.ravel()
        
        if InputSize != len(inp):
            print(Fore.RED +"ERROR304: All input matrices or vectors in inputs list, must be same size. from: TrainPLAN",infoPLAN + Style.RESET_ALL)
            return 'e'
        
        
        for Ulindex, Ul in enumerate(UniqueLabels):
            
            if Ul == Labels[index]:
                for Windex, w in enumerate(W):
                    for i, ul in enumerate(Ul):
                        if ul == 1.0:
                            k = i
                    Cs = Divides[int(k)][Windex][0]
       
                    W[Windex] = SynapticPruning(w, Cs, 'row', int(k),ClassCount)

        NeuralLayer = inp
        
        for Lindex, Layer in enumerate(Layers):
            
            if Normalizations[Lindex] == 'y':
                NeuralLayer = Normalization(NeuralLayer)
                
            if Activations[Lindex] == 'relu':
                NeuralLayer = Relu(NeuralLayer)
            elif Activations[Lindex] == 'sigmoid':
                NeuralLayer = Sigmoid(NeuralLayer)
            elif Activations[Lindex] == 'softmax':
                NeuralLayer = Softmax(NeuralLayer)
                
            if Layer == 'fex':
                NeuralLayer,W[Lindex] = Fex(NeuralLayer, W[Lindex], ThresholdSigns[Lindex], ThresholdValues[Lindex])
            elif Layer == 'cat':
                NeuralLayer,W[Lindex] = Cat(NeuralLayer, W[Lindex], ThresholdSigns[Lindex], ThresholdValues[Lindex],1)
                
        RealOutput = np.argmax(Labels[index])
        PredictedOutput = np.argmax(NeuralLayer)
        if RealOutput == PredictedOutput:
            true += 1
        Acc = true / len(Labels)
        TrainPredictions[index] = PredictedOutput+1
        
        if index == 0:
            for i, w in enumerate(W):
                TrainedWs[i] = w
                     
        else:
            for i, w in enumerate(W):
                TrainedWs[i] = TrainedWs[i] + w
            
                
        W = WeightIdentification(len(Layers) - 1,ClassCount,Neurons,InputSize)
         
               
        UniEndTime = time.time()
        
        CalculatingEst = round((UniEndTime - UniStartTime) * (len(Inputs) - index),3)
        
        if CalculatingEst < 60:
            print('\rest......(sec):',CalculatingEst,'\n',end= "")
            print('\rTrain Accuracy: ' ,Acc ,"\n", end="")
        
        elif CalculatingEst > 60 and CalculatingEst < 3600:
            print('\rest......(min):',CalculatingEst/60,'\n',end= "")
            print('\rTrain Accuracy: ' ,Acc ,"\n", end="")
        
        elif CalculatingEst > 3600:
            print('\rest......(h):',CalculatingEst/3600,'\n',end= "")
            print('\rTrain Accuracy: ' ,Acc ,"\n", end="")
        
    EndTime = time.time()
    
    CalculatingEst = round(EndTime - StartTime,2)
    
    print(Fore.GREEN + " \nTrain Finished with 0 ERROR\n")
    
    if CalculatingEst < 60:
        print('Total training time(sec): ',CalculatingEst)
        
    elif CalculatingEst > 60 and CalculatingEst < 3600:
        print('Total training time(min): ',CalculatingEst/60)
        
    elif CalculatingEst > 3600:
        print('Total training time(h): ',CalculatingEst/3600)
        
    if Acc > 0.8:
        print(Fore.GREEN + '\nTotal Train Accuracy: ' ,Acc, '\n',Style.RESET_ALL)
    
    elif Acc < 0.8 and Acc > 0.6:
        print(Fore.MAGENTA + '\nTotal Train Accuracy: ' ,Acc, '\n',Style.RESET_ALL)
    
    elif Acc < 0.6:
        print(Fore.RED+ '\nTotal Train Accuracy: ' ,Acc, '\n',Style.RESET_ALL)
    
    
    

    return TrainedWs,TrainPredictions
        
# FUNCTIONS -----

def WeightIdentification(
    LayerCount,      # int: Number of layers in the neural network.
    ClassCount,      # int: Number of classes in the classification task.
    Neurons,         # list[num]: List of neuron counts for each layer.
    InputSize        # int: Size of the input data.
) -> str:
    """
    Identifies the weights for a neural network model.

    Args:
        LayerCount (int): Number of layers in the neural network.
        ClassCount (int): Number of classes in the classification task.
        Neurons (list[num]): List of neuron counts for each layer.
        InputSize (int): Size of the input data.

    Returns:
        list([numpy_arrays],[...]): Weight matices of the model. .
    """

    
    Wlen = LayerCount + 1
    W = [None] * Wlen
    W[0] = np.ones((Neurons[0],InputSize))
    ws = LayerCount - 1
    for w in range(ws):
        W[w + 1] = np.ones((Neurons[w + 1],Neurons[w]))
    W[LayerCount] = np.ones((ClassCount,Neurons[LayerCount - 1]))
    return W

def SynapticPruning(
    w,            # list[list[num]]: Weight matrix of the neural network.
    Cs,           # list[list[num]]: Synaptic connections between neurons.
    Key,          # int: Key for identifying synaptic connections.
    Class,        # int: Class label for the current training instance.
    ClassCount   # int: Total number of classes in the dataset.
    
) -> str:
    infoPruning = """
    Performs synaptic pruning in a neural network model.

    Args:
        w (list[list[num]]): Weight matrix of the neural network.
        Cs (list[list[num]]): Synaptic connections between neurons.
        Key (str): Key for identifying synaptic row or col connections.
        Class (int): Class label for the current training instance.
        ClassCount (int): Total number of classes in the dataset.

    Returns:
        numpy array: Weight matrix.
    """

    
    Class += 1 # because index start 0
    
    if Class != ClassCount and Class != 1:
            
            Ce = Cs / Class
     
            w[int(Ce)-1::-1,:] = 0
          
            w[Cs:,:] = 0
    

    else:
        
        if Class == 1:
            if Key == 'row':
    
                w[Cs:,:] = 0
    
            elif Key == 'col':
    
                w[:,Cs] = 0
    
            else:
                print(Fore.RED + "ERROR103: SynapticPruning func's Key parameter must be 'row' or 'col' from: SynapticPruning" + infoPruning)
                return 'e'
        else:
            if Key == 'row':
    
                w[Cs:,:] = 0
    
                Ce = int(round(w.shape[0] - Cs / ClassCount))
                w[Ce-1::-1,:] = 0
    
            elif Key == 'col':
    
                w[:,Cs] = 0
    
            else:
                print(Fore.RED + "ERROR103: SynapticPruning func's Key parameter must be 'row' or 'col' from: SynapticPruning" + infoPruning + Style.RESET_ALL)
                return 'e'
    return w

def SynapticDividing(
    ClassCount,    # int: Total number of classes in the dataset.
    W              # list[list[num]]: Weight matrix of the neural network.
) -> str:
    """
    Divides the synaptic weights of a neural network model based on class count.

    Args:
        ClassCount (int): Total number of classes in the dataset.
        W (list[list[num]]): Weight matrix of the neural network.

    Returns:
        list: a 3D list holds informations of divided net.
    """

    
    Piece = [1] * len(W)
    #print('Piece:' + Piece)
    #input()
    # Boş bir üç boyutlu liste oluşturma
    Divides = [[[0] for _ in range(len(W))] for _ in range(ClassCount)]
    
    for i in range(len(W)):
            

            Piece[i] = int(math.floor(W[i].shape[0] / ClassCount))

    Cs = 0
    # j = Classes, i = Weights, [0] = CutStart.

    for i in range(len(W)):
        for j in range(ClassCount):
            Cs = Cs + Piece[i]
            Divides[j][i][0] = Cs
            #print('Divides: ' + j + i + ' = ' + Divides[j][i][0])
            #input()
        
        j = 0
        Cs = 0
        
    return Divides
        

def Fex(
    Input,               # list[num]: Input data.
    w,                   # list[list[num]]: Weight matrix of the neural network.
    ThresholdsSign,      # str: Sign for threshold comparison ('<', '>', '==', '!=').
    ThresholdValue       # num: Threshold value for comparison.
) -> tuple:
    """
    Applies feature extraction process to the input data using synaptic pruning.

    Args:
        Input (list[num]): Input data.
        w (list[list[num]]): Weight matrix of the neural network.
        ThresholdsSign (str): Sign for threshold comparison ('<', '>', '==', '!=').
        ThresholdValue (num): Threshold value for comparison.

    Returns:
        tuple: A tuple (vector) containing the neural layer result and the updated weight matrix.
    """

    if ThresholdsSign == '<':
        PruneIndex = np.where(Input < ThresholdValue)
    elif ThresholdsSign == '>': 
        PruneIndex = np.where(Input > ThresholdValue)
    elif ThresholdsSign == '==':
        PruneIndex = np.where(Input == ThresholdValue)
    elif ThresholdsSign == '!=':
        PruneIndex = np.where(Input != ThresholdValue)

    w = SynapticPruning(w, PruneIndex, 'col', 0, 0)

    NeuralLayer = np.dot(w, Input)
    return NeuralLayer,w

def Cat(
    Input,               # list[num]: Input data.
    w,                   # list[list[num]]: Weight matrix of the neural network.
    ThresholdsSign,      # str: Sign for threshold comparison ('<', '>', '==', '!=').
    ThresholdValue,      # num: Threshold value for comparison.
    isTrain              # int: Flag indicating if the function is called during training (1 for training, 0 otherwise).
) -> tuple:
    """
    Applies categorization process to the input data using synaptic pruning if specified.

    Args:
        Input (list[num]): Input data.
        w (list[list[num]]): Weight matrix of the neural network.
        ThresholdsSign (str): Sign for threshold comparison ('<', '>', '==', '!=').
        ThresholdValue (num): Threshold value for comparison.
        isTrain (int): Flag indicating if the function is called during training (1 for training, 0 otherwise).

    Returns:
        tuple: A tuple containing the neural layer (vector) result and the possibly updated weight matrix.
    """

    if ThresholdsSign == '<':     
        PruneIndex = np.where(Input < ThresholdValue)
    elif ThresholdsSign == '>':     
        PruneIndex = np.where(Input > ThresholdValue)
    elif ThresholdsSign == '==':
        PruneIndex = np.where(Input == ThresholdValue)
    elif ThresholdsSign == '!=':     
        PruneIndex = np.where(Input != ThresholdValue)
    if isTrain == 1 and ThresholdsSign != 'none':
     
            w = SynapticPruning(w, PruneIndex, 'col', 0, 0)
     
    
    NeuralLayer = np.dot(w, Input)
    return NeuralLayer,w


def Normalization(
    Input  # list[num]: Input data to be normalized.
):
    """
    Normalizes the input data using maximum absolute scaling.

    Args:
        Input (list[num]): Input data to be normalized.

    Returns:
        list[num]: Scaled input data after normalization.
    """

   
    AbsVector = np.abs(Input)
    
    MaxAbs = np.max(AbsVector)
    
    ScaledInput = Input / MaxAbs
    
    return ScaledInput


def Softmax(
    x  # list[num]: Input data to be transformed using softmax function.
):
    """
    Applies the softmax function to the input data.

    Args:
        x (list[num]): Input data to be transformed using softmax function.

    Returns:
        list[num]: Transformed data after applying softmax function.
    """


    MaxX = np.max(x)
    
    x -= MaxX
    
    ExpX = np.exp(x)
    
    SumExpX = np.sum(ExpX)
    
    SoftmaxX = ExpX / SumExpX
    
    return SoftmaxX


def Sigmoid(
    x  # list[num]: Input data to be transformed using sigmoid function.
):
    """
    Applies the sigmoid function to the input data.

    Args:
        x (list[num]): Input data to be transformed using sigmoid function.

    Returns:
        list[num]: Transformed data after applying sigmoid function.
    """

    PositiveMask = x >= 0
    NegativeMask = ~PositiveMask
   
    ExpXPositive = np.exp(-np.clip(x[PositiveMask], -709, None))
    ExpXNegative = np.exp(np.clip(x[NegativeMask], None, 709))

    SigmoidX = np.zeros_like(x, dtype=float)
    SigmoidX[PositiveMask] = 1 / (1 + ExpXPositive)
    SigmoidX[NegativeMask] = ExpXNegative / (1 + ExpXNegative)
   
    return SigmoidX


def Relu(
    x  # list[num]: Input data to be transformed using ReLU function.
):
    """
    Applies the Rectified Linear Unit (ReLU) function to the input data.

    Args:
        x (list[num]): Input data to be transformed using ReLU function.

    Returns:
        list[num]: Transformed data after applying ReLU function.
    """

    
    return np.maximum(0, x)


def TestPLAN(
    TestInputs,         # list[list[num]]: Test input data.
    TestLabels,         # list[num]: Test labels.
    Layers,             # list[str]: List of layer names.
    ThresholdSigns,     # list[str]: List of threshold signs for each layer.
    ThresholdValues,    # list[num]: List of threshold values for each layer.
    Normalizations,    # str: Whether normalization will be performed ("y" or "n").
    Activation,         # str: Activation function list for the neural network.
    W                  # list[list[num]]: Weight matrix of the neural network.
) -> tuple:
    infoTestModel =  """
    Tests the neural network model with the given test data.

    Args:
        TestInputs (list[list[num]]): Test input data.
        TestLabels (list[num]): Test labels.
        Layers (list[str]): List of layer names.
        ThresholdSigns (list[str]): List of threshold signs for each layer.
        ThresholdValues (list[num]): List of threshold values for each layer.
        Normalizatios list([str]): Whether normalization will be performed ("yes" or "no").
        Activation (str): Activation function for the neural network.
        W (list[list[num]]): Weight matrix of the neural network.

    Returns:
        tuple: A tuple containing the predicted labels and the accuracy of the model.
    """


    try:
        Wc = [0] * len(W)
        true = 0
        TestPredictions = [1] * len(TestLabels)
        for i, w in enumerate(W):
            Wc[i] = np.copy(w)
            print('\rCopying weights.....',i+1,'/',len(W),end = "")
                
        print(Fore.GREEN + "\n\nTest Started with 0 ERROR\n" + Style.RESET_ALL)
        StartTime = time.time()
        for inpIndex,Input in enumerate(TestInputs):
            Input = np.array(Input)
            Input = Input.ravel()
            UniStartTime = time.time()
            NeuralLayer = Input
            
            for index, Layer in enumerate(Layers):
                if Normalizations[index] == 'y':
                    NeuralLayer = Normalization(NeuralLayer)
                if Activation[index] == 'relu':
                        NeuralLayer = Relu(NeuralLayer)
                elif Activation[index] == 'sigmoid':
                        NeuralLayer = Sigmoid(NeuralLayer)
                elif Activation[index] == 'softmax':
                        NeuralLayer = Softmax(NeuralLayer)
                        
                if Layers[index] == 'fex':
                    NeuralLayer,useless = Fex(NeuralLayer, W[index], ThresholdSigns[index], ThresholdValues[index])
                if Layers[index] == 'cat':
                    NeuralLayer,useless = Cat(NeuralLayer, W[index], ThresholdSigns[index], ThresholdValues[index],0)
            for i, w in enumerate(Wc):
                W[i] = np.copy(w)
            RealOutput = np.argmax(TestLabels[inpIndex])
            PredictedOutput = np.argmax(NeuralLayer)
            if RealOutput == PredictedOutput:
                true += 1
            Acc = true / len(TestLabels)
            TestPredictions[inpIndex] = PredictedOutput+1
            UniEndTime = time.time()
                
            CalculatingEst = round((UniEndTime - UniStartTime) * (len(TestInputs) - inpIndex),3)
                
            if CalculatingEst < 60:
                print('\rest......(sec):',CalculatingEst,'\n',end= "")
                print('\rTest Accuracy: ' ,Acc ,"\n", end="")
            
            elif CalculatingEst > 60 and CalculatingEst < 3600:
                print('\rest......(min):',CalculatingEst/60,'\n',end= "")
                print('\rTest Accuracy: ' ,Acc ,"\n", end="")
            
            elif CalculatingEst > 3600:
                print('\rest......(h):',CalculatingEst/3600,'\n',end= "")
                print('\rTest Accuracy: ' ,Acc ,"\n", end="")
                
        EndTime = time.time()
        for i, w in enumerate(Wc):
            W[i] = np.copy(w)

        CalculatingEst = round(EndTime - StartTime,2)
        
        print(Fore.GREEN + "\nTest Finished with 0 ERROR\n")
        
        if CalculatingEst < 60:
            print('Total testing time(sec): ',CalculatingEst)
            
        elif CalculatingEst > 60 and CalculatingEst < 3600:
            print('Total testing time(min): ',CalculatingEst/60)
            
        elif CalculatingEst > 3600:
            print('Total testing time(h): ',CalculatingEst/3600)
            
        if Acc >= 0.8:
            print(Fore.GREEN + '\nTotal Test Accuracy: ' ,Acc, '\n' + Style.RESET_ALL)
        
        elif Acc < 0.8 and Acc > 0.6:
            print(Fore.MAGENTA + '\nTotal Test Accuracy: ' ,Acc, '\n' + Style.RESET_ALL)
        
        elif Acc <= 0.6:
            print(Fore.RED+ '\nTotal Test Accuracy: ' ,Acc, '\n' + Style.RESET_ALL)   
    
    except:
        
        print(Fore.RED + "ERROR: Testing model parameters like 'Layers' 'ThresholdCounts' must be same as trained model. Check parameters. Are you sure weights are loaded ? from: TestPLAN" + infoTestModel + Style.RESET_ALL)
        return 'e'
   
    return TestPredictions,Acc

def SavePLAN(ModelName,
             ModelType,
             Layers,
             ClassCount,
             ThresholdSigns,
             ThresholdValues,
             Normalizations,
             Activations,
             TestAcc,
             LogType,
             WeightsType,
             WeightFormat,
             SavePath,
             W
 ):
    
    infoSavePLAN = """
    Function to save a deep learning model.

    Arguments:
    ModelName (str): Name of the model.
    ModelType (str): Type of the model.(options: PLAN)
    Layers (list): List containing 'fex' and 'cat' layers.
    ClassCount (int): Number of classes.
    ThresholdSigns (list): List containing threshold signs.
    ThresholdValues (list): List containing threshold values.
    DoNormalization (str): is that normalized data ? 'y' or 'n'.
    Activations (list): List containing activation functions for each layer.
    TestAcc (float): Test accuracy of the model.
    LogType (str): Type of log to save (options: 'csv', 'txt', 'hdf5').
    WeightsType (str): Type of weights to save (options: 'txt', 'npy', 'mat').
    WeightFormat (str): Format of the weights (options: 'd', 'f', 'raw').
    SavePath (str): Path where the model will be saved. For example: C:/Users/beydili/Desktop/denemePLAN/
    W: Weights of the model.
    
    Returns:
    str: Message indicating if the model was saved successfully or encountered an error.
    """
    
    # Operations to be performed by the function will be written here
    pass

    if LogType != 'csv' and  LogType != 'txt' and LogType != 'hdf5':
        print(Fore.RED + "ERROR109: Save Log Type (File Extension) must be 'csv' or 'txt' or 'hdf5' from: SavePLAN" + infoSavePLAN + Style.RESET_ALL)
        return 'e'
    
    if WeightsType != 'txt' and  WeightsType != 'npy' and WeightsType != 'mat':
        print(Fore.RED + "ERROR110: Save Weight type (File Extension) Type must be 'txt' or 'npy' or 'mat' from: SavePLAN" + infoSavePLAN + Style.RESET_ALL)
        return 'e'
    
    if WeightFormat != 'd' and  WeightFormat != 'f' and WeightFormat != 'raw':
        print(Fore.RED + "ERROR111: Weight Format Type must be 'd' or 'f' or 'raw' from: SavePLAN" + infoSavePLAN + Style.RESET_ALL)
        return 'e'
    
    NeuronCount = 0
    SynapseCount = 0
    try:
        for w in W:
            NeuronCount += np.shape(w)[0]
            SynapseCount += np.shape(w)[0] * np.shape(w)[1]
    except:
        
        print(Fore.RED + "ERROR: Weight matrices has a problem from: SavePLAN" + infoSavePLAN + Style.RESET_ALL)
        return 'e'
    import pandas as pd
    from datetime import datetime
    from scipy import io
    
    data = {'MODEL NAME': ModelName,
            'MODEL TYPE': ModelType,
            'LAYERS': Layers,
            'LAYER COUNT': len(Layers),
            'CLASS COUNT': ClassCount,
            'THRESHOLD SIGNS': ThresholdSigns,
            'THRESHOLD VALUES': ThresholdValues,
            'NORMALIZATION': Normalizations,
            'ACTIVATIONS': Activations,
            'NEURON COUNT': NeuronCount,
            'SYNAPSE COUNT': SynapseCount,
            'TEST ACCURACY': TestAcc,
            'SAVE DATE': datetime.now(),
            'WEIGHTS TYPE': WeightsType,
            'WEIGHTS FORMAT': WeightFormat,
            'SAVE PATH': SavePath
            }
    try:
        
        df = pd.DataFrame(data)
        
        if  LogType == 'csv':
        
            df.to_csv(SavePath + ModelName + '.csv', sep='\t', index=False)
            
        elif LogType == 'txt':
            
            df.to_csv(SavePath + ModelName + '.txt', sep='\t', index=False)
            
        elif LogType == 'hdf5':
            
            df.to_hdf(SavePath + ModelName + '.h5', key='data', mode='w')
            
    except:
        
        print(Fore.RED + "ERROR: Model log not saved. Check the log parameters from: SavePLAN" + infoSavePLAN + Style.RESET_ALL)
        return 'e'
    try:
        
        if WeightsType == 'txt' and WeightFormat == 'd':
            
            for i, w in enumerate(W):
                np.savetxt(SavePath + ModelName +  str(i+1) + 'w.txt' ,  w, fmt='%d')
                
        if WeightsType == 'txt' and WeightFormat == 'f':
             
            for i, w in enumerate(W):
                 np.savetxt(SavePath + ModelName +  str(i+1) + 'w.txt' ,  w, fmt='%f')
        
        if WeightsType == 'txt' and WeightFormat == 'raw':
            
            for i, w in enumerate(W):
                np.savetxt(SavePath + ModelName +  str(i+1) + 'w.txt' ,  w)
            
                
        ###
        
        
        if WeightsType == 'npy' and WeightFormat == 'd':
            
            for i, w in enumerate(W):
                np.save(SavePath + ModelName + str(i+1) + 'w.npy', w.astype(int))
        
        if WeightsType == 'npy' and WeightFormat == 'f':
             
            for i, w in enumerate(W):
                 np.save(SavePath + ModelName +  str(i+1) + 'w.npy' ,  w, w.astype(float))
        
        if WeightsType == 'npy' and WeightFormat == 'raw':
            
            for i, w in enumerate(W):
                np.save(SavePath + ModelName +  str(i+1) + 'w.npy' ,  w)
                
           
        ###
        
         
        if WeightsType == 'mat' and WeightFormat == 'd':
            
            for i, w in enumerate(W):
                w = {'w': w.astype(int)}
                io.savemat(SavePath + ModelName + str(i+1) + 'w.mat', w)
    
        if WeightsType == 'mat' and WeightFormat == 'f':
             
            for i, w in enumerate(W):
                w = {'w': w.astype(float)}
                io.savemat(SavePath + ModelName + str(i+1) + 'w.mat', w)
        
        if WeightsType == 'mat' and WeightFormat == 'raw':
            
            for i, w in enumerate(W):
                w = {'w': w}
                io.savemat(SavePath + ModelName + str(i+1) + 'w.mat', w)
            
    except:
        
        print(Fore.RED + "ERROR: Model Weights not saved. Check the Weight parameters. SaveFilePath expl: 'C:/Users/hasancanbeydili/Desktop/denemePLAN/' from: SavePLAN" + infoSavePLAN + Style.RESET_ALL)
        return 'e'
    print(df)
    message = (
        Fore.GREEN + "Model Saved Successfully\n" +
        Fore.MAGENTA + "Don't forget, if you want to load model: model log file and weight files must be in the same directory." + 
        Style.RESET_ALL
        )
    
    return print(message)


def LoadPLAN(ModelName,
             LoadPath,
             LogType,
):
   infoLoadPLAN = """
   Function to load a deep learning model.

   Arguments:
   ModelName (str): Name of the model.
   LoadPath (str): Path where the model is saved.
   LogType (str): Type of log to load (options: 'csv', 'txt', 'hdf5').

   Returns:
   lists: W(list[num]), Layers, ThresholdSigns, ThresholdValues, Normalization,Activations
    """
   pass

    
   import pandas as pd
   import scipy.io as sio
   
   try:
   
       if LogType == 'csv':
           df = pd.read_csv(LoadPath + ModelName + '.' + LogType)
        
    
       if LogType == 'txt':
           df = pd.read_csv(LoadPath + ModelName + '.' + LogType, delimiter='\t')
        
    
       if LogType == 'hdf5':
           df = pd.read_hdf(LoadPath + ModelName + '.' + LogType)
   except:
       print(Fore.RED + "ERROR: Model Path error. Accaptable form: 'C:/Users/hasancanbeydili/Desktop/denemePLAN/' from: LoadPLAN" + infoLoadPLAN + Style.RESET_ALL)

   ModelName = str(df['MODEL NAME'].iloc[0])
   Layers = df['LAYERS'].tolist()
   LayerCount = int(df['LAYER COUNT'].iloc[0])
   ClassCount = int(df['CLASS COUNT'].iloc[0])
   ThresholdSigns = df['THRESHOLD SIGNS'].tolist()
   ThresholdValues = df['THRESHOLD VALUES'].tolist()
   Normalization = df['NORMALIZATION'].tolist()
   Activations = df['ACTIVATIONS'].tolist()
   NeuronCount = int(df['NEURON COUNT'].iloc[0])
   SynapseCount = int(df['SYNAPSE COUNT'].iloc[0])
   TestAcc = int(df['TEST ACCURACY'].iloc[0])
   ModelType = str(df['MODEL TYPE'].iloc[0])
   WeightType = str(df['WEIGHTS TYPE'].iloc[0])
   WeightFormat = str(df['WEIGHTS FORMAT'].iloc[0])
   SavePath = str(df['SAVE PATH'].iloc[0])

   W = [0] * LayerCount
   
   if WeightType == 'txt':
       for i in range(LayerCount):    
           W[i] = np.loadtxt(LoadPath + ModelName + str(i+1) + 'w.txt')
   elif WeightType == 'npy':
       for i in range(LayerCount):    
           W[i] = np.load(LoadPath + ModelName + str(i+1) + 'w.npy')
   elif WeightType == 'mat':
       for i in range(LayerCount):  
           W[i] = sio.loadmat(LoadPath + ModelName + str(i+1) + 'w.mat')
   else:
        raise ValueError(Fore.RED + "Incorrect weight type value. Value must be 'txt', 'npy' or 'mat' from: LoadPLAN."  + infoLoadPLAN + Style.RESET_ALL)
   print(Fore.GREEN + "Model loaded succesfully" + Style.RESET_ALL)     
   return W,Layers,ThresholdSigns,ThresholdValues,Normalization,Activations,df

def PredictFromDiscPLAN(Input,ModelName,ModelPath,LogType):
    infoPredictFromDİscPLAN = """
    Function to make a prediction using a divided pruning deep learning neural network (PLAN).

    Arguments:
    Input (list or ndarray): Input data for the model (single vector or single matrix).
    ModelName (str): Name of the model.
    ModelPath (str): Path where the model is saved.
    LogType (str): Type of log to load (options: 'csv', 'txt', 'hdf5').

    Returns:
    ndarray: Output from the model.
    """
    W,Layers,ThresholdSigns,ThresholdValues,Normalization,Activations = LoadPLAN(ModelName,ModelPath,
                                                                                  LogType)[0:6]
    Wc = [0] * len(W)
    for i, w in enumerate(W):
        Wc[i] = np.copy(w)
    try:
        NeuralLayer = Input
        NeuralLayer = np.array(NeuralLayer)
        NeuralLayer = NeuralLayer.ravel()
        for index, Layer in enumerate(Layers):                                                                          
            if Normalization == 'y':
                NeuralLayer = Normalization(NeuralLayer)
            if Activations[index] == 'relu':
                NeuralLayer = Relu(NeuralLayer)
            elif Activations[index] == 'sigmoid':
                NeuralLayer = Sigmoid(NeuralLayer)
            elif Activations[index] == 'softmax':
                NeuralLayer = Softmax(NeuralLayer)
                                
            if Layers[index] == 'fex':
                NeuralLayer,useless = Fex(NeuralLayer, W[index],
                                          ThresholdSigns[index],
                                          ThresholdValues[index])
            if Layers[index] == 'cat':
                NeuralLayer,useless = Cat(NeuralLayer, W[index],
                                          ThresholdSigns[index],
                                          ThresholdValues[index],
                                          0)
    except:
       print(Fore.RED + "ERROR: The input was probably entered incorrectly. from: PredictFromDiscPLAN"  + infoPredictFromDİscPLAN + Style.RESET_ALL)
       return 'e'
    for i, w in enumerate(Wc):
        W[i] = np.copy(w)
    return NeuralLayer


def PredictFromRamPLAN(Input,Layers,ThresholdSigns,ThresholdValues,Normalizations,Activations,W):
    infoPredictFromRamPLAN = """
    Function to make a prediction using a pruning learning artificial neural network (PLAN)
    from weights and parameters stored in memory.

    Arguments:
    Input (list or ndarray): Input data for the model (single vector or single matrix).
    Layers (list): Number and types of layers.
    ThresholdSigns (list): Threshold signs.
    ThresholdValues (list): Threshold values.
    DoNormalization (str): Whether to normalize ('y' or 'n').
    Activations (list): Activation functions for each layer.
    W (list of ndarrays): Weights of the model.

    Returns:
    ndarray: Output from the model.
    """
    
    Wc = [0] * len(W)
    for i, w in enumerate(W):
        Wc[i] = np.copy(w)
    try:
        NeuralLayer = Input
        NeuralLayer = np.array(NeuralLayer)
        NeuralLayer = NeuralLayer.ravel()
        for index, Layer in enumerate(Layers):                                                                          
            if Normalizations[index] == 'y':
                NeuralLayer = Normalization(NeuralLayer)
            if Activations[index] == 'relu':
                NeuralLayer = Relu(NeuralLayer)
            elif Activations[index] == 'sigmoid':
                NeuralLayer = Sigmoid(NeuralLayer)
            elif Activations[index] == 'softmax':
                NeuralLayer = Softmax(NeuralLayer)
                                
            if Layers[index] == 'fex':
                NeuralLayer,useless = Fex(NeuralLayer, W[index],
                                          ThresholdSigns[index],
                                          ThresholdValues[index])
            if Layers[index] == 'cat':
                NeuralLayer,useless = Cat(NeuralLayer, W[index],
                                          ThresholdSigns[index],
                                          ThresholdValues[index],0)
    except:
        print(Fore.RED + "ERROR: Unexpected input or wrong model parameters from: PredictFromRamPLAN."  + infoPredictFromRamPLAN + Style.RESET_ALL)
        return 'e'
    for i, w in enumerate(Wc):
        W[i] = np.copy(w)
    return NeuralLayer
    

def AutoBalancer(TrainInputs, TrainLabels, ClassCount):
   infoAutoBalancer = """
   Function to balance the training data across different classes.

   Arguments:
   TrainInputs (list): Input data for training.
   TrainLabels (list): Labels corresponding to the input data.
   ClassCount (int): Number of classes.

   Returns:
   tuple: A tuple containing balanced input data and labels.
   """
   try:
        ClassIndices = {i: np.where(np.array(TrainLabels)[:, i] == 1)[0] for i in range(ClassCount)}
        ClassCounts = [len(ClassIndices[i]) for i in range(ClassCount)]
        
        if len(set(ClassCounts)) == 1:
            print(Fore.WHITE + "INFO: All training data have already balanced. from: AutoBalancer"  + Style.RESET_ALL)
            time.sleep(1.5)
            return TrainInputs, TrainLabels
        
        MinCount = min(ClassCounts)
        
        BalancedIndices = []
        for i in range(ClassCount):
            if len(ClassIndices[i]) > MinCount:
                SelectedIndices = np.random.choice(ClassIndices[i], MinCount, replace=False)
            else:
                SelectedIndices = ClassIndices[i]
            BalancedIndices.extend(SelectedIndices)
        
        BalancedInputs = [TrainInputs[idx] for idx in BalancedIndices]
        BalancedLabels = [TrainLabels[idx] for idx in BalancedIndices]
        
        print(Fore.GREEN + "All Training Data Succesfully Balanced from: " + str(len(TrainInputs)) + " to: " + str(len(BalancedInputs)) + ". from: AutoBalancer " + Style.RESET_ALL)
        time.sleep(1.5)
   except:
        print(Fore.RED + "ERROR: Inputs and labels must be same length check parameters" + infoAutoBalancer)
        return 'e'
        
   return BalancedInputs, BalancedLabels