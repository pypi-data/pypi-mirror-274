from setuptools import setup, find_packages

setup(
    name="latex_formatter",
    version="1.2.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ujson >= 5.8.0",
        # 你的依赖包列表，例如：
        # "matplotlib >= 2.2.0"
    ],
)
