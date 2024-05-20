from setuptools import setup, find_packages

setup(
    name='my_cpp_package',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],  # Add any dependencies here
    data_files=[('bin', ['image_processor'])],  # Adjust the path if needed
)

