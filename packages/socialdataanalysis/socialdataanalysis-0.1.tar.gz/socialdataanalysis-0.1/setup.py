from setuptools import setup, find_packages

setup(
    name='socialdataanalysis',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'statsmodels',
        'scipy',
        'matplotlib',
        'sympy',
        'prince',
        'altair'
    ],
    description='Funções personalizadas para análise de dados nas ciências sociais, complementando o uso do SPSS.',
    author='Ricardo Mergulhao',
    author_email='ricardomergulhao@gmail.com',
    url='https://github.com/rcmergulhao/socialdataanalysis',  # Atualize com o URL do seu repositório
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
