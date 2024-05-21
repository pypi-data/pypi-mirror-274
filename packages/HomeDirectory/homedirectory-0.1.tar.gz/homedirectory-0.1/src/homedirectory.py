import os

def hd():

    # Get the home directory
    home_directory = os.path.expanduser('~')
    # Print the Home Directory
    hdprint = print(f"Home directory: {home_directory}")
    
    return print(hd())