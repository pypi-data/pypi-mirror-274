import os

def home_dir():
    import os

    # Print the home directory
    home_dir = os.path.expanduser("~")
    print(f"Home Directory: {home_dir}")

    # Ask for user input
    new_dir = input("Enter the directory to change into or create: ")

    # Check if the directory exists
    if os.path.exists(new_dir):
        # Change the current working directory
        try:
            os.chdir(new_dir)
            print(f"Successfully changed the current directory to {new_dir}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        # Create the new directory
        try:
            os.makedirs(new_dir)
            print(f"Successfully created the new directory: {new_dir}")
        except Exception as e:
            print(f"An error occurred: {e}")

    return home_dir()

