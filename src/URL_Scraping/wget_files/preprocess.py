import os

def read_folders(root_path):
    """
    Reads HTML files from nested folders.
    Returns a list of type(list) of HTML files.
    """
    html_contents = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r',  encoding='ISO-8859-1') as file:
                    html_contents.append(file.read())
    return html_contents