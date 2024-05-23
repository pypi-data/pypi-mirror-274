from setuptools import setup, find_packages
exec(open("composition_vectorizer/version.py").read())

setup(
    name='composition_vectorizer',  # Replace with your package's name
    version= __version__,  # Replace with your package's version
    author='Arindam Debnath',  # Replace with your name
    author_email='debnath@psu.edu',  # Replace with your email
    description='Converts string composition to numpy arrays',  # Provide a short description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # If your README is in markdown
    url='https://github.com/dovahkiin0022/composition_vectorizer.git',  # Replace with the URL to your repository
    packages=find_packages(),
    install_requires=[  # Specify your dependencies here
        "pymatgen>=2024.2.20", 
        "numpy>=1.25.0" # Use the correct pymatgen version
        # Add other dependencies as needed
    ],
    include_package_data=True,
    classifiers=[
        # Choose your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        # Add additional classifiers as appropriate for your project
    ],
    python_requires='>=3.9',  # Specify which Python versions you support
    # Add any additional package configuration here
)
