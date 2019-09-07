from setuptools import find_packages, setup

readme = open('README.md').read()

setup(
    name="lazypr",
    version="0.1.1",
    description="Creating a pull request on GitHub",
    long_description=readme,
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
