from pathlib import Path
from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open(Path(__file__).parent / "dagster_pydantic/version.py", encoding="utf8") as fp:
        exec(fp.read(), version)  # pylint: disable=exec-used

    return version["__version__"]


ver = get_version()
# dont pin dev installs to avoid pip dep resolver issues
pin = "" if ver == "0+dev" else f"=={ver}"
setup(
    name="dagster-pydantic",
    version=ver,
    author="Mitchell Hynes",
    author_email="me@mitchellhynes.com",
    license="Apache-2.0",
    description=("Integration layer for dagster and pydantic."),
    url="https://github.com/ecumene/dagster-pydantic",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["dagster_pydantic_tests*"]),
    include_package_data=True,
    install_requires=[f"dagster{pin}", "pydantic"],
    extras_require={
        "test": [
            "pytest",
        ],
    },
)
