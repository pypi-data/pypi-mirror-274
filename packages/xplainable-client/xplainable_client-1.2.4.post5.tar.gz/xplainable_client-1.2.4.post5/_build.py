# import os
# import platform
# import argparse

# # CONFIG
# package_name = 'xplainable-client'

# # Load arguments
# parser = argparse.ArgumentParser()

# choices=['true', 'false']

# parser.add_argument(
#     "--install",
#     type=str,
#     default='false',
#     choices=choices,
#     help="Installs the whl file if true."
#     )

# parser.add_argument(
#     "--force",
#     type=str,
#     default='false',
#     choices=choices,
#     help="Forces a reinstall of the whl file and dependencies if true."
#     )

# args = parser.parse_args()
# install = args.install
# force = args.force

# # Load the latest version number
# # exec(open(f'{package_name}/_version.py').read())
# exec(open('_version.py').read())


# # Build Wheel
# os.system('python -m .\_build --wheel')

# # Install Wheel
# if install == 'true':

#     if force == "true":
#         os.system(f'pip uninstall {package_name}')

#     # Find the current whl version filepath
#     whl_prefix = f'{package_name}-{__version__}'
#     target_whl = ''
#     for file in os.listdir("dist"):
#         if file.startswith(whl_prefix):
#             target_whl = file

#     # Normal install
#     os.system(f'cd dist & pip install dist/{target_whl}')

# # Remove .egg-info file
# if platform.system() == 'Windows':
#     os.system(f'rmdir /s /q build target {package_name}.egg-info')

# else:
#     os.system(f'rm -r build target {package_name}.egg-info')

import os
import platform
import argparse
import sys

# Add the package directory to the system path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# CONFIG
package_name = 'xplainable_client'

# Load arguments
parser = argparse.ArgumentParser()

choices = ['true', 'false']

parser.add_argument(
    "--install",
    type=str,
    default='false',
    choices=choices,
    help="Installs the whl file if true."
)

parser.add_argument(
    "--force",
    type=str,
    default='false',
    choices=choices,
    help="Forces a reinstall of the whl file and dependencies if true."
)

parser.add_argument(
    "--wheel",
    action='store_true',
    help="Builds the wheel file."
)

args = parser.parse_args()
install = args.install
force = args.force
wheel = args.wheel

# Load the latest version number
exec(open('_version.py').read())

# Build Wheel
if wheel:
    result = os.system('python setup.py bdist_wheel')
    if result != 0:
        print("Error building the wheel.")
        sys.exit(result)

# Verify if the dist directory and wheel file were created
if not os.path.exists('dist'):
    print("Error: 'dist' directory not found. Wheel build failed.")
    sys.exit(1)

# Install Wheel
if install == 'true':
    if force == "true":
        os.system(f'pip uninstall -y {package_name}')

    # Find the current whl version filepath
    whl_prefix = f'{package_name.replace("_", "-")}-{__version__}'
    target_whl = ''
    for file in os.listdir("dist"):
        if file.startswith(whl_prefix):
            target_whl = file

    if not target_whl:
        print("Error: Wheel file not found.")
        sys.exit(1)

    # Normal install
    result = os.system(f'pip install dist/{target_whl}')
    if result != 0:
        print("Error installing the wheel.")
        sys.exit(result)

# Remove .egg-info file
if platform.system() == 'Windows':
    os.system(f'rmdir /s /q build dist {package_name}.egg-info')
else:
    os.system(f'rm -rf build dist {package_name}.egg-info')

