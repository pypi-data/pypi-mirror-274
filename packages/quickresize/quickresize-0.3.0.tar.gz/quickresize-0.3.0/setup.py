from setuptools import find_packages, setup

readme = open('README.md').read()

setup(
    name='quickresize',
    packages=find_packages(),
    version='0.3.0',
    description='In-place resizing of images present in a folder',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Nityanand Mathur',
    license='MIT',
    install_requires=['tqdm', 'pillow'],
    entry_points={
        'console_scripts': [
            'resize=quickresize.resize:main'
        ]
    }
)
