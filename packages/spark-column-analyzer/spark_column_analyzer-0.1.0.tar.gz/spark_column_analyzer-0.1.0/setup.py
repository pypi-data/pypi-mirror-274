from setuptools import setup, find_packages

setup(
    name='spark-column-analyzer',
    version='0.1.0',  # Update the version number as needed
    packages=find_packages(where="src"),  # Automatically find packages in the 'src' directory
    package_dir={"": "src"},  # Specify the package directory
    author='Mich Talebzadeh',
    author_email='mich.talebzadeh@gmail.com',
    description='A package for analyzing PySpark DataFrame columns',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/michTalebzadeh/spark_column_analyzer',  # Update the URL to your package repository
    install_requires=[
        'pyspark',  # Add any dependencies required by your package
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

