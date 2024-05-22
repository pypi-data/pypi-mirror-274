from setuptools import setup, find_packages

# Function to read the requirements from the file
def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Filter out comments and empty lines
        parsed_requirements = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    return parsed_requirements

# Parse requirements
requirements = parse_requirements('requirements.txt')

# print(f"++++++++++++++++++++++++++++requirements: {requirements}")


setup(
    packages=find_packages(),
    install_requires = requirements,
    entry_points={
        'console_scripts': [
            'hc_log_tools = src.entry:entry',
        ]
    },
)