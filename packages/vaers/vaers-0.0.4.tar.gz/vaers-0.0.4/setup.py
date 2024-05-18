import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vaers",
    version="0.0.4",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="A package for adverse effects on death using VAERS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/y-takefuji/safety_vaccine",
    project_urls={
        "Bug Tracker": "https://github.com/y-takefuji/safety_vaccine",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['vaers'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'vaers = vaers:main'
        ]
    },
)
