#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : ML Studio                                                         #
# Version : 0.1.0                                                             #
# File    : gradient_descent_optimizers.py                                    #
# Python  : 3.8.2                                                             #
# --------------------------------------------------------------------------  #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/MLStudio                       #
# --------------------------------------------------------------------------  #
# Created       : Saturday, May 16th 2020, 9:13:15 pm                         #
# Last Modified : Saturday, May 16th 2020, 9:13:16 pm                         #
# Modified By   : John James (jjames@decisionscients.com)                     #
# --------------------------------------------------------------------------  #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Gradient descent optimization algorithms."""
from abc import ABC, abstractmethod

import numpy as np
from sklearn.base import BaseEstimator  

from mlstudio.supervised.callbacks.base import Callback, CallbackList
from mlstudio.supervised.callbacks.learning_rate import LearningRateSchedule
# --------------------------------------------------------------------------  #
class Optimizer(ABC, BaseEstimator):
    """Base class for all optimizers."""

    def __init__(self):
        pass

    @abstractmethod        
    def __call__(self, gradient, learning_rate, theta, **kwargs):   
        """Computes the parameter updates.
        
        Parameters
        ----------
        gradient : func
            The function that performs the gradient computation 

        learning_rate : float
            The learning rate from the estimator object.

        theta : array-like
            The model parameters

        **kwargs : dict
            Arbitrary parameters used for computing the gradient.

        Returns
        -------
        theta : array-like
            The updated parameters of the model

        grad : array-like
            The gradient of the objective function w.r.t. parameters theta.
        """
        pass



# --------------------------------------------------------------------------  #
class Classic(Optimizer):
    """Standard gradient descent optimizer."""
    
    def __call__(self, gradient, learning_rate, theta, **kwargs):        
        grad = gradient(theta, **kwargs)
        theta = theta - learning_rate * grad
        return theta, grad

# --------------------------------------------------------------------------  #
class Momentum(Optimizer):
    """Standard gradient descent optimizer."""

    def __init__(self, gamma=0.9):
        self.gamma = gamma
        self._velocity = 0
    
    def __call__(self, gradient, learning_rate, theta, **kwargs):             
        grad = gradient(theta)
        self._velocity = gamma * self._velocity + learning_rate * grad
        theta = theta - self._velocity
        return theta, grad

# --------------------------------------------------------------------------  #
class Nesterov(Optimizer):
    """Nesterov accelerated gradient optimizer."""

    def __init__(self, gamma=0.9):
        self.gamma = gamma
        self._velocity = 0
    
    def __call__(self, gradient, learning_rate, theta, **kwargs):
        next_position = theta - self.gamma * self._velocity        
        grad = gradient(next_position)
        self._velocity = gamma * self._velocity + learning_rate * grad
        theta = theta - self._velocity
        return theta, grad

# --------------------------------------------------------------------------  #
class Adagrad(Optimizer):
    """Adagrad optimizer."""

    def __init__(self, epsilon=1e-8):
        self.epsilon = epsilon
        self.gradients = 0
    
    def __call__(self, gradient, learning_rate, theta, **kwargs):
        grad = gradient(theta)
        self.gradients = self.gradients + grad
        Gt = np.diag(np.square(self.gradients))        
        theta = theta - (learning_rate / np.sqrt(Gt + self.epsilon)) * grad
        return theta, grad        

# --------------------------------------------------------------------------  #
class Adadelta(Optimizer):
    """Adadelta optimizer."""

    def __init__(self, gamma=0.9, epsilon=1e-8):
        self.gamma = gamma
        self.epsilon = epsilon
        self.avg_sqr_gradient = 0
        self.avg_sqr_delta_theta = 0
    
    def __call__(self, gradient, learning_rate, theta, **kwargs):                
        grad = gradient(theta)     

        self.avg_sqr_gradient = self.gamma * self.avg_sqr_gradient + \
            (1 - self.gamma) * np.square(grad)            
        rms_grad = np.sqrt(np.square(self.avg_sqr_gradient) + self.epsilon)
        
        delta_theta = -learning_rate / rms_grad  * grad            

        self.avg_sqr_delta_theta = self.gamma * self.avg_sqr_delta_theta + \
            (1 - self.gamma) * np.square(delta_theta)
        rms_delta_theta = np.sqrt(np.square(self.avg_sqr_delta_theta) + self.epsilon)

        delta_theta = - (rms_delta_theta / rms_grad).dot(grad)

        theta = theta + delta_theta
        return theta, grad

