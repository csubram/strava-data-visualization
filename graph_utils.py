import os
import matplotlib.pyplot as plt


OUTPUT_DIRECTORY = 'graphs'


def create_output_directory():
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)


def save_graph(filename):
    output_file_location = os.path.join(OUTPUT_DIRECTORY, filename)
    plt.savefig(output_file_location)
