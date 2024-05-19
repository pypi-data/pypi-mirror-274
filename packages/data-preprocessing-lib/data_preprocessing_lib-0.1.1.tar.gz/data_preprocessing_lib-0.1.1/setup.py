from setuptools import setup, find_packages

setup(
    name='data_preprocessing_lib',
    version='0.1.1',
    description='A easy peasy comprehensive library for data preprocessing tasks',
    author='Mehdi Miraç ARAT, Latif Şimşek',
    author_email='mehdimirac.arat@stu.fsm.edu.tr, latif.simsek@stu.fsm.edu.tr',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'nltk',
    ],
    python_requires='>=3.6',
)