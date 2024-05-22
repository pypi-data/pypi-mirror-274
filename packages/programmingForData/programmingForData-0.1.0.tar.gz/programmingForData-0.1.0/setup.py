from setuptools import setup, find_packages

setup(
    name='programmingForData',
    version='0.1.0',
    author='Beyza Nur Sevigen, Meryem Kilic',
    author_email='beyzanur.sevigen@stu.fsm.edu.tr, meryem.kilic@stu.fsm.edu.tr',
    description='A comprehensive library for data preprocessing tasks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/beyzasevigen/programmingForData',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.1.5',
        'numpy>=1.19.5',
        'scikit-learn>=0.24.2',
        'matplotlib>=3.3.4',
        'seaborn>=0.11.1',
        'nltk>=3.6.1',
        'scipy>=1.6.2'
    ],
)