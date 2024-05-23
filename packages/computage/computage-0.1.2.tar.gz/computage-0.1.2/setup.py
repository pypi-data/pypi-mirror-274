from setuptools import setup, find_packages

setup(
    name='computage',
    version='0.1.2',
    description='A library for full-stack aging clocks design and benchmarking.',
    packages=find_packages(),
    package_data={
            '': ['*.csv']
        },
    install_requires=[
        'scikit-learn',
        'scipy',
        'statsmodels',
        'pandas',
        'numpy',
        'tqdm',
        'matplotlib',
        'seaborn',
        'huggingface_hub',
        'plottable',
    ],
    author_email='dmitrii.kriukov@skoltech.ru',
    zip_safe=False,
)
