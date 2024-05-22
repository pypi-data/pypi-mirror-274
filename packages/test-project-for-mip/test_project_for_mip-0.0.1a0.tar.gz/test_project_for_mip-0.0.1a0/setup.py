from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='test-project-for-mip',
    version='0.0.1-alpha',
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
