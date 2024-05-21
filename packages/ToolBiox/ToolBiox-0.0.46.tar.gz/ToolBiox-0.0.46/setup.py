# coding utf8
import setuptools
from toolbiox.versions import get_versions

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="ToolBiox",
    version=get_versions(),
    author="Yuxing Xu",
    author_email="xuyuxing@mail.kib.ac.cn",
    description="a biological toolkit for genome assembly, annotation and analysis that we have accumulated from our bioinformatics work",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://github.com/SouthernCD/ToolBiox",

    packages=setuptools.find_packages(),

    install_requires=[
        "bcbio-gff>=0.6.6",
        "biopython<=1.80",
        "interlap>=0.2.6",
        "matplotlib>=3.5.0",
        "networkx>=2.4",
        "numpy>=1.18.1",
        "pandas>=1.0.1",
        "pyfaidx>=0.5.5.2",
        # "pysam==0.17.0",
        "pysam>=0.21.0",
        "PyVCF3>=1.0.3",
        "retry>=0.9.2",
        "scipy>=1.4.1",
        "lxml>=4.4.1",
        "pingouin>=0.2.7",
        "fitter>=1.2.3",
        "mlxtend>=0.17.2",
        "cloudpickle>=2.2.0",
        "geopandas>=0.14.3",
        "rasterio>=1.3.10",
        "shapely>=2.0.4",
    ],

    include_package_data=True,

    python_requires='>=3.5',

)
