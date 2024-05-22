import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


kwargs = dict(
    name="lljz_tools",
    version="0.2.16.2",
    author="liulangjuanzhou",
    author_email="liulangjuanzhou@gmail.com",
    description="常用工具封装",
    long_description_content_type="text/markdown",
    url="",
    package_data={
        "my_tools": ["*.html", "*.js"]
    },
    install_requires=['openpyxl', 'gevent', 'colorlog>=6.8.2'],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
setuptools.setup(
    **kwargs,
    long_description=long_description,
    packages=setuptools.find_packages(),
)
