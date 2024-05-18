from setuptools import setup

setup(
    name='query_to_df',
    version='0.1',
    description='A function to convert database query results to DataFrame',
    author='Elias Attias',
    author_email='attiaselias@gmail.com',
    py_modules=['query_to_df'],  # Replace with your module name
    install_requires=['pandas','snowflake.connector'],  # Add any dependencies here
)
