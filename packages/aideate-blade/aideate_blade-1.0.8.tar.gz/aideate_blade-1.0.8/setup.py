from setuptools import setup, find_packages


setup(
    name='aideate-blade',
    version='1.0.8',
    description='web content aideate_scraper',
    author='Aideate',
    author_email='xiaye@aideate.ai',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        "pydantic==2.6.1",
        "ipdb==0.13.11",
        "simplejson==3.17.6",
        "boto3==1.29.6",
        "boto3[crt]==1.29.6",
        "sqlalchemy==2.0.5.post1",
        #"psycopg2==2.9.5",
        "scrapetube==2.3.1",
        "overrides==7.3.1",
        "snakemd==2.1.0",
        "html2text==2020.1.16",
        "playwright==1.35.0",
        "prometheus-client==0.20.0",
        "extraction==0.3",
        "pdfplumber==0.11.0",
        "stripe==5.5.0",
        "python-magic==0.4.27",
        "StrEnum==0.4.15",
        "modal==0.61.105",
        "setuptools==69.5.1",
        "tenacity==8.0.1",
        "httpx==0.21.0",
        "wandb==0.17.0",
        "docstring_parser==0.16",
    ],
)