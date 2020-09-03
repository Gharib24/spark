#!/usr/bin/python3
from distutils.core import setup

from spark.sparkothers import settings


setup(name = settings.APP_NAME.lower(),
	version = settings.APP_VERSION,
	description = settings.APP_DESCRIPTION,
	author = "AG",
	author_email = "ahmad2484@mail.com",
	url = "http://example.com",
	license='GPLv3',
	python_requires='>=3.6, <4',
	platforms=['linux'],
	scripts=['spark/spark'],
#	package_dir={'': 'src'},
	packages=[
		"spark",
		"spark.sparkhandlers",
		"spark.sparkothers",
		"spark.sparkviews",
	],
#	data_files = [("share/applications", ["data/spark.desktop"]),
#					("share/pixmaps", ["data/spark.png"])],
	data_files = [("share/applications", ["data/spark.desktop"]),],
)


