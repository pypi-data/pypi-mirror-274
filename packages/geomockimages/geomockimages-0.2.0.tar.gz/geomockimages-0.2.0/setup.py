# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geomockimages', 'geomockimages.test']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.26.4,<2.0.0',
 'rasterio>=1.3.10,<2.0.0',
 'rio-cogeo>=5.3.0,<6.0.0',
 'scikit-image>=0.23.2,<0.24.0',
 'scipy>=1.13.0,<2.0.0']

setup_kwargs = {
    'name': 'geomockimages',
    'version': '0.2.0',
    'description': 'A module to programmatically create geotiff images which can be used for unit tests.',
    'long_description': '# fake-geo-images\n\nA module to programmatically create geotiff images which can be used for unit tests.\n\n<p align="center">\n    <img src="./coverage.svg">\n</p>\n\nThe underlying idea is that in order to write unit tests for geospatial image processsing algorithms,\nit is necessary to have an actual input image file or array. Organising these test images becomes a chore over time,\nthey should not be stored in git as they are large binary data and when stored outside, there always\nis the danger that they are not updated according to changes in the code repo.\n\n**geomockimages** provides a solution to the problem by providing simple code that allows to create\ngeospatial images (so far geotiffs) in a parameterised way.\n\n## Install package\n```bash\npip install geomockimages\n```\n\n## Run tests\n```bash\npytest\n```\n\n## Usage\n\nIn the following an example unit test for a hypothetical NDVI function.\n\n```python\nimport numpy as np\nimport rasterio as rio\nfrom pathlib import Path\n\nfrom rasterio.transform import from_origin\nfrom my_image_processing import ndvi\nfrom fake_geo_images.fakegeoimages import FakeGeoImage\n\ndef test_ndvi():\n    """\n    A unit test if an NDVI method works in general\n    """\n    # Create 4-band image simulating RGBN as needed for NDVI\n    test_image, _ = FakeGeoImage(\n        300,\n        150,\n        4,\n        "uint16",\n        out_dir=Path("/tmp"),\n        crs=4326,\n        nodata=0,\n        nodata_fill=3,\n        cog=False,\n    ).create(seed=42, transform=from_origin(13.428596, 52.494384, 0.000006, 0.000006))\n\n    ndvi_image = ndvi(test_image)\n\n    with rio.open(str(ndvi_image)) as src:\n        ndvi_array = src.read()\n        # NDVI only has one band of same size as input bands\n        assert ndvi_array.shape == (1, 300, 150)\n        # NDVI has float values between -1 and 1\n        assert ndvi_array.dtype == np.float\n        assert ndvi_array.min >= -1\n        assert ndvi_array.max <= 1\n\n```\n',
    'author': 'Markus Müller',
    'author_email': 'markus.u.mueller@zoho.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
