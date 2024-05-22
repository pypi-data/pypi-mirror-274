from setuptools import setup, find_packages

setup(
    name="chemical_safety",
    version="0.0.5",
    packages=find_packages(include=['chemical_safety', 'chemical_safety.*']),
    description="A package for retreiving chemical safety information",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Demetrios Pagonis",
    author_email="demetriospagonis@weber.edu",
    include_package_data=True,
    install_requires=[
        'pandas',
        'numpy',
        'jinja2',
        'requests',
        'Levenshtein',
        'natsort',
        'flask',
        'scipy',
        'rdkit'
    ],
    entry_points={
        'console_scripts': [
            'chemical-dashboard=chemical_safety.dashboard.app:dashboard',
        ],
    },
)
