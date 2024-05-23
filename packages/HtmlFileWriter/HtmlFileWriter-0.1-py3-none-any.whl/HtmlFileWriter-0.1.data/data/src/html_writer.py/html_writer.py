import os
from tkinter.filedialog import asksaveasfile
from tkinter import *

def create_index_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="EN">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>FlaskApplication</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="">
        <script src="#"></script>
    </head>
    <body>
        <!-- rest of your HTML code -->
    </body>
    <footer>
    </footer>
    </html>
    """
    # Get user input
    
    file_name = input("Enter the file name: ")
    content = input(html_content)

    # Write the content to the file
    with open(os.path.join(os.getcwd(), file_name), 'w') as f:
        f.write(content)

    print(f"File '{file_name}' has been written successfully.")

    asksaveasfile()

    with open(os.path.join('index.html'), 'w') as f:
        f.write(html_content)
    
    return