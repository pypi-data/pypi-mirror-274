'''Module to compute statistics for a list of sequences'''
import csv
import os

class SequenceStats:
    '''Class to compute statistics for a list of sequences'''
    def get_seq_stats(self, sequence):
        '''Computes statistics for a sequence'''
        # Calculates statistics for an individual sequence
        length = len(sequence.seq)
        counts = {'A': 0, 'C': 0, 'T': 0, 'G': 0, '-': 0}

        for base in sequence.seq:
            if base in counts:
                counts[base] += 1

        # Return statistics in a list
        stats = [sequence.id, length] + [counts[base] for base in 'ACTG-']
        return stats

    def get_seq_stats_matrix(self, seq):
        '''Computes statistics for a list of sequences'''
        header = ['id', 'len', 'A', 'C', 'T', 'G', '-']
        matrix = [header]

        for sequence in seq:
            stats = SequenceStats().get_seq_stats(sequence)
            matrix.append(stats)

        # Returns the statistics array
        return matrix

    def stats_to_csv(self, matrix, filepath):
        '''Writes the statistics array to a CSV file'''
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(matrix)

    def generate_stats(self, sequences, stats_directory, filename):
        '''Generates statistics for a list of sequences'''
        os.makedirs(stats_directory, exist_ok=True)
        stats_matrix = self.get_seq_stats_matrix(sequences)
        stats_filename = os.path.splitext(filename)[0] + '_stats.csv'
        stats_filepath = os.path.join(stats_directory, stats_filename)
        self.stats_to_csv(stats_matrix, stats_filepath)
