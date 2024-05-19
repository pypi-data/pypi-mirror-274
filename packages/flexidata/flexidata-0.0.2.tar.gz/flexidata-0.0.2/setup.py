from setuptools import setup, find_packages

# Function to read the requirements from the requirements.txt file
def read_requirements():
    with open('requirements.txt', 'r') as req:
        return req.read().splitlines()

setup(
    packages=find_packages(),
    install_requires=read_requirements(),
    package_dir={"flexidata": "flexidata"}
)
