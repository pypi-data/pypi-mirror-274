'''Returns a list of Sequence objects with the reverse complement of the sequences.'''
# pylint: disable=too-few-public-methods
from packages.sequences.sequences import Sequence
from .abstract_transformer import AbstractTransformer

class ReverseComplement(AbstractTransformer):
    '''Returns a list of Sequence objects with the reverse complement of the sequences.'''
    def __init__(self, style):
        self.style = style

    def transform(self, sequence):
        '''Returns a list of Sequence objects with the specified transformation.'''
        toret = []
        if self.style == 'reverse':
            for seq in sequence:
                toret.append(Sequence(seq.id, seq.seq[::-1], seq.file_name))

        elif self.style == 'complement':
            complements = {
                'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A',
                'a': 't', 'c': 'g', 'g': 'c', 't': 'a'
            }
            for seq in sequence:
                toret.append(Sequence(seq.id, ''.join(complements[base] for base in seq.seq),
                                      seq.file_name))

        elif self.style == 'both':
            complements = {
                'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A',
                'a': 't', 'c': 'g', 'g': 'c', 't': 'a'
            }
            for seq in sequence:
                combined_seq = ''.join(complements[base] for base in seq.seq[::-1])
                toret.append(Sequence(seq.id, combined_seq, seq.file_name))

        return toret
