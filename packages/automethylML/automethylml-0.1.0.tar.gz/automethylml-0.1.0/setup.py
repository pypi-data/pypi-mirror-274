from setuptools import setup, find_packages

setup(
    name='automethylML',  # Replace with your package name
    version='0.1.0',  # Replace with your version
    author='Phillip Maire',
    author_email='phillip.maire@gmail.com',
    description='pipline and version control for classifying methylation data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PhillipMaire/automethylML',  # Replace with your project URL
    packages=find_packages(),
    classifiers=[
        # 'Programming Language :: Python :: 3',
        # 'License :: OSI Approved :: MIT License',
        # 'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # # List your dependencies here
        # 'dependency1',
        # 'dependency2',
    ],
    license='MIT',
)


# ____ ____ ____ ____ ____ ____
# DEBUGGING 

# https://stackoverflow.com/questions/42609943/what-is-the-use-case-for-pip-install-e

# once you have a setup.py file in root directory you can use this command to install package that automatically updates as you use it. this allows you to directly debug the code using hte debugger!!!!


# pip install -e .


# ____ ____ ____ ____ ____ ____
