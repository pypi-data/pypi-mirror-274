import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chaoren2_01",
    version="0.0.1",
    author="chaoren2",
    author_email="chaoren2@naver.com",
    description="chaoren2 sample lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/play3s/ctv_protector",
    project_urls={
        "Bug Tracker": "https://github.com/play3s/ctv_protector",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)