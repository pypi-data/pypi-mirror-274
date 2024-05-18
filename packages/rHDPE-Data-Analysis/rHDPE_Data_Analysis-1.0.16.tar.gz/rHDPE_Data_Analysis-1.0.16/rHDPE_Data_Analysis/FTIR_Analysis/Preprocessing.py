# Imports.

import os
import glob
import re
import numpy as np
import pandas as pd

from .. import Global_Utilities as gu

# Function definitions.

def read_raw_data_file_1( filename, f, resin_data, file_data, data ):

    pattern = re.compile( r"^Resin(\d+)_(\d+)_" )

    resin = int( pattern.search( f ).groups()[0] )

    specimen = int( pattern.search( f ).groups()[1] )

    with open( filename, 'r' ) as file:

        x, y = [], []

        lines = file.readlines()

        for line in lines:

            a_list = line.split()

            if a_list:

                map_object = map( float, a_list )
                list_of_floats = list( map_object )

                if list_of_floats[0] <= 3996.26214 and list_of_floats[0] >= 599.82506:

                    x.append( list_of_floats[0] )
                    y.append( list_of_floats[1] )

            else:

                break

    data[0].append( np.array( x ) )
    data[1].append( np.array( y ) )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

def read_raw_data_file_2( filename, f, resin_data, file_data, data ):

    pattern = re.compile( r"^Resin(\d+)_(\d+)_" )

    resin = int( pattern.search( f ).groups()[0] )

    specimen = int( pattern.search( f ).groups()[1] )

    with open( filename, 'r' ) as file:

        x, y = [], []

        lines = file.read().splitlines()

        for line in lines:

            a_list = line.split( "," )

            if a_list:

                map_object = map( float, a_list )
                list_of_floats = list( map_object )

                if list_of_floats[0] <= 3996.26214 and list_of_floats[0] >= 599.82506:

                    x.append( list_of_floats[0] )
                    y.append( list_of_floats[1] )

            else:

                break

    data[0].append( np.array( x ) )
    data[1].append( np.array( y ) )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

