# -*- coding: utf-8 -*-

"""
Copyright (C) 2010 Dariusz Suchojad <dsuch at gefira.pl>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from setuptools import setup, find_packages

version = "1.0.0"

setup(
    name="sec-wall-py3",
    version=version,
    scripts=["scripts/sec-wall"],
    author="Alejo Sarmiento",
    author_email="asarmiento@leafnoise.io",
    description="A feature packed security proxy",
    long_description="sec-wall is a feature packed security proxy supporting SSL/TLS, WS-Security, HTTP Auth Basic/Digest, extensible authentication schemes based on custom HTTP headers and XPath expressions, powerful URL matching/rewriting and an optional headers enrichment. It's a security wall you can conveniently fence the otherwise defenseless backend servers with.",
    platforms=["OS Independent"],
    license="GNU Lesser General Public License v3 (LGPLv3)",
    package_dir={"": "src"},
    packages=find_packages("src"),
    namespace_packages=["secwall"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Intended Audience :: Developers",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Topic :: System :: Networking :: Firewalls",
    ],
)