# --------------------------------------------------------------------------  #
class RMSprop(Optimizer):
    """RMSprop optimizer."""

    def __init__(self, gamma=0.9, epsilon=1e-8):        
        self.gamma = gamma
        self.epsilon = epsilon
        self.avg_sqr_gradient = 0
        self.avg_sqr_delta_theta = 0
    
    def __call__(self, gradient, learning_rate, theta, **kwargs):                
        grad = gradient(theta)        
        self.avg_sqr_gradient = self.gamma * self.avg_sqr_gradient + \
            0.1 * np.square(grad)
        rms_grad = np.sqrt(np.square(self.avg_sqr_gradient) + self.epsilon)
        theta = theta - (learning_rate / rms_grad) * grad
        
        return theta, grad

# --------------------------------------------------------------------------  #
class Adam(Optimizer):
    """Adam optimizer."""

    def __init__(self, beta_one=0.9, beta_two=0.999, epsilon=10e-8):
        self.beta_one = beta_one
        self.beta_two = beta_two        
        self.epsilon = epsilon

        self.t = 0
        self.m = 0
        self.v = 0
    
    def __call__(self, gradient, learning_rate, theta, **kwargs):                
        self.t += 1
        grad = gradient(theta)        
        self.m = self.beta_one * self.m + (1 - beta_one) * grad
        self.v = self.beta_two * self.v + (1 - beta_two) * np.square(grad)
        # Bias corrected moment estimates
        m_hat = self.m / (1 - self.beta_one**t)
        v_hat = self.v / (1 - self.beta_two**t)

        theta = theta - learning_rate / (np.sqrt(v_hat) + self.epsilon) * m_hat        
        
        return theta, grad        

# --------------------------------------------------------------------------  #
class AdaMax(Optimizer):
    """AdaMax optimizer."""

    def __init__(self, beta_one=0.9, beta_two=0.999):        
        self.beta_one = beta_one
        self.beta_two = beta_two        
        self.t = 0
        self.m = 0
        self.v = 0
    
    def __call__(self, gradient, learning_rate, theta, **kwargs):                
        self.t += 1
        grad = gradient(theta)        
        
        self.m = self.beta_one * self.m + (1 - beta_one) * grad
        m_hat = self.m / (1 - self.beta_one**t)
        u = np.max(self.beta_two * self.v, np.abs(grad))    
        self.v = self.beta_two * self.v + (1 - beta_two) * np.linalg.norm(grad)
        theta = theta - (learning_rate / u) * m_hat
        
        return theta, grad              

# --------------------------------------------------------------------------  #
class Nadam(Optimizer):
    """Nadam optimizer."""

    def __init__(self, beta_one=0.9, epsilon=10e-8):
        self.beta_one = beta_one        
        self.epsilon = epsilon
        self.t = 0
        self.m = 0
        self.v = 0
    
    def __call__(self, gradient, learning_rate, theta, **kwargs):    
        self.t += 1
        self.m = self.beta_one * self.m + (1 - beta_one) * grad        
        # Bias corrected moment estimates
        m_hat = self.m / (1 - self.beta_one**self.t)        
        # Nadam update
        theta = theta - (learning_rate / (np.sqrt(v_hat) + self.epsilon)) * \
            (self.beta_one * m_hat + ((1-self.beta_one)* grad)/(1-self.beta_one**self.t))

        return theta, grad                                    

# --------------------------------------------------------------------------  #
class AMSGrad(Optimizer):
    """AMSGrad optimizer."""

    def __init__(self, beta_one=0.9, epsilon=10e-8):
        self.beta_one = beta_one        
        self.epsilon = epsilon
        self.t = 0
        self.m = 0
        self.v = 0
        self.v_hat = 0
    
    def __call__(self, gradient, learning_rate, theta, **kwargs):    
        self.t += 1
        self.m = self.beta_one * self.m + (1 - beta_one) * grad
        self.v = self.beta_two * self.v + (1 - beta_two) * np.square(grad)
        self.v_hat = np.max(self.v_hat, self.v)
        theta = theta - (learning_rate / np.sqrt(self.v_hat) + self.epsilon) * self.m
        
        return theta, grad                        