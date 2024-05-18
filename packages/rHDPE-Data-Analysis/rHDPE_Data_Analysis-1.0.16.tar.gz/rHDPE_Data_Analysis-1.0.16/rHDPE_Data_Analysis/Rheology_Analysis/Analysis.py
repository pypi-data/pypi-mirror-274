# Imports.

from . import Preprocessing
from . import Utilities as util
from . import rheology_plotting

# Main function definition.

def Rheology_Analysis_Main( ip ):

    file_data, data = [], []

    if ip.read_files:

        file_data, data = Preprocessing.read_files_and_preprocess( ip.directory, ip.data_directory, ip.merge_groups )

    if ip.write_csv:

        Preprocessing.write_csv( ip.output_directory, file_data, data )

    if ip.read_csv:

        file_data, data = Preprocessing.read_csv( ip.directory, ip.output_directory, ip.merge_groups )

    # Data of form [Point, Angular Frequency, [Complex Viscosity], [Storage Modulus], [Loss Modulus], [Loss Factor], [Shear Strain], [Shear Stress], [Torque]].

    print( str( len( data[2] ) ) + " files have been read." )

    if len( data[2] ) != 30:

        print( "Warning: 30 files have not been read." )

    if ip.remove_files:

        Preprocessing.remove_files( file_data, data )

    if ip.compute_mean:

        Preprocessing.compute_mean( ip.output_directory, file_data, data )

    if ip.read_mean:

        Preprocessing.read_mean( ip.output_directory, data )

    # Data now of form [..., [CV_Means], [SM_Means], [LM_Means], [LF_Means]].

    if ip.derivative:

        first_derivative_data = util.compute_derivatives( data )
        second_derivative_data = util.compute_derivatives( first_derivative_data )

    if ip.extract_features:

        util.extract_rheology_features( ip.output_directory, file_data, data, first_derivative_data, second_derivative_data )

    if ip.read_and_analyse_features:

        util.read_and_analyse_features( ip, file_data )

    if ip.plot_data:

        rheology_plotting.plot_data( ip.directory, ip.output_directory, file_data, data, first_derivative_data, second_derivative_data )

    if ip.sandbox:

        util.sandbox( ip.directory, ip.output_directory, file_data, data, first_derivative_data, second_derivative_data )
