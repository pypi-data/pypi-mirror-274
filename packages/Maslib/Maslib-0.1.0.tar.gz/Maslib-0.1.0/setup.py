from setuptools import setup, find_packages

setup(
    name='Maslib',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'phik',
        'matplotlib',
        'scikit-learn',
        'catboost',
        'joblib',
        'wordcloud'
    ],
    author='Alecsandr_C.V.V',
    author_email='dxomko@gmail.com',
    description='Это моя библиотека для оптимизации кода для python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
