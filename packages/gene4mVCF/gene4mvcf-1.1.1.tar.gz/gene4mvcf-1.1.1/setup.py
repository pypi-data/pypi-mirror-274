from setuptools import setup, find_packages
import subprocess

# Define a function to check if a command exists
def command_exists(cmd):
    return subprocess.run(['which', cmd], stdout=subprocess.PIPE).returncode == 0

# Define a list of required shell commands
required_commands = ['bcftools', 'bgzip', 'tabix']

# Check if all required commands exist
if not all(command_exists(cmd) for cmd in required_commands):
    raise RuntimeError("Please install the following dependencies: bcftools, bgzip, tabix")

setup(
    name='gene4mVCF',
    version='1.1.1',
    description='Description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pr (France). Dr. rer. nat. Vijay K. ULAGANATHAN',
    author_email='vijay-kumar.ulaganathan@uni-tuebingen.de',
    url='https://github.com/VJ-Ulaganathan/gene4mVCF',
    packages=find_packages(),
    package_data={'gene4mVCF': ['hg19.ensGene.bed', 'hg19.ncbiRefSeq.bed', 'hg38.ensGene.bed', 'hg38.ncbiRefSeq.bed']},
    install_requires=[
        'pysam>=0.16.0.1',
        'pandas>=1.0.0',
        'pybedtools>=0.8.0',
        'tqdm>=4.47.0',
        'gffutils>=0.10.1'
    ],
    entry_points={
        'console_scripts': [
            'gene4mVCF=gene4mVCF.fetchgenes:main'
        ]
    },
    include_package_data=True,
)

