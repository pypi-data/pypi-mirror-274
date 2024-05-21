import os

# Define the directory and file name
dir_name = 'static'
file_name = 'scripts.js' 
js_content = """
    $(document).ready(function(){
        $("#clickme").click(function(){
            alert("Button clicked!");
        });
    });
    """

# Create the directory if it doesn't exist
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# Define the full file path
file_path = os.path.join(dir_name, file_name)

# Write to the file
with open(file_path, 'w') as my_file:
    my_file.write(js_content)
