from setuptools import setup, find_packages

setup(
    name="xtractor",
    version="0.1.0",
    description="An educational tool for understanding web scraping concepts using X (formerly Twitter).",
    long_description="""\
This package is intended as an educational resource to illustrate web scraping concepts 
using Python. It is specifically designed to scrape X (formerly Twitter) for demonstrative purposes only. 
The creator of this package does not endorse nor encourage scraping X (formerly Twitter) in violation of their 
Terms of Service. This tool should not be used for any commercial or illegal purposes. By using this tool, 
you agree to adhere to X's Terms of Service and acknowledge that the creator of this package is not liable 
for any misuse or damages caused.""",
    long_description_content_type="text/plain",
    author="Ryan",
    author_email="ryan@kinnear.io",
    url="https://github.com/rskinnear/xtractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="education webscraping x twitter",
    install_requires=[
        "annotated-types==0.6.0",
        "attrs==23.2.0",
        "beautifulsoup4==4.12.3",
        "bs4==0.0.2",
        "certifi==2024.2.2",
        "cffi==1.16.0",
        "h11==0.14.0",
        "idna==3.6",
        "outcome==1.3.0.post0",
        "pycparser==2.21",
        "pydantic==2.6.3",
        "pydantic-settings==2.2.1",
        "pydantic_core==2.16.3",
        "PySocks==1.7.1",
        "python-dotenv==1.0.1",
        "selenium==4.18.1",
        "sniffio==1.3.1",
        "sortedcontainers==2.4.0",
        "soupsieve==2.5",
        "trio==0.24.0",
        "trio-websocket==0.11.1",
        "typing_extensions==4.10.0",
        "urllib3==2.2.1",
        "wsproto==1.2.0",
    ],
    python_requires=">=3.10",
)
