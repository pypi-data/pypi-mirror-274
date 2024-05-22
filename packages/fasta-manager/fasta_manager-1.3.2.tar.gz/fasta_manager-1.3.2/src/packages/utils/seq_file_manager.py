'''Module for loading and writing fasta files.'''
import os
from packages.sequences.sequences import Sequence

class SeqFileManager:
    '''This class allows us to format sequences and load and write fasta files.'''
    def __init__(self, input_filename=None):
        self.input_filename = input_filename


    def load_fasta(self, file_name):
        '''Returns a list of Sequence objects from the fasta file.'''
        sequences = []
        with open(file_name, 'r', encoding='utf-8') as file:
            current_id = None
            current_seq = ''
            for line in file:
                line = line.strip()
                if line.startswith('>'):
                    if current_id is not None:
                        # Provide the file_name parameter when creating Sequence objects
                        sequences.append(Sequence(current_id, current_seq, file_name))
                    current_id = line[1:]
                    current_seq = ''
                else:
                    current_seq += line
            if current_id is not None:
                # Provide the file_name parameter when creating Sequence objects
                sequences.append(Sequence(current_id, current_seq, file_name))

        return sequences

    # En la clase SeqFileManager en packages/Utils/seq_file_manager.py
    def write_fasta(self, sequences, output_directory):
        '''Writes all sequences to individual files in the output directory.'''
        os.makedirs(output_directory, exist_ok=True)  # Ensure the output directory exists

        for i, sequence in enumerate(sequences):
            # Use the input file name (sequence.file_name) without extension for the output file
            input_file_name = os.path.splitext(os.path.basename(sequence.file_name))[0]
            output_filename = f"{input_file_name}_result.fasta"
            output_file_path = os.path.join(output_directory, output_filename)

            # Use 'w' mode for the first sequence, 'a' mode for subsequent sequences
            mode = 'w' if i == 0 else 'a'

            with open(output_file_path, mode, encoding='utf-8') as f:
                f.write(f'>{sequence.id}\n')
                f.write(f'{sequence.seq}\n')
