'''Returns a list of Sequence objects with the specified transformation.'''
# pylint: disable=too-few-public-methods
from .abstract_transformer import AbstractTransformer

class DuplicatedTransformer(AbstractTransformer):
    '''Returns a list of Sequence objects with the specified transformation.'''
    def __init__(self, style):
        self.style = style

    def transform(self, sequence):
        new_seq_list = []

        if self.style == 'rename':
            id_dict = {}
            duplicate_count = {}
            for seq in sequence:
                seq_id = seq.id
                if seq_id in id_dict:
                    if seq_id not in duplicate_count:
                        duplicate_count[seq_id] = 1
                        id_dict[seq_id].id = f'{seq_id}.{duplicate_count[seq_id]}'
                        seq.id = f'{seq_id}.{duplicate_count[seq_id] + 1}'
                        id_dict[seq.id] = seq
                        duplicate_count[seq_id] += 1
                    else:
                        duplicate_count[seq_id] += 1
                        seq.id = f'{seq_id}.{duplicate_count[seq_id]}'
                        id_dict[seq.id] = seq
                else:
                    id_dict[seq_id] = seq
            new_seq_list = list(id_dict.values())


        elif self.style == 'remove':
            id_dict = {}
            for seq in sequence:
                seq_id = seq.id
                if seq_id not in id_dict:
                    id_dict[seq_id] = seq
            new_seq_list = list(id_dict.values())

        return new_seq_list
