# coding utf8
import setuptools
from biogeoloc.versions import get_versions

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="biogeoloc",
    version=get_versions(),
    author="Yuxing Xu",
    author_email="xuyuxing@mail.kib.ac.cn",
    description="A python package for plotting correlations between variants and environmental factors.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://github.com/SouthernCD/GeoGenoPlot",
    include_package_data = True,

    # entry_points={
    #     "console_scripts": ["HugeP2G = hugep2g.cli:main"]
    # },    

    packages=setuptools.find_packages(),

    install_requires=[
        "toolbiox>=0.0.46",
        "plotbiox>=0.0.2",
        "cyvcf2>=0.30.28"
    ],

    python_requires='>=3.5',
)