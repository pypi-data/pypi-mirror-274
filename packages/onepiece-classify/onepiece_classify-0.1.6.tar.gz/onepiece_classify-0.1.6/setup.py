from pathlib import Path
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    DESCRIPTION = fh.read()

setup(
    name="onepiece-classify",
    version="0.1.6",
    author="annur-afgoni",
    author_email="afgoniannur@gmmail.com",
    description="package to predict onepiece image character ",
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/lombokai/onepiece-classifier.git",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10.0",
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    # install_requires=['numpy', 'pandas', 'pyarrow', 'torch', 'torchvision'],
    # extras_require={
    #     "dev": ["autoflake==2.3.1", "black==24.4.2", "isort==5.13.2", 
    #             "jupyter", "matplotlib", "pre-commit==3.7.1", "pytest==6.2.5",
    #             "pytest-pythonpath==0.7.4", "seaborn"]
    #             },
)

# from setuptools import find_packages, setup

# with open("README.md", "r") as r:
#     DESCRIPTION = r.read()

# with open("requirements/main.txt", "r") as fd:
#     reqs = fd.read().splitlines()

# setup(
#     name="onepiece-classify",
#     version="0.1.0",
#     author="annur-afgoni",
#     author_email="afgoniannur@gmmail.com",
#     description="package to predict onepiece image character ",
#     long_description=DESCRIPTION,
#     long_description_content_type="text/markdown",
#     url="https://github.com/lombokai/onepiece-classifier.git",
#     python_requires=">=3.12.0",
#     install_requires=reqs,
#     extras_require={},
#     package_dir={"": "src"},
#     packages=find_packages(where="src", exclude=("tests", )),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#     ],
# )
