from setuptools import find_packages, setup

REQUIRED_PKGS = [
    'spacy>=3.7.4',
    'pyphen>=0.15.0',
    'editdistance==0.8.1',
    'sentence-transformers>=2.7.0',
]

setup(
    name='italian-ats-evaluator',
    install_requires=REQUIRED_PKGS,
    test_suite='tests',
    packages=find_packages(exclude={"tests"}),
    package_data={'ats_evaluator': ['nvdb/*.txt']},
    include_package_data=True,
    python_requires=">=3.7",
    version="1.0.0",
    author="RedHitMark",
    url="https://github.com/RedHitMark/italian-ats-evaluator",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)