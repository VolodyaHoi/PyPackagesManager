# PyPackagesManager

<img src="https://img.shields.io/badge/PyPackagesManager-0.1-violet"/> <img src="https://img.shields.io/badge/python-3.10+-blue"/> <img src="https://img.shields.io/badge/pip-24.0-green"/>

## About:

PyPackagesManager is program which allows you to work with python packages by calling pip.

### Functional:

- Install package
- Uninstall package
- Upgrade package
- Show information about package
- Show installed packages
- Donwload package`s .whl archive

### Requirements:

- dearpygui module
- configparser module
- pip
- python3
- package_work.py from repository
- settings.ini from repository
- favicon.ico from repository

> Testing was conducted on Windows 10 with pip 24.0 and Python 3.12.4

## Screenshots:

## Work principle:

Install function         - pip install <package-name>
Uninstall function       - pip uninstall <package-name>
Upgrade function         - pip install --upgrade <package-name>
Show information         - pip show <package-name>
Show installed packages  - pip list
Download package archive - pip download <package-name>

### package_work.py 

#### get_installed_packages()

Getting and return installed packages list

> pip list

#### get_upgrade_packages()

Getting and return packages list witch you can upgrade

> pip list --outdated

#### get_package_info(package)

Getting information about package. Return list with information

> pip show <package-name>

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `package` | `string` | package name                      |

#### install_package(package)

Installing package. Return True or "ERROR"

> pip install <package-name>

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `package` | `string` | package name                      |

#### uninstall_package(package)

Uninstalling package. Return True or "ERROR"

> pip uninstall <package-name>

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `package` | `string` | package name                      |

#### upgrade_package(package)

Upgrade package. Return True or "ERROR"

> pip install --upgrade <package-name>

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `package` | `string` | package name                      |

#### download_package(package, directory)

Donwloading package`s .whl archive in user directory. Return True or "ERROR"

> pip download <package-name> -d <directory>

| Parameter   | Type     | Description                       |
| :---------- | :------- | :-------------------------------- |
| `package`   | `string` | package name                      |
| `directory` | `string` | path to download                  |

## Install:

### Download requirements

```bash
pip install dearpygui
pip install configparser
```

### Start script

Download files from repository and run main.py
