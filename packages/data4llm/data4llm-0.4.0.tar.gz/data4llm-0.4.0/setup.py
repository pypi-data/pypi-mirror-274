import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data4llm",  # 用自己的名替换其中的YOUR_USERNAME_
    version="0.4.0",  # 包版本号，便于维护版本
    author="SweeneyHe",  # 作者，可以写自己的姓名
    author_email="sweeneyandhe@gmail.com",  # 作者联系方式，可写自己的邮箱地址
    description="Add apply_multi and other bugs fix",  # 包的简述
    long_description="support apply_multi which uses multi threadings to process files and fix the bugs for merge files",  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://github.com/SWEENEYHE/Data4LLM",  # 自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # 对python的最低版本要求
)