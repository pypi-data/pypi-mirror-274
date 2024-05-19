from setuptools import setup, find_packages

setup(
    name='pop_sort',
    version='0.2',
    description='Project for exploring popular sorting algorithms.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/MartynasGr/pop_sort',
    author='Martynas Greičius',
    author_email='martynas.greicius@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
