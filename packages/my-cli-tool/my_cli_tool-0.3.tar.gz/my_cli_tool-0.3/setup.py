from setuptools import setup, find_packages
import os

# 确保 README.md 文件存在
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name="my_cli_tool",
    version="0.3",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mycli=my_cli_tool.cli:main",
        ],
    },
    install_requires=[
        # 在这里添加依赖项，例如 'requests',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple CLI tool to add two numbers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_cli_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
