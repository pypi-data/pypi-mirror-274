from setuptools import setup, find_packages


# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()
long_description='Mahdi Hasan Shuvo'
setup(
    name="fb_atm",
    version='0.1.8.2',
    author="Mahdi Hasan Shuvo",
    author_email="shvo.mex@gmail.com",
    url="https://www.facebook.com/bk4human",
    description="An application that informs you of the different modules and very easy to use.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["click", "pytz"],
    entry_points={"console_scripts": ["cloudquicklabs1 = src.main:main"]},
    project_urls={
        "GitHub": "https://github.com/Shuvo-BBHH/",
        "Bug Reports": "https://www.facebook.com/bk4human",
        "Source": "https://github.com/Shuvo-BBHH/mahdix",
    },
    keywords="Shuvo-BBHH, MAHDI HASAN, Shuvo BBHH, Bk4kuman",
    license="MIT",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
)
