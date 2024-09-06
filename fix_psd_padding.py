from hashlib import new
import os
import re
import sys

# Check if a command-line argument is provided
if len(sys.argv) > 1:
    # Use the provided directory path
    directory = sys.argv[1]
    print('running in a path')
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        # Use regular expression to search for the pattern
        match = re.search(r'.*?_(\d{4})_(?!.*_\d{4}_)', filename)
        print(match)
        if match and filename[-4:] == '.png':
            # Remove the matched pattern
            new_filename = match.group() + re.sub(r'.*?_(\d{4})_(?!.*_\d{4}_)', '_', filename)[6:]
            print('new filename ' , new_filename)
            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

print('running')
