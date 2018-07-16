from setuptools import setup

setup(
    name='lemma_tokenizer',
    author='Patrick lee',
    author_email='lee.patrickmunseng@gmail.com',
    packages=['lemma_tokenizer'],
    description='lemma tokenizer class',
    platforms='Linux, MacOSX',
    install_requires=[
        'nltk',
        'pandas',
        'numpy'
        'nltk.corpus',
        'nltk.stem'
    ],
    url='github.com/kcirtap2014/LemmaTokenizer.git'
)
