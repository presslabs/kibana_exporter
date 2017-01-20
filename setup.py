from setuptools import setup, find_packages


setup(
    name="kibana_exporter",
    version="0.0.1",
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=["elasticsearch"],
    author="PressLabs SRL",
    author_email="contact@presslabs.com",
    url="https://github.com/presslabs/kibana_exporter",
    description="Backup ZFS snapshots to S3",
    entry_points={
        'console_scripts': [
            'kibana_export = kibana_exporter:main',
        ]
    },
    keywords='Elasticsearch Kibana',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Utilities",
    ],
)
