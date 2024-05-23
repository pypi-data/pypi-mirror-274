from setuptools import setup

setup(
    name='computage',
    version='0.1',
    description='A library for fullstack aging clocks design and benchmarking.',
    packages=['computage'],
    install_requires=[
        'scikit-learn',
        'scipy',
        'statsmodels',
        'pandas',
        'numpy',
        'tqdm',
        'matplotlib',
        'huggingface_hub'
    ],
    author_email='dmitrii.kriukov@skoltech.ru',
    zip_safe=False,
)
