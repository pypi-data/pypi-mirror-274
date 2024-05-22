'''This module contains the Sequence class.'''
## Definition of the Sequence class

class Sequence:
    '''This class represents a sequence.'''
    def __init__(self, sequence_id, sequence, file_name=None):
        self.id = sequence_id
        self.seq = sequence
        self.file_name = file_name

    def __repr__(self):
        return f'{self.id}: {self.seq}'

    def __str__(self):
        return f'{self.id}: {self.seq}\n'

    def lower(self):
        '''Returns a new Sequence object with the sequence in lowercase.'''
        return Sequence(self.id, self.seq.lower(), self.file_name)

    def upper(self):
        '''Returns a new Sequence object with the sequence in uppercase.'''
        return Sequence(self.id, self.seq.upper(), self.file_name)
