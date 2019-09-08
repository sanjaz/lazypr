from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lazypr",
    version="0.1.2",
    description="Creating a pull request on GitHub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sanja Segan",
    author_email="sanjazivotic@gmail.com",
    url="https://github.com/sanjaz/lazypr",
    packages=find_packages(),
    include_package_data=True,
    test_suite="tests",
    install_requires=["PyGithub", "pygit2"],
    extras_require=None,
    tests_require=["mock", "pytest<5.0"],
    entry_points={"console_scripts": ["lazypr = lazypr.main:main"]},
)
