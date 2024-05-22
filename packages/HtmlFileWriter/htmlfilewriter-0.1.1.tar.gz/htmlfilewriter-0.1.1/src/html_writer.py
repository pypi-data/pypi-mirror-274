import os

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

    with open(os.path.join('index.html'), 'w') as f:
        f.write(html_content)
    
    return