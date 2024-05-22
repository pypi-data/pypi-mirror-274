'''Main module for the FASTA file processing tool'''
import argparse
import os

from packages.utils.seq_file_manager import SeqFileManager
from packages.plots.plot_generator import PlotGenerator
from packages.sequences.sequences import Sequence
from packages.transformers.duplicated_transformer import DuplicatedTransformer
from packages.transformers.reverse_complement import ReverseComplement
from packages.stats.sequence_stats import SequenceStats

def apply_case_transformation(args, sequences):
    '''Applies a case transformation to the sequences'''
    if args.casefile == 'upper':
        return [Sequence(seq.id, seq.seq.upper(), seq.file_name) for seq in sequences]
    if args.casefile == 'lower':
        return [Sequence(seq.id, seq.seq.lower(), seq.file_name) for seq in sequences]
    return sequences

def apply_duplicate_transformation(args, sequences):
    '''Applies a duplicate transformation to the sequences'''
    if args.dremove:
        return DuplicatedTransformer(style='remove').transform(sequences)
    if args.drename:
        return DuplicatedTransformer(style='rename').transform(sequences)
    return sequences

def apply_sequence_transformation(args, sequences):
    '''Applies a sequence transformation to the sequences'''
    if args.reverse:
        return ReverseComplement(style='reverse').transform(sequences)
    if args.complement:
        return ReverseComplement(style='complement').transform(sequences)
    if args.rc:
        return ReverseComplement(style='both').transform(sequences)
    return sequences

def main():
    '''Main function'''
    parser = argparse.ArgumentParser(description='FASTA file processing tool')
    parser.add_argument('--dremove', action='store_true', help='Remove duplicates')
    parser.add_argument('--drename', action='store_true', help='Rename duplicates')
    parser.add_argument('--reverse', action='store_true', help='Reverse sequences')
    parser.add_argument('--complement', action='store_true', help='Complement sequences')
    parser.add_argument('--rc', action='store_true', help='Reverse complement sequences')
    parser.add_argument('--stats', help='Compute stats', action='store_true')
    parser.add_argument('--casefile', help='Case transformation (original, upper, lower)')
    parser.add_argument('--plots', help='Generate plots', action='store_true')
    args = parser.parse_args()


    # Get the FASTA files in the current directory
    current_directory = os.getcwd()
    fasta_files = [file for file in os.listdir(current_directory) if file.endswith('.fasta')]

    # Verify that there are FASTA files in the current directory
    if not any([args.casefile, args.dremove, args.drename, args.reverse,
                args.complement, args.rc, args.stats, args.plots]):
        print('No transformation specified, use fasta -h for help.')
        return

    if not fasta_files:
        print('No FASTA files found in the current directory.')
        return

    stats_directory = os.path.join(current_directory, 'result_stats')

    
    for filename in fasta_files:
        seq_file_manager = SeqFileManager(input_filename=filename)
        sequences = seq_file_manager.load_fasta(filename)

        # Auxiliar sequence in uppercase for stats and plots
        aux_seq = [seq.upper() for seq in sequences]

        sequences = apply_duplicate_transformation(args, sequences)

        sequences = apply_sequence_transformation(args, sequences)

        sequences = apply_case_transformation(args, sequences)

        sequence_stats = SequenceStats()
        sequence_stats.generate_stats(aux_seq, stats_directory, filename)

        plot_generator = PlotGenerator(aux_seq, filename, 'result_plots')
        plot_generator.generate_plots()

        


        # Process the sequences if any transformation was specified
        if any([args.casefile, args.dremove, args.drename, args.reverse, args.complement, args.rc]):
            output_directory = os.path.join(current_directory, 'result_formatted')
            seq_file_manager.write_fasta(sequences, output_directory)

        # Print success message
        print('Operation completed successfully!')

if __name__ == '__main__':
    main()
