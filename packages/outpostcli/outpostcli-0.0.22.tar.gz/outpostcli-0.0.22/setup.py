from setuptools import setup

setup(
    name="outpostcli",
    version="0.0.22",
    py_modules=["outpostcli"],
    install_requires=["Click", "outpostkit"],
    entry_points={
        "console_scripts": [
            "outpostcli = outpostcli.cli:outpostcli",
        ],
    },
)
