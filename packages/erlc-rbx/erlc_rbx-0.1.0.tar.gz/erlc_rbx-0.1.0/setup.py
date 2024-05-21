import pathlib
import setuptools

setuptools.setup(
    name="erlc-rbx",
    version="0.1.0",
    description="a better (and open-source) wrapper for the ERLC api.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/thatgurkangurk/gurkz.me",
    author="Gurkan",
    author_email="hello@gurkz.me",
    license="GPL 3.0",
    project_urls={
        "Source": "https://github.com/thatgurkangurk/erlc.py",
        "Bug Tracker": "https://github.com/thatgurkangurk/erlc.py/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10,<3.14",
    install_requires=["requests>=2.32"],
    packages=setuptools.find_packages(),
    include_package_data=True,
)
