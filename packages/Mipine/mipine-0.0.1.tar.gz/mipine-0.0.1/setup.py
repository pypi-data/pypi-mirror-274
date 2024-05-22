from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='Mipine',
    version='0.0.1',
    author='mipsirint',
    author_email='grigorevv972@gmail.com',
    description='Основанный на библиотеке PyGame игровой движок',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/mipsirint/Mipine',
    packages=find_packages(),
    install_requires=['pygame>=2.5.2'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    keywords='pygame game games engine',
    project_urls={
        'GitHub': 'https://github.com/mipsirint/Mipine'
    },
    python_requires='>=3.11'
)
