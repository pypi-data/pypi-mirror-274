import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swdata",
    version="0.0.1",
    author="sw",
    author_email="",
    include_package_data=True,
    description="data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
	license='MIT',
    packages=setuptools.find_packages(),
    python_requires='>=3.6, <4',
    install_requires=["netifaces>=0.11.0",
                      "django-redis>=5.0.0"
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
