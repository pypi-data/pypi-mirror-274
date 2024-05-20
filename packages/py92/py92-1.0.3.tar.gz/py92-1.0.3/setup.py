from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py92",  # 包的名称
    version="1.0.3",  # 包的版本
    author="Stanley SUN",  # 作者名称
    author_email="stanleysun233@163.com",  # 作者邮箱
    description="Python Packages for Labeling(985/211/双一流/本科) Schools in China",  # 简短描述
    long_description=long_description,  # 长描述，通常从 README.md 文件中读取
    long_description_content_type="text/markdown",
    url="https://github.com/stanleysun233/py92",  # 项目主页
    packages=find_packages(),  # 自动找到项目中的包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',  # 依赖的Python版本
    package_data={
        'py92': ['cn_schools.csv',
                 'qs2024.csv'],
    },
    install_requires=[
        "pandas"
    ],
)
