'''Abstract class for sequence transformers.'''
# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod

class AbstractTransformer(ABC):
    '''Abstract class for sequence transformers.'''
    @abstractmethod
    def transform(self, sequence):
        '''Returns a list of Sequence objects with the transformation applied.'''
