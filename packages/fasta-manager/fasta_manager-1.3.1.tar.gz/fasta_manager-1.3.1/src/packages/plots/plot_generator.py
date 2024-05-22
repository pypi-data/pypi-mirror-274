'''Module for generating plots from sequences.'''
import os
import pandas as pd
import matplotlib.pyplot as plt

class PlotGenerator:
    '''Class for generating plots from sequences.'''
    def __init__(self, sequences, input_path, plots_dir):
        self.sequences = sequences
        self.input_path = input_path
        self.plots_dir = plots_dir
        self.df = self.create_dataframe()

    def create_dataframe(self):
        '''Creates a DataFrame from the sequences.'''
        seq_ids = [seq.id for seq in self.sequences]
        seq_lengths = [len(seq.seq) for seq in self.sequences]

        base_counts = {'A': [], 'C': [], 'T': [], 'G': []}
        for seq in self.sequences:
            for base, count_list in base_counts.items():
                count_list.append(seq.seq.count(base))

        data = {
            'seq_id': seq_ids,
            'len': seq_lengths,
            'A': base_counts['A'],
            'C': base_counts['C'],
            'T': base_counts['T'],
            'G': base_counts['G']
        }
        return pd.DataFrame(data)

    def generate_histogram(self):
        '''Generates a histogram of sequence lengths.'''
        sequence_lengths = self.df['len']
        plt.hist(sequence_lengths, bins=10, color='#DDA0DD')
        plt.xlabel('Sequence length')
        plt.ylabel('Frequency')
        plt.title('Histogram of sequence length distribution')
        plt.grid(True)
        input_file_name = os.path.splitext(os.path.basename(self.input_path))[0]
        histogram_filename = input_file_name + '_histogram.png'
        histogram_filepath = os.path.join(self.plots_dir, histogram_filename)
        os.makedirs(self.plots_dir, exist_ok=True)
        plt.savefig(histogram_filepath)
        plt.close()

    def generate_boxplot(self):
        '''Generates a box plot of base percentages.'''
        base_counts = ['A', 'C', 'T', 'G']
        total_lengths = self.df['len']
        for base in base_counts:
            self.df[base] = self.df[base] / total_lengths

        box_colors = ['#FFC0CB', '#ADD8E6', '#90EE90', '#FFFF66']
        plt.boxplot(self.df[base_counts].values, labels=base_counts, patch_artist=True)

        plt.xticks([])

        for patch, color in zip(plt.boxplot(self.df[base_counts].values,patch_artist=True)['boxes'],
                                box_colors):
            patch.set_facecolor(color)

        plt.xlabel('Bases')
        plt.ylabel('Percentage')
        plt.title('Relative percentage of bases in the total length of sequences')

        plt.grid(True)
        input_file_name = os.path.splitext(os.path.basename(self.input_path))[0]
        boxplot_filename = input_file_name + '_boxplot.png'
        boxplot_filepath = os.path.join(self.plots_dir, boxplot_filename)
        plt.savefig(boxplot_filepath)
        plt.close()

    def generate_plots(self):
        '''Generates plots from the sequences.'''
        self.generate_histogram()
        self.generate_boxplot()
