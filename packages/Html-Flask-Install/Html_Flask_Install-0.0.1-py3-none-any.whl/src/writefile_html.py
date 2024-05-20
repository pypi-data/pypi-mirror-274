import os

# Define the directory and file name
dir_name = 'templates'
file_name = 'index.html' 
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
        <script src="{{ url_for('static', filename='js/script.js') }}"></script>
    </head>
    <body>
        <!-- rest of your HTML code -->
    </body>
    <footer>
    </footer>
    </html>
    """

# Create the directory if it doesn't exist
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# Define the full file path
file_path = os.path.join(dir_name, file_name)

# Write to the file
with open(file_path, 'w') as my_file:
    my_file.write(html_content)
