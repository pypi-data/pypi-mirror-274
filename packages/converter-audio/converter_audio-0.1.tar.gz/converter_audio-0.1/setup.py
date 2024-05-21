from setuptools import setup, find_packages

setup(
    name="converter_audio",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # 你的依赖包列表，例如：
        # "matplotlib >= 2.2.0"
    ],
)
