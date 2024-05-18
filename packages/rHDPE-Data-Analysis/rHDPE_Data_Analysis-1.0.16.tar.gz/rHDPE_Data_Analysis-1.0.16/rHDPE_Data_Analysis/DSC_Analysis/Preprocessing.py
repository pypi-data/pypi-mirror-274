# Imports.

import os
import glob
import re
import numpy as np
import pandas as pd

from .. import Global_Utilities as gu

# Function definitions.

def read_until_break( f, T, Temp, HF, gap ):
    '''Read the file until there is a break.'''

    linenumber = 0

    time = []
    temperature = []
    heat_flow = []

    for line in f:

        if linenumber >= gap:

            if line.rstrip():

                a_list = line.rstrip().split( ',' )

                if a_list[0] and a_list[1] and a_list[2]:

                    map_object = list( map( float, a_list ) )

                    time.append( map_object[0] )
                    temperature.append( map_object[1] )
                    heat_flow.append( map_object[2] )

            else:

                break

        linenumber += 1

    T.append( time )
    Temp.append( temperature )
    HF.append( heat_flow )

def read_raw_data_file_1( filename, f, resin_data, file_data, data ):

    pattern = re.compile( r"^Resin(\d+)_(\d+)_" )

    resin = int( pattern.search( f ).groups()[0] )

    specimen = int( pattern.search( f ).groups()[1] )

    Time = [[] for i in range( 6 )]
    Temperature = [[] for i in range( 6 )]
    Heat_Flow = [[] for i in range( 6 )]

    with open( filename, 'r' ) as f:

        read_until_break( f, Time[0], Temperature[0], Heat_Flow[0], 10 )

        read_until_break( f, Time[1], Temperature[1], Heat_Flow[1], 4 )

        read_until_break( f, Time[2], Temperature[2], Heat_Flow[2], 4 )

        read_until_break( f, Time[3], Temperature[3], Heat_Flow[3], 4 )

        read_until_break( f, Time[4], Temperature[4], Heat_Flow[4], 4 )

        read_until_break( f, Time[5], Temperature[5], Heat_Flow[5], 4 )

    data[0].append( Temperature[2][0] )
    data[1].append( Heat_Flow[2][0] )
    data[2].append( Temperature[4][0] )
    data[3].append( Heat_Flow[4][0] )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

def read_raw_data_file_2( filename, f, resin_data, file_data, data ):

    pattern = re.compile( r"^Resin(\d+)_(\d+)_(\D)" )

    resin = int( pattern.search( f ).groups()[0] )

    specimen = int( pattern.search( f ).groups()[1] )

    phase = pattern.search( f ).groups()[2]

    Time = [[] for i in range( 6 )]
    Temperature = [[] for i in range( 6 )]
    Heat_Flow = [[] for i in range( 6 )]

    if phase == "C":

        with open( filename, 'r' ) as f:

            read_until_break( f, Time[2], Temperature[2], Heat_Flow[2], 3 )

        data[0].append( Temperature[2][0] )
        data[1].append( Heat_Flow[2][0] )

        file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

    else:

        with open( filename, 'r' ) as f:

            read_until_break( f, Time[4], Temperature[4], Heat_Flow[4], 3 )

        data[2].append( Temperature[4][0] )
        data[3].append( Heat_Flow[4][0] )

