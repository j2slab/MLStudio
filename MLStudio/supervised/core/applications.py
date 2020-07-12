#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : ML Studio                                                         #
# Version : 0.1.0                                                             #
# File    : application.py                                                           #
# Python  : 3.8.2                                                             #
# --------------------------------------------------------------------------  #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/MLStudio                       #
# --------------------------------------------------------------------------  #
# Created       : Tuesday, May 19th 2020, 10:00:13 pm                         #
# Last Modified : Tuesday, May 19th 2020, 10:00:13 pm                         #
# Modified By   : John James (jjames@decisionscients.com)                     #
# --------------------------------------------------------------------------  #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Defines linear, logistic, and multinomial logistic regression classes."""
from abc import ABC, abstractmethod 

import numpy as np
from sklearn.base import BaseEstimator

from mlstudio.supervised.core.activations import Sigmoid, Softmax
from mlstudio.supervised.core.objectives import MSE, CrossEntropy, CategoricalCrossEntropy 
# --------------------------------------------------------------------------  #
class Application(ABC, BaseEstimator):
    """Defines the base class for all applications."""

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def compute_output(self, theta, X):
        """Computes output for the application."""
        pass

    @abstractmethod
    def predict(self, theta, X):
        """Computes prediction."""
        pass

# --------------------------------------------------------------------------  #
class LinearRegression(Application):
    """Defines the linear regression application."""

    @property
    def name(self):
        return "Linear Regression"
    
    def compute_output(self, theta, X):
        """Computes linear regression output."""        
        return np.array(X.dot(theta), dtype=np.float32) 

    def predict(self, theta, X):
        return self.compute_output(theta, X)

# --------------------------------------------------------------------------  #
class LogisticRegression(Application):
    """Defines the logistic regression application."""

    def __init__(self):
        self.sigmoid = Sigmoid()

    @property
    def name(self):
        return "Logistic Regression"    

    def compute_output(self, theta, X):
        """Computes logistic regression output."""        
        z = np.array(X.dot(theta), dtype=np.float32)
        return self.sigmoid(z)

    def predict(self, theta, X):
        o = self.compute_output(theta, X)        
        return np.round(o).astype(int)

    def predict_proba(self, theta, X):
        return self.compute_output(theta, X)        

# --------------------------------------------------------------------------  #
class MultinomialLogisticRegression(Application):
    """Defines the multinomial logistic regression application."""

    def __init__(self):
        self.softmax = Softmax()

    @property
    def name(self):
        return "Multinomial Logistic Regression"    

    def compute_output(self, theta, X):
        """Computes multinomial logistic regression output."""        
        z = np.array(X.dot(theta), dtype=np.float32)
        return self.softmax(z)        

    def predict(self, theta, X):
        o = self.compute_output(theta, X)        
        return o.argmax(axis=1)

    def predict_proba(self, theta, X):
        return self.compute_output(theta, X)                