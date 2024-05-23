from setuptools import setup, find_packages

module_directory = 'talking_equipment'

setup(
    name="talking-equipment-sdk",
    version="0.0.9",
    author="Nathan Johnson",
    author_email="nathanj@stratusadv.com",
    description="Talking Equipment Standard Development Kit",
    long_description=open(f"{module_directory}/README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": module_directory},
    packages=find_packages(where=module_directory, exclude=["tests"]),
    include_package_data=True,
    python_requires=">=3.9",
)