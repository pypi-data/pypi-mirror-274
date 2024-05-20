from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = f.read()

setup(
    name = "flet_route_static",
    version = "0.0.1",
    author="Saurabh Wadekar, SmokyAce",
    packages=find_packages(),
    license="MIT",
    maintainer="SmokyAce",
    maintainer_email="smokyacetv@gmail.com",
    keywords=["flet","routing","flet_route_static","routes","flet app","flet-route","flet simple routing"],
    description="This makes it easy to manage multiple views with dynamic routing.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/saurabhwadekar/flet_route",
    include_package_data=True,
    install_requires=[
        # 'click==8.1.3',
        "repath",
        # "flet",
    ],
)
