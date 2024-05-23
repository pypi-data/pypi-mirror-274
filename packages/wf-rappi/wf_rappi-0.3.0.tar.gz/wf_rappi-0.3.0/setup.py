from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="wf_rappi",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.11.1',
        'pandas>=1.0',
        'matplotlib==3.8.3',
        'openpyxl==3.1.2',
        'packaging==23.2',
        'pillow==10.2.0',
        'psycopg2==2.9.9',
        'pyarrow==15.0.0',
        'pydantic==2.5.3',
        'pydantic-core==2.14.6',
        'requests==2.31.0',
        'scikit-learn==1.3.2',
        'snowflake-connector-python==3.7.1',
        'snowflake-snowpark-python==1.13.0',
        'SQLAlchemy==1.4.51',
        'twine==5.1.0',
        'xgboost==2.0.3'
    ],
    entry_points={
        "console_scripts": [
            "wf-rappi = wf_rappi.main:distribute_orders",
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)