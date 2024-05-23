from setuptools import setup

setup(
    name='subfinder-leakix',  # Descriptive and consistent with project name
    version='6',
    description='Extracts subdomains from a given domain using various techniques',  # Clear and concise description
    author='Jhonson12',
    author_email='wannaajhonson@gmail.com',
    url='https://github.com/Jhonsonwannaa/subfinder-by-leakix',  # Correct project URL
    install_requires=[  # Replace with actual dependencies (if any)
        'requests',  # Example dependency for making HTTP requests
    ],
    # Removed packages entry since you haven't created modules yet
    package_data={
        'subfinder': ['LICENSE', 'README.md'],  # Include essential files from root directory
    },
    entry_points={  # Create an executable script (optional)
        'console_scripts': ['subfinder-leakix=main:main'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
