import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='multi-interface',
    version="0.0.2",
    author='Chao',
    description='reflection and deflection between Crust1.0 and Vertical Gravity Gradient',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/WangChao/Chao-interface',
    include_package_data=True,
    package_data={
        'multi_interface': ['crust1.0/crust1.bnds', 'crust1.0/crust1.rho',
                                      'gravities/delta-g-3.dg', 'gravities/delta-g-5.dg']
    },
    python_requires='>=3.6',
    install_requires=[
        'matplotlib>=3.8.4',
        'numpy>=1.26.4',
        'scikit-image>=0.22.0'
    ]
)
