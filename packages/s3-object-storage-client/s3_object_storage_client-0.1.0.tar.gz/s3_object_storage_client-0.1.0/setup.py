from setuptools import setup, find_packages

setup(
    name="s3_object_storage_client",
    version="0.1.0",
    keywords=["pip", "py_s3", "s3", "ceph", "minio"],
    description="s3 using tool",
    long_description="s3 protocol using tool",
    license="MIT Licence",
    url="https://github.com/susufqx/pyCeph",
    author="susufqx",
    author_email="jiangsulirui@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "aioboto3",
        "boto3",
        "urllib3",
    ]
)
