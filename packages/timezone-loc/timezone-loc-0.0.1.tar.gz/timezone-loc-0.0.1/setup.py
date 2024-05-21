from setuptools import setup, find_packages

setup(
    name="timezone-loc",
    version="0.0.1",
    author="Abhilasha Jaishal",
    author_email="abhilasha.jaishal@anko.com",
    description="An application that informs you of the time in different locations and timezones",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["click", "pytz"],
    entry_points={"console_scripts": ["timezone-loc = src.main:main"]},
)
