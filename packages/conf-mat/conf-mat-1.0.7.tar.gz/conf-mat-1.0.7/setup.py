from setuptools import setup, find_packages

setup(
    name="conf-mat",
    version="1.0.7",
    author="khiat Mohammed Abderrezzak",
    author_email="khiat.abderrezzak@gmail.com",
    license="MIT",
    description="Sophisticate Confusion Matrix",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/conf-mat/",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'conf_mat': ['conf_Mat_Ex.png'],
    },
    install_requires=[
        "tabulate>=0.9.0",
        "matplotlib>=3.8.3",
    ],
    keywords=[
        "confusion matrix",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
