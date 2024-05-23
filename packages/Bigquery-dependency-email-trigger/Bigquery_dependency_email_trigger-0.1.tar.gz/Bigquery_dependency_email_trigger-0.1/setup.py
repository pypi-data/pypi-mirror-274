from setuptools import setup, find_packages

with open('README.md', "r") as f:
    description = f.read()

setup(
    name = 'Bigquery_dependency_email_trigger',
    version = '0.1',
    packages = find_packages(),
    install_requires = [],
    entry_points = {"console_scripts" : [
        "Bigquery_dependency_email_trigger = Bigquery_dependency_email_trigger:bigquery_dependency_email_trigger",
    ],},
    long_description=description,
    long_description_content_type="text/markdown",
)