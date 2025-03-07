import os
import subprocess

# Define the port you want to use
PORT = 8080

# Set the environment variable for the port
os.environ['CHALICE_LOCAL_PORT'] = str(PORT)

# Run the Chalice local server with the specified port
subprocess.run(["chalice", "local", "--port", str(PORT)])
