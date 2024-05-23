from setuptools import setup, find_packages

setup(
    name='cf_datapreprocessor',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'nltk',
    ],
    description='A data preprocessor for machine learning projects.',   
    author='fatmanur caliskan, cihan yilmaz',
    author_email='fatmanur.caliskan@stu.fsm.edu.tr, cihan.yilmaz@stu.fsm.edu.tr',

    python_requires='>=3.6',
)
