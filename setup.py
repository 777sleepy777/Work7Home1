from setuptools import setup, find_packages

setup(
    name='clean_foder',
    version='0.0.1',
    description='Clean files in folder',
    author='Annette',
    author_email='ankamorozka@outlook.com',
    license='MIT',
    packages=find_packages(),
    #install_requires=['markdown'],
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)