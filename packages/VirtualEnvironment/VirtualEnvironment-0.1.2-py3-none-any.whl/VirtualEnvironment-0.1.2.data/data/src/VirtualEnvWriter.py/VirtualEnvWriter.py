from virtualenv import BuildVenv
import os

file_path = os.getcwd()

# Write to the folder
with open(file_path, 'w') as app:
    app.write(BuildVenv.VirtEnv())

