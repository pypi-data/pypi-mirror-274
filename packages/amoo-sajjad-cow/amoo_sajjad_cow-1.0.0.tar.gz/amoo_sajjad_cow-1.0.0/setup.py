from setuptools import setup


def pre_install():
    # f = open("readme.md", "r")
    # text = f.read()
    text = "#Amoo Sajjad Cow Package"
    return text


setup(
    name="amoo_sajjad_cow",
    version="1.0.0",
    author="Sajjad Aemmi",
    description="A test package for pydeploy students",
    long_description=pre_install(),
    requires=[],
    author_email="sajjadaemmi@gmail.com",
    packages=["amoo_sajjad_cow"]
)
