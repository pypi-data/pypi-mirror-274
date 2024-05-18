# Imports.

import numpy as np

from .. import Global_Utilities as gu

# Function definitions.

def extract_colour_features( output_directory, file_data, data ):

    # L*.

    feature_1 = []

    for i in range( len( file_data ) ):

        feature_1.append( data[0][i] )

    features = np.array( feature_1 )[:, np.newaxis]

    feature_names = ["Colour_L*"]

    # a*.

    feature_1 = []

    for i in range( len( file_data ) ):

        feature_1.append( data[1][i] )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "Colour_a*" )

    # b*.

    feature_1 = []

    for i in range( len( file_data ) ):

        feature_1.append( data[2][i] )

    features = np.hstack( (features, np.array( feature_1 )[:, np.newaxis]) )

    feature_names.append( "Colour_b*" )

    df = gu.array_with_column_titles_to_df( features, feature_names )

    df.to_csv( output_directory + "Colour/Features/Features.csv" )

def read_and_analyse_features( ip, file_data ):

    plot_specimen_bars = False
    plot_mean_bars = False
    plot_specimen_features = True
    plot_mean_features = True
    plot_specimen_distance_matrix = True
    plot_mean_distance_matrix = True
    plot_specimen_dendrogram = True
    plot_mean_dendrogram = True

    resin_data = gu.get_list_of_resins_data( ip.directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( ip.output_directory + "Colour/Features/Features.csv" )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    if not ip.sample_mask:

        ip.sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]

    sample_mask = ip.sample_mask

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    if not ip.feature_selection:

        ip.feature_selection = [i for i in range( len( feature_names ) )]

    feature_selection = ip.feature_selection

    features = features[:, feature_selection]
    feature_names = list( np.array( feature_names )[feature_selection] )

    specimen_mask = gu.produce_mask( sample_array, sample_mask )

    features = features[specimen_mask, :]
    file_data_mask = np.array( file_data )[specimen_mask] # Orders file data according to specimen mask.
    file_data_mask = [[int( f[0] ), int( f[1] ), f[2], f[3]] for f in file_data_mask] # Converts file data so that f[0], etc. are integers and not np.str.
    sample_array = sample_array[specimen_mask]

    feature_weights = [1 for i in range( len( feature_selection ) )]

    gu.normalise_features( features )

    mean_features = gu.extract_mean_features( features, sample_array, sample_mask )
    mean_feature_names = feature_names.copy()

    std_of_features = gu.extract_std_of_features( features, sample_array, sample_mask )

    distance_matrix = gu.distance_matrix_from_features( features )

    mean_distance_matrix = gu.distance_matrix_from_features( mean_features )

    mean_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], mean_features) )

    df = gu.array_with_column_titles_to_df( mean_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "Colour/Features/Mean_Features.csv" )

    std_of_features_plus_sample_mask = np.hstack( (np.array( sample_mask )[:, np.newaxis], std_of_features) )

    df = gu.array_with_column_titles_to_df( std_of_features_plus_sample_mask, ["sample"] + mean_feature_names )

    df.to_csv( ip.output_directory + "Colour/Features/Std_of_Features.csv" )

    df = gu.array_with_column_titles_and_label_titles_to_df( mean_distance_matrix, sample_mask, sample_mask )

    df.to_csv( ip.output_directory + "Colour/Features/Distance_Matrix.csv" )

    if plot_specimen_bars:

        for i in range( len( features[0] ) ):

            gu.plot_barchart_of_feature( features[:, i], [f[2] for f in file_data_mask], colour = True, colour_mask = sample_array, filename = ip.output_directory + "Colour/Feature_Bars/Specimen/" + feature_names[i] + ".pdf", savefig = True )

    if plot_mean_bars:

        for i in range( len( mean_features[0] ) ):

            gu.plot_barchart_of_feature( mean_features[:, i], [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = std_of_features[:, i], colour = True, colour_mask = sample_mask, filename = ip.output_directory + "Colour/Feature_Bars/Mean/" + mean_feature_names[i] + ".pdf", savefig = True )

    if plot_specimen_features:

        gu.plot_features( ip.output_directory, features, feature_names, [f[2] for f in file_data_mask], specimen = True, subdirectory = "Colour/Features/", title = "Specimen_Features.pdf" )

    if plot_mean_features:

        gu.plot_features( ip.output_directory, mean_features, mean_feature_names, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "Colour/Features/", title = "Means_Features.pdf" )

    if plot_specimen_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, file_data = file_data_mask, sample_mask = sample_mask, subdirectory = "Colour/Features/", title = "Specimen_Distance_Matrix.pdf" )

    if plot_mean_distance_matrix:

        gu.plot_distance_matrix( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "Colour/Features/", title = "Means_Distance_Matrix.pdf" )

    if plot_specimen_dendrogram:

        gu.plot_dendrogram( ip.output_directory, distance_matrix, [f[2] for f in file_data_mask], specimen = True, subdirectory = "Colour/Features/", title = "Specimen_Dendrogram.pdf" )

    if plot_mean_dendrogram:

        gu.plot_dendrogram( ip.output_directory, mean_distance_matrix, [resin_data.loc[i]["Label"] for i in sample_mask], subdirectory = "Colour/Features/", title = "Means_Dendrogram.pdf" )

def distance_to_virgin( file_data, data ):

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    array = np.hstack( (np.array( data[3] )[:, np.newaxis], np.array( data[4] )[:, np.newaxis], np.array( data[5] )[:, np.newaxis]) )

    gu.normalise_features( array )

    distance_matrix = gu.distance_matrix_from_features( array )

    distance = np.zeros( len( array ) )

    for i in range( len( array ) ):

        distance[i] = (distance_matrix[i][23] + distance_matrix[i][15] + distance_matrix[i][16] + distance_matrix[i][18]) / 4

    temp = distance.argsort()

    print( samples_present_array[temp] )

    print( distance[temp] )

    # [24 16 19 17 12  1 15 18  3  7  2  5  9  4 10 11  8  6 14 21 22 20 23 13]
    # [0.03974382 0.05419614 0.05511484 0.06760492 0.30163964 0.3595544
    #  0.45287626 0.54839772 0.57774539 0.58428028 0.58444907 0.63841646
    #  0.6426062  0.64468085 0.67112142 0.67640252 0.69095171 0.70618429
    #  0.72230624 0.79168456 0.82771439 0.84616013 0.88966182 1.89269532]

def sandbox( directory, output_directory, file_data, data ):

    perform_distance_to_virgin = True

    if perform_distance_to_virgin:

        distance_to_virgin( file_data, data )
