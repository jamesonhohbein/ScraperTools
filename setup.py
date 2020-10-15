from setuptools import setup

# run package setup
setup(
    name="scrapers",

    # define paths to submodules
    packages=["scrapers", "scrapers/scrape", "scrapers/extract", "scrapers/process"],
    
    # install packages from requirements.txt
    install_requires=[package.strip() for package in open('requirements.txt', 'r').readlines()],
)
