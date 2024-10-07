from setuptools import setup
from glob import glob
import os

package_name = 'cam_calibration'
pkg = package_name

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', [f'resource/{pkg}']),
        (f'share/{pkg}/config', [f for f in glob(os.path.join('config', '*')) if os.path.isfile(f)]),
        (f'share/{pkg}/config/MicrosoftL2LifeCamHD3000', glob(os.path.join('config', 'MicrosoftL2LifeCamHD3000', '*'))),
        (f'share/{pkg}', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='james',
    maintainer_email='primordia@live.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
