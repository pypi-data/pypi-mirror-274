import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dyDNS",
    version="0.0.12",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="activating dynamicDNS for freedns.afraid.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/y-takefuji/dyDNS",
    project_urls={
        "Bug Tracker": "https://github.com/y-takefuji/dyDNS",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['dydns'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'dydns = dydns:main'
        ]
    },
)
