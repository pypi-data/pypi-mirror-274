import os

def write_file():
    # Get user input
    file_type = input("Enter the file type (e.g., .txt, .js, .py): ")
    file_name = input("Enter the file name: ")
    content = input("Enter the content to be written: ")

    # Create the full file name
    full_file_name = file_name + file_type

    # Write the content to the file
    with open(os.path.join(os.getcwd(), full_file_name), 'w') as f:
        f.write(content)

    print(f"File '{full_file_name}' has been written successfully.")