def extract_raw_data( directory, data_directory ):
    '''Extract the raw data from the files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    resins = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + "*" )], key = gu.sort_raw_files_1 )

    file_data, data = [], [[], []]

    pattern = re.compile( r"^Resin(\d+)" )

    for r in resins:

        filenames = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + r + "/*" )], key = gu.sort_raw_files_2 )

        resin = int( pattern.search( r ).groups()[0] )

        for f in filenames:

            if resin >= 40 and resin <= 70:

                read_raw_data_file_2( data_directory + r + "/" + f, f, resin_data, file_data, data )

            else:

                read_raw_data_file_1( data_directory + r + "/" + f, f, resin_data, file_data, data )

    return file_data, data

def normalise( y ):
    '''Normalise the data.'''

    for i in range( len( y ) ):

        y[i] = y[i] / y[i].max()

def standardise_data( data ):
    '''Standardise data.'''

    standard_x_list = np.linspace( 600, 3996, 1762 ).tolist()
    standard_x_list.reverse()

    for i in range( len( data[0] ) ):

        mask = []

        array = np.array( data[0][i] )

        for j in range( len( standard_x_list ) ):

            interval_mask_upper = np.where( array >= standard_x_list[j] )[0]
            interval_mask_lower = np.where( array <= standard_x_list[j] )[0]

            if len( interval_mask_upper ) == 0:

                mask.append( interval_mask_lower[0] )

            elif len( interval_mask_lower ) == 0:

                mask.append( interval_mask_upper[len( interval_mask_upper ) - 1] )

            elif abs( data[0][i][interval_mask_upper[len( interval_mask_upper ) - 1]] - standard_x_list[j] ) > abs( data[0][i][interval_mask_lower[0]] - standard_x_list[j] ):

                mask.append( interval_mask_lower[0] )

            else:

                mask.append( interval_mask_upper[len( interval_mask_upper ) - 1] )

        data[1][i] = np.array( data[1][i] )[mask]

        print( i )

    data[0] = np.array( standard_x_list )

    normalise( data[1] )

def add_description_to_file_data( file_data ):
    '''Add descriptions in the form of letters to each specimen.'''

    # Add m for data produced in Manchester (by Thomas Franklin).
    # Add f for probably faulty experimental data.
    # Add r for repetitions.
    # Add p for virgin specimen that (erroneously) contains significant PP.
    # Add n for noisy.
    # Add a for additive data.
    # Add e for ebm trial sprectra.
    # Add u for Unilever FTIRs.
    # Add b for blends.

    specimens = {40:[0, 1, 2], 41:[0, 1, 2, 3, 4, 5]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "m"

    specimens = {40:[2], 406:[5]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "n"

    specimens = {4:[2, 4], 3:[0]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "f"

    specimens = {4:[5], 10:[8]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "r"

    specimens = {} #{19:[8]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "p"

    specimens = {41:[3, 4, 5]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "a"

    for f in file_data:

        if f[0] >= 50 and f[0] <= 100:

            f[3] = f[3] + "a"

    for f in file_data:

        if f[0] >= 301 and f[0] <= 400:

            f[3] = f[3] + "e"

    for f in file_data:

        if f[0] >= 401 and f[0] <= 499:

            f[3] = f[3] + "u"

    for f in file_data:

        if f[0] >= 500 and f[0] <= 599:

            f[3] = f[3] + "b"

def read_files_and_preprocess( directory, data_directory, merge_groups ):
    '''Read files and preprocess data.'''

    file_data, data = extract_raw_data( directory, data_directory )

    standardise_data( data )

    add_description_to_file_data( file_data )

    if merge_groups:

        gu.merge( file_data )

    return file_data, data

def write_csv( output_directory, file_data, data ):
    '''Write read and preprocessed data to a .csv file.'''

    array = data[0][:, np.newaxis]

    for i in range( len( data[1] ) ):

        array = np.hstack( (array, data[1][i][:, np.newaxis]) )

    np.savetxt( output_directory + "FTIR/Condensed_Data/FTIR_data.csv", array, delimiter = "," )

    array = np.array( file_data )

    np.savetxt( output_directory + "FTIR/Condensed_Data/file_data.csv", array, delimiter = ",", fmt = "%s" )

def read_csv( directory, output_directory, merge_groups ):
    '''Read the preprocessed .csv file.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    file_data = []

    df = pd.read_csv( output_directory + "FTIR/Condensed_Data/file_data.csv", sep = ",", header = None )

    for i in range( len( df.index ) ):

        resin = df.iloc[i, 0]
        specimen = df.iloc[i, 1]

        file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

    data = []

    df = pd.read_csv( output_directory + "FTIR/Condensed_Data/FTIR_data.csv", sep = ",", header = None )

    data.append( df.iloc[:, 0].tolist() )

    y = []

    for i in range( 1, len( df.columns ) ):

        y.append( df.iloc[:, i].tolist() )

    data.append( y )

    add_description_to_file_data( file_data )

    if merge_groups:

        gu.merge( file_data )

    return file_data, data

def remove_files( file_data, data ):
    '''Remove files not needed/wanted for analysis by searching for letters in file descriptions.'''

    files_to_remove = []

    for i in range( len( file_data ) ):

        s = file_data[i][3]

        if s.find( "m" ) > -0.5:

            files_to_remove.append( i )

        elif s.find( "n" ) > -0.5:

            files_to_remove.append( i )

        elif s.find( "f" ) > -0.5:

            files_to_remove.append( i )

        elif s.find( "r" ) > -0.5:

            files_to_remove.append( i )

        elif s.find( "p" ) > -0.5:

            files_to_remove.append( i )

        elif s.find( "a" ) > -0.5:

            files_to_remove.append( i )

        elif s.find( "e" ) > -0.5:

            if file_data[i][0] == 24:

                pass
                continue

            files_to_remove.append( i )

        elif s.find( "u" ) > -0.5:

            files_to_remove.append( i )

        elif s.find( "b" ) > -0.5:

            files_to_remove.append( i )

    files_to_remove.reverse()

    for r in files_to_remove:

        file_data.pop( r )
        data[1].pop( r )

def compute_mean( output_directory, file_data, data ):
    '''Compute the mean data for each resin.'''

    m = gu.sample_mean( file_data, data[1] )

    array = m[0][:, np.newaxis]

    for i in range( 1, len( m ) ):

        array = np.hstack( (array, m[i][:, np.newaxis]) )

    np.savetxt( output_directory + "FTIR/Condensed_Data/Means.csv", array, delimiter = "," )

def read_mean( output_directory, data ):
    '''Read the computed means for each resin from a file.'''

    m = []

    df = pd.read_csv( output_directory + "FTIR/Condensed_Data/Means.csv", sep = ",", header = None )

    for i in range( len( df.columns ) ):

        m.append( df.iloc[:, i].tolist() )

    data.append( m )
