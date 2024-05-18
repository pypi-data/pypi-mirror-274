from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gwas2vcf",
    version="0.1.6",
    author="Pr (France). Dr. rer. nat. Vijay K. ULAGANATHAN",
    author_email="vijay-kumar.ulaganathan@uni-tuebingen.de",
    description="A tool to convert GWAS TSV files to VCF format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VJ-Ulaganathan/gwas2vcf/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11.6',
    install_requires=[
        'pandas',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'gwas2vcf=gwas2vcf.convert_to_vcf:main',
        ],
    },
)