def read_raw_data_file_3( filename, f, resin_data, file_data, data ):

    pattern = re.compile( r"^Resin(\d+)_(\d+)_" )

    resin = int( pattern.search( f ).groups()[0] )

    specimen = int( pattern.search( f ).groups()[1] )

    Temperature = [[] for i in range( 6 )]
    Heat_Flow = [[] for i in range( 6 )]

    with open( filename, 'r', encoding = "windows-1252" ) as f:

        linenumber = 0

        temp = []
        heat_flow = []

        for line in f:

            if linenumber < 3:

                linenumber += 1
                continue

            line_data = line.split( "," )

            temp.append( float( line_data[0] ) )
            heat_flow.append( float( line_data[1] ) )

            if abs( temp[ len( temp ) - 1] - temp[ len( temp ) - 2] ) > 1:

                break

        temp = []
        heat_flow = []

        for line in f:

            line_data = line.split( "," )

            temp.append( float( line_data[0] ) )
            heat_flow.append( float( line_data[1] ) )

            if abs( temp[ len( temp ) - 1] - temp[ len( temp ) - 2] ) > 1:

                break

        Temperature[2].append( temp )
        Heat_Flow[2].append( heat_flow )

        temp = []
        heat_flow = []

        for line in f:

            line_data = line.split( "," )

            temp.append( float( line_data[0] ) )
            heat_flow.append( float( line_data[1] ) )

            if abs( temp[ len( temp ) - 1] - temp[ len( temp ) - 2] ) > 1:

                break

        Temperature[4].append( temp )
        Heat_Flow[4].append( heat_flow )

    data[0].append( Temperature[2][0] )
    data[1].append( Heat_Flow[2][0] )
    data[2].append( Temperature[4][0] )
    data[3].append( Heat_Flow[4][0] )

    file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

