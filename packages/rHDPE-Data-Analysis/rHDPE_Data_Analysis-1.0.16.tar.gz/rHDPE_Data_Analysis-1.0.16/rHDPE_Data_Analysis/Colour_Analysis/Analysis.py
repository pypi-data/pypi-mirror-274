# Imports.

from . import Preprocessing
from . import Utilities as util
from . import Colour_plotting

# Main function definition.

def Colour_Analysis_Main( ip ):

    file_data, data = [], []

    if ip.read_files:

        file_data, data = Preprocessing.read_files_and_preprocess( ip.directory, ip.data_directory, ip.merge_groups )

    if ip.write_csv:

        Preprocessing.write_csv( ip.output_directory, file_data, data )

    if ip.read_csv:

        file_data, data = Preprocessing.read_csv( ip.directory, ip.output_directory, ip.merge_groups )

    # Data of form [[L], [a], [b]].

    print( str( len( data[0] ) ) + " files have been read." )

    if len( data[0] ) != 120:

        print( "Warning: 120 files have not been read." )

    if ip.remove_files:

        Preprocessing.remove_files( file_data, data )

    if ip.compute_mean:

        Preprocessing.compute_mean( ip.output_directory, file_data, data )

    if ip.read_mean:

        Preprocessing.read_mean( ip.output_directory, data )

    # Data now of form [[L], [a], [b], [mL], [ma], [mb]].

    if ip.extract_features:

        util.extract_colour_features( ip.output_directory, file_data, data )

    if ip.read_and_analyse_features:

        util.read_and_analyse_features( ip, file_data )

    if ip.plot_data:

        Colour_plotting.plot_data( ip.directory, ip.output_directory, file_data, data )

    if ip.sandbox:

        util.sandbox( ip.directory, ip.output_directory, file_data, data )
