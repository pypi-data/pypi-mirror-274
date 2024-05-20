from setuptools import setup, find_packages

setup(
    name = 'plum-project',
    version = '1.0.1',
    description = 'A python data job framework to simplify development and operations.',
    long_description = 'A python data job framework to simplify development and operations.',
    long_description_content_type = "text/markdown",
    keywords = ['data', 'etl', 'jobs'],
    packages = find_packages(),
    install_requires = [
        'psycopg[binary]==3.1.16',
        'requests==2.31.0',
        'python-dotenv==1.0.1',
        'boto3==1.34.64',
        'botocore==1.34.64'
    ]
)