def extract_raw_data( directory, data_directory ):
    '''Extract the raw data from the files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    resins = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + "*" )], key = gu.sort_raw_files_1 )

    file_data, data = [], [[], [], [], []]

    pattern = re.compile( r"^Resin(\d+)" )

    for r in resins:

        filenames = sorted( [os.path.basename( path ) for path in glob.glob( data_directory + r + "/*" )], key = gu.sort_raw_files_2 )

        resin = int( pattern.search( r ).groups()[0] )

        for f in filenames:

            if resin == 28:

                read_raw_data_file_2( data_directory + r + "/" + f, f, resin_data, file_data, data )

            elif resin == 40 or resin == 41:

                read_raw_data_file_3( data_directory + r + "/" + f, f, resin_data, file_data, data )

            else:

                read_raw_data_file_1( data_directory + r + "/" + f, f, resin_data, file_data, data )

    return file_data, data

def standardise_data( data ):
    '''Standardise data.'''

    standard_temp_list = np.linspace( 55, 165, 5500 ).tolist() # 195, 7000
    reverse_standard_temp_list = standard_temp_list[::-1]

    for i in range( len( data[0] ) ):

        mask = []

        array = np.array( data[0][i] )

        for j in range( len( reverse_standard_temp_list ) ):

            interval_mask = np.where( array <= reverse_standard_temp_list[j] )[0]

            if interval_mask.any():

                mask.append( interval_mask[0] )

            else:

                mask.append( len( array ) - 1 )

        data[1][i] = list( np.array( data[1][i] )[mask] )

        print( i )

    standard_temp_list = np.linspace( 55, 175, 6000 ).tolist()

    for i in range( len( data[2] ) ):

        mask = []

        array = np.array( data[2][i] )

        for j in range( len( standard_temp_list ) ):

            interval_mask = np.where( array >= standard_temp_list[j] )[0]

            if interval_mask.any():

                mask.append( interval_mask[0] )

            else:

                mask.append( len( array ) - 1 )

        data[3][i] = list( np.array( data[3][i] )[mask] )

        print( i )

    data[0] = list( reverse_standard_temp_list )
    data[2] = list( standard_temp_list )

def add_description_to_file_data( file_data ):
    '''Add descriptions in the form of letters to each specimen.'''

    # Add a for specimens that may be anomalous.
    # Add d for specimens that are duplicates.
    # Add u for unusual specimens.
    # Add z for PP specimens.
    # Add p for specimens for which the DSC was performed by Peiyao.

    specimens = {9:[2], 13:[0], 14:[2], 16:[0], 18:[0], 19:[1], 21:[2], 24:[2]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "a"

    specimens = {23:[2, 4]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "d"

    specimens = {24:[0]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "u"

    specimens = {201:[0, 1]}

    for f in file_data:

        if f[0] in specimens.keys():

            if f[1] in specimens[f[0]]:

                f[3] = f[3] + "z"

    for f in file_data:

        if f[0] >= 101 and f[0] <= 200:

            f[3] = f[3] + "p"

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

    array = np.array( data[0] )[:, np.newaxis]

    for i in range( len( data[1] ) ):

        array = np.hstack( (array, np.array( data[1][i] )[:, np.newaxis]) )

    np.savetxt( output_directory + "DSC/Condensed_Data/Crystallisation.csv", array, delimiter = "," )

    array = np.array( data[2] )[:, np.newaxis]

    for i in range( len( data[3] ) ):

        array = np.hstack( (array, np.array( data[3][i] )[:, np.newaxis]) )

    np.savetxt( output_directory + "DSC/Condensed_Data/Melt.csv", array, delimiter = "," )

    array = np.array( file_data )

    np.savetxt( output_directory + "DSC/Condensed_Data/file_data.csv", array, delimiter = ",", fmt = "%s" )

def read_csv( directory, output_directory, merge_groups ):
    '''Read the preprocessed .csv files.'''

    resin_data = gu.get_list_of_resins_data( directory ) # Obtain the spreadsheet of data for the resins.

    file_data = []

    df = pd.read_csv( output_directory + "DSC/Condensed_Data/file_data.csv", sep = ",", header = None )

    for i in range( len( df.index ) ):

        resin = df.iloc[i, 0]
        specimen = df.iloc[i, 1]

        file_data.append( [resin, specimen, resin_data.loc[resin]["Label"] + ".{}".format( specimen ), ""] )

    data = []

    df = pd.read_csv( output_directory + "DSC/Condensed_Data/Crystallisation.csv", sep = ",", header = None )

    data.append( df.iloc[:, 0].tolist() )

    Heat_Flow = []

    for i in range( 1, len( df.columns ) ):

        Heat_Flow.append( df.iloc[:, i].tolist() )

    data.append( Heat_Flow )

    df = pd.read_csv( output_directory + "DSC/Condensed_Data/Melt.csv", sep = ",", header = None )

    data.append( df.iloc[:, 0].tolist() )

    Heat_Flow = []

    for i in range( 1, len( df.columns ) ):

        Heat_Flow.append( df.iloc[:, i].tolist() )

    data.append( Heat_Flow )

    add_description_to_file_data( file_data )

    if merge_groups:

        gu.merge( file_data )

    return file_data, data

def remove_files( file_data, data ):
    '''Remove files not needed/wanted for analysis by searching for letters in file descriptions.'''

    files_to_remove = []

    for i in range( len( file_data ) ):

        s = file_data[i][3]

        if s.find( "p" ) > -0.5:

            pass

            # files_to_remove.append( i )

        # elif s.find( "p" ) == -1:
        #
        #     files_to_remove.append( i )

        if s.find( "a" ) > -0.5:

            files_to_remove.append( i )

        elif s.find( "d" ) > -0.5:

            files_to_remove.append( i )

        elif s.find( "u" ) > -0.5:

            files_to_remove.append( i )

        elif s.find( "z" ) > -0.5:

            files_to_remove.append( i )

    files_to_remove.reverse()

    for r in files_to_remove:

        file_data.pop( r )
        data[1].pop( r )
        data[3].pop( r )

def compute_mean( output_directory, file_data, data):
    '''Compute the mean data for each resin.'''

    m = [gu.sample_mean( file_data, data[1] ), gu.sample_mean( file_data, data[3] )]

    labels = ["Crystallisation", "Melt"]

    for i in range( len( m ) ):

        array = m[i][0][:, np.newaxis]

        for j in range( 1, len( m[i] ) ):

            array = np.hstack( (array, m[i][j][:, np.newaxis]) )

        np.savetxt( output_directory + "DSC/Condensed_Data/" + labels[i] + "_Means.csv", array, delimiter = "," )

def read_mean( output_directory, data ):
    '''Read the computed means for each resin from a file.'''

    labels = ["Crystallisation", "Melt"]

    for i in range( len( labels ) ):

        m = []

        df = pd.read_csv( output_directory + "DSC/Condensed_Data/" + labels[i] + "_Means.csv", sep = ",", header = None )

        for j in range( len( df.columns ) ):

            m.append( df.iloc[:, j].tolist() )

        data.append( m )
