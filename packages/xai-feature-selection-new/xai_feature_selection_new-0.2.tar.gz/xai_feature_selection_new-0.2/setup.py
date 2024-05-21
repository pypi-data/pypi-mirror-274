from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

DESCRIPTION = 'Feature selection using XAI'
LONG_DESCRIPTION = 'allows to select best features using XAI by combining with local and global importance'

# Setting up
setup(
    name="xai_feature_selection_new",
    version="0.2",
    author="Yaganteeswarudu Akkem",
    author_email="yaganteeswaritexpert@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[ 'pandas==2.0.*','lime', 'shap'],
    keywords=['machine learning', 'feature selection', 'explainable artificial intelligence', 'XAI'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
