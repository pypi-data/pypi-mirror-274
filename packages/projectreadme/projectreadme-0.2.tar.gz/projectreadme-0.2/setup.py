from setuptools import setup, find_packages


setup(
    name='projectreadme',
    version='0.2',
    packages= find_packages(),
    install_requires=[
        'google-generativeai',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'generate-readme = projectreadmegenerator.generator:generatereadmefile'
        ]
    },
    author='Anmol Dhiman',
    author_email='anmoldhimand666@gmail.com',
    description='A package for generating Project README files for a github project',
    long_description= open('README.md', encoding= "utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Anmol-STRS/projectreadmegenerator',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
