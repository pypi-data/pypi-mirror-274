import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("LICENSE", "r") as fh:
    license_text = fh.read()

setuptools.setup(
    name="dzidb",
    version="1.0.14",
    author="Your Name",
    author_email="your.email@example.com",
    description="A custom adb-like tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dzidb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 示例：MIT License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dzidb = dzidb.__main__:main',
        ],
    },
    license=license_text,  # 添加许可证信息
)