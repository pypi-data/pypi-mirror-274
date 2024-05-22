from setuptools import setup, find_packages

setup(
    name="chemical_safety",
    version="0.0.2",
    packages=find_packages(include=['chemical_safety', 'chemical_safety.*']),
    description="A package for retreiving chemical safety information",
    author="Demetrios Pagonis",
    author_email="demetriospagonis@weber.edu",
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
