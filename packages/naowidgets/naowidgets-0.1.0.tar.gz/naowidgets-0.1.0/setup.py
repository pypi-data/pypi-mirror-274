from setuptools import setup, find_packages

setup(
    name='naowidgets',
    version='0.1.0',
    package_dir={'': 'src'},
    py_modules=['naowidgets'],
    install_requires=[
        'ipywidgets',
        'IPython'
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A small library for NAO widgets',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NaosClassroom/naowidgets',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
