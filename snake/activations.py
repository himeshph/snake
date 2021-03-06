import torch 
from torch import nn, sin, pow
from torch.nn import Parameter
from torch.distributions.exponential import Exponential

class Snake(nn.Module):
    '''
    Implementation of a rather serpentine sine-based periodic activation function 

    Shape:
        - Input: (N, *) where * means, any number of additional
          dimensions
        - Output: (N, *), same shape as the input

    Parameters:
        - alpha - trainable parameter

    References:
        - This activation function is from this paper by Liu Ziyin, Tilman Hartwig, Masahito Ueda:
        https://arxiv.org/abs/2006.08195


    Examples:
        >>> a1 = snake(256)
        >>> x = torch.randn(256)
        >>> x = a1(x)
    '''
    def __init__(self, in_features, alpha = None, alpha_trainable = True):
        '''
        Initialization.
        INPUT:
            - in_features: shape of the input
            - alpha: trainable parameter
            
            alpha is initialized to 1 by default, higher values = higher-frequency, 
            5-50 is a good starting point if you already think your data is periodic, 
            consider starting lower e.g. 0.5 if you think not, but don't worry, 
            alpha will be trained along with the rest of your model. 
        '''
        super(Snake,self).__init__()
        self.in_features = in_features

        # initialize alpha
        if alpha is not None:
            self.alpha = Parameter(torch.ones(in_features) * alpha) # create a tensor out of alpha
        else:            
            m = Exponential(torch.tensor([0.1]))
            self.alpha = Parameter(m.sample(in_features)) # Random init = mix of frequencies

        self.alpha.requiresGrad = alpha_trainable # Usually we'll want to train alpha, but maybe for some experiments we won't?


    def forward(self, x):
        '''
        Forward pass of the function.
        Applies the function to the input elementwise.

        Snake ∶= x + 1/a * sin^2 (xa)
        '''
        return  x + (1.0/self.alpha) * pow(sin(x * self.alpha), 2)

