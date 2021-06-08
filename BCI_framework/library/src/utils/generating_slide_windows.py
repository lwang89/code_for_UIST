def generate_slide_window_chunks(raw_df, slide_window_params, default_label, chunk_index_list):
    """Generate the slide window DFs when it's the time

    It's time to generate a new slide windows for a setting if:

    * The length is larger than or equal to the slide window length
        
    * The difference of all data length and the slide window length,
    is an intger multiple to slide window interval.
    It means the rows of data added since the last time to
    update the slide window, is exactly the same as one slide
    window interval.

    Args:
        raw_df (Pandas Dataframe): The dataframe for all sequential raw data
        slide_window_params (list): A list containing all sets of slide window
            parameters
        default_label (int): The default label for the data
        chunk_index_list (list(int)): A list of numbers as the next chunk numbers
            for all slide window sets

    Returns:
        temp_chunk_df_dict (dict(Pandas DataFrame)): A dictionary for all new slide
            windows, keys represent the indices of slide window settings, values
            represent the DataFrames.
    """

    temp_chunk_df_dict = dict()
    total_row_length = raw_df.shape[0]
    for index in list(range(len(slide_window_params))):
        window_length = slide_window_params[index]["window_length"]
        slide_interval = slide_window_params[index]["slide_interval"]

        # Check if it's the correct total length to generate new chunk
        # If not, discard this slide window parameter setting
        if not is_correct_length(total_row_length,
                                    window_length,
                                    slide_interval):
            continue

        # Make a REFERENCE for the new chunk
        temp_chunk_df = raw_df.loc[total_row_length-window_length\
                                    :total_row_length,:]
        
        # Check if all labels in the current chunk are the same(clean)
        # If not, discard it
        if not are_valid_labels(temp_chunk_df, default_label):
            continue

        # Generate new chunk

        # Allocate memory for the new chunk
        temp_chunk_df = temp_chunk_df.copy()
        
        # Add chunk number to all rows in this chunk
        chunk_index = chunk_index_list[index]
        chunk_number_list = [chunk_index] * window_length
        temp_chunk_df['chunk'] = chunk_number_list

        # Update temp chunk dict with the new chunk
        temp_chunk_df_dict[index] = temp_chunk_df.reset_index(drop=True)
    return temp_chunk_df_dict


def is_correct_length(total_row_length, window_length, slide_interval):
    """Check if it's the correct total length to generate new chunk

    Args:
        total_row_length (int): The total number of rows of the raw data
        window_length (int): The number of rows for this slide window
        slide_interval (int): The step size for this slide window

    Returns:
        [type]: [description]
    """
    flag = (total_row_length>= window_length) and\
        (total_row_length-window_length)%slide_interval == 0
    return flag

def are_valid_labels(temp_chunk_df, default_label):
    """Check if the lebels of the chunk are valid

    Valid means:
    1. All labels are the same
    2. All labels are not the default label

    Args:
        temp_chunk_df (Pandas DataFrame): The current chunk

    Returns:
        bool: True if the labels are valid, otherwise False
    """
    
    label_column = temp_chunk_df.loc[:,["label"]].to_numpy()

    are_same = (label_column[0]==label_column).all()
    
    not_default = (default_label!=label_column).all()

    flag = are_same and not_default

    return flag