import os
import subprocess
import tkinter
import time

# very simple script. creates a directory, creates a virtual environment, creates tkinter ui
# everything written in tkinter ui notepad is saved to directory, corrupted, and then thrown into the virtual environment.
# basically, acting as a digital version of erasable/fade ink.

dir_name = input("Enter the name of the directory: ")
file_name = ''

# create a virtual anaconda environment
# check to see if conda environment with the dir_name exists, store in list

def create_anaconda_env(dir_name):
    conda_check = subprocess.run(["conda", "env", "list"], capture_output=True, text=True)

    # if dir_name is in captured output, use that environment
    if dir_name in conda_check.stdout:
        print("Anaconda environment already exists. We'll use that.")
    else:
        print("Creating Anaconda environment")

        # using python 3.8 or above as I'm on silicon mac
        conda_env = subprocess.run(["conda", "create", "-n", dir_name, "python=3.8"])

        try:
            conda_env.check_returncode()
            print("Anaconda environment created successfully")
        except subprocess.CalledProcessError:
            print("Anaconda environment failed to create")

# make corrupt.sh executable
subprocess.run(["chmod", "+x", "corrupt.sh"])

# create the directory
def create_dir(dir_name):
    # does it already exist?
    if os.path.exists(dir_name):
        print("Directory already exists. We'll use that.")
    else:
        os.mkdir(dir_name)
        print("Directory created successfully")

# using tkinter, create a basic notepad ui
def window_tk(dir_name):
    window = tkinter.Tk()
    window.title("*~* diary corrupt *~*")

    text_area = tkinter.Text(window)
    text_area.pack()

    button = tkinter.Button(window, text="Save")
    button.pack()

    # create a function to save the text to the directory
    def save_text():
        text = text_area.get("1.0", "end-1c")

        # create a file with the time & date in filename, write to file
        file_name = time.strftime("%Y%m%d-%H%M%S") + ".txt"
        with open(file_name, "w") as file:
            file.write(text)

        # move the file to the user directory
        subprocess.run(["mv", file_name, dir_name])
        print("File saved successfully")
        return file_name
    
    button.config(command=save_text)

    # once save is hit, close tkinter window
    def close_window():
        window.destroy()
    
    button.config(command=close_window)
    window.mainloop()


# there's no need for a crontab as this runs right after it's written!
# file gets corrupted and thrown into the ether (anaconda environment)
def watch_dir(dir_name, file_name):

    # just corrupt file
    subprocess.run(["./corrupt.sh", file_name])

    # then move all contents of dir_name into the anaconda environment with the same name
    subprocess.run(["mv", dir_name, f"~/anaconda3/envs/{dir_name}"])
    print("Files corrupted and moved to anaconda environment, into the ether.")

if __name__ == "__main__":
    create_anaconda_env(dir_name)
    create_dir(dir_name)
    window_tk(dir_name)
    watch_dir(dir_name, file_name)
