# AUTOGENERATED! DO NOT EDIT! File to edit: src/entropy_evaluator.ipynb (unless otherwise specified).

__all__ = ['EntropyEvaluator','UncertainEntropyEvaluator','UncertainGiniEvaluator','UncertainSqrtGiniEvaluator']

# Cell
from abc import ABCMeta, abstractmethod
from .data import Data
import math
import numpy as np
from scipy.stats import entropy

# Cell
class EntropyEvaluator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate_entropy(self, data: Data) -> float:
        raise NotImplementedError
        
    @abstractmethod
    def calculate_raw_entropy(self, labels: list, base:int = 2) -> float:
        raise NotImplementedError
        
# Cell
class UncertainEntropyEvaluator():

    def calculate_entropy(self, data: Data) -> float:
        class_att = data.get_attributes()[-1]
        probs = data.calculate_statistics(class_att)
        entropy = sum(map(lambda v: -v.get_confidence() * math.log2(v.get_confidence())  if v.get_confidence()!=0 else 0, probs.get_statistics()))
        return entropy

    def calculate_raw_entropy(self, labels: list,base: int = 2) -> float:
        value,counts = np.unique(labels, return_counts=True)
        return entropy(counts, base=base)
    
#Cell
class UncertainGiniEvaluator(EntropyEvaluator):
    def calculate_entropy(self, data: Data) -> float:
        class_att = data.get_attributes()[-1]
        probs = data.calculate_statistics(class_att)
        gini = 1-sum(map(lambda v: v.get_confidence()**2  if v.get_confidence()!=0 else 0, probs.get_statistics()))
        return gini
    
    def calculate_raw_entropy(self, labels: list,base: int = 2) -> float:
        value,counts = np.unique(labels, return_counts=True)
        gini = 1-sum([(c/len(labels))**2 for c in counts])
        return gini
    

#Cell
class UncertainSqrtGiniEvaluator(EntropyEvaluator):
    def calculate_entropy(self, data: Data) -> float:
        class_att = data.get_attributes()[-1]
        probs = data.calculate_statistics(class_att)
        gini = 1-sum(map(lambda v: v.get_confidence()**2  if v.get_confidence()!=0 else 0, probs.get_statistics()))
        return np.sqrt(gini)
    
    def calculate_raw_entropy(self, labels: list,base: int = 2) -> float:
        value,counts = np.unique(labels, return_counts=True)
        gini = 1-sum([(c/len(labels))**2 for c in counts])
        return np.sqrt(gini)