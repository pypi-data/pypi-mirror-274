from setuptools import setup, find_packages

setup(
    name="pipy-test-xiaoqiang",
    version="1.1.2",
    packages=find_packages(),
    install_requires=[
        'click',  # 添加 click 作为依赖
    ],
    entry_points={
        'console_scripts': [
            'my_project_init=pipy_test_xiaoqiang.cli:init',  # 使用命令组前缀
        ],
    },
    author="Ma Xiaoqiang",
    author_email="851788096@qq.com",
    description="A short description of your project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/my_project",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)