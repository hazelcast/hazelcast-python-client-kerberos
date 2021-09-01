from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="hazelcast-kerberos",
    version="1.0.0",
    packages=["hzkerberos"],
    url="https://github.com/hazelcast/hazelcast-python-client-kerberos",
    license="Apache 2.0",
    keywords="hazelcast,hazelcast client,in-memory data grid,distributed computing,kerberos,authentication",
    author="Hazelcast Inc. Developers",
    author_email="info@hazelcast.com",
    description="Kerberos Authentication Support for Hazelcast Python Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["gssapi"],
    tests_require=["hazelcast-python-client", "nose", "thrift"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
