import os
from tkinter.filedialog import asksaveasfile
from tkinter import *

def create_index_html():
    js_content = """
    $(document).ready(function(){
        $("#clickme").click(function(){
            alert("Button clicked!");
        });
    });
    """
    # Get user input
    
    file_name = input("Enter the file name: ")
    content = input(js_content)

    # Write the content to the file
    with open(os.path.join(os.getcwd(), file_name), 'w') as f:
        f.write(content)

    print(f"File '{file_name}' has been written successfully.")

    asksaveasfile()

    with open(os.path.join('index.html'), 'w') as f:
        f.write(js_content)
    
    return