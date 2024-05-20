from pathlib import Path

from setuptools import find_packages, setup

# Read the contents of README file
source_root = Path(".")
with (source_root / "README.md").open(encoding="utf-8") as f:
    long_description = f.read()

# Read the requirements
# with (source_root / "requirements.txt").open(encoding="utf8") as f:
#     requirements = f.readlines()

try:
    version = (source_root / "VERSION").read_text().rstrip("\n")
except FileNotFoundError:
    version = "0.0.dev0"

setup(
    name="pipy-test-xiaoqiang",
    version=version,
    author="Ma Xiaoqiang",
    author_email="851788096@qq.com",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.7",
    classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent",
            "Topic :: Scientific/Engineering",
        ]
)