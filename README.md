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

<img src="https://sun9-77.userapi.com/impg/ro2dzUovg1qM5ju_rWM8sd978NRahugUdoaO2g/q2aPlnthUcQ.jpg?size=989x601&quality=95&sign=031a79997d1f6a3a6edc604ac84eac01&type=album"/>

> Main window with installed packages, information and uninstall function

&nbsp;

<img src="https://sun9-15.userapi.com/impg/RqDyq_9QJVNgVPl9McV5tGu8EawUlZLv4jqY-g/n_rr_H91Ak4.jpg?size=986x594&quality=95&sign=6c7a29925ee99f9d7561ab6065bd58f6&type=album"/>

> Package install window (install proccess)

&nbsp;

<img src="https://sun9-52.userapi.com/impg/alqkGwVrUZixx-zhftNhgjXa8-7BP-ik6l4OjQ/nPsupGH_o9c.jpg?size=987x599&quality=95&sign=09f71be966d6f2e076b4f2ae65c0bfdf&type=album"/>

> Packages install window (install from txt file)

&nbsp;

<img src="https://sun9-64.userapi.com/impg/mIZgeCqaO7ytL0eq8DBITSge2_vLXGp74NecFQ/z1NX0CE17-g.jpg?size=988x595&quality=95&sign=8c2ccc218e9f144e8f77e83c213d7d0d&type=album"/>

> Upgrade package proccess

&nbsp;

<img src="https://sun9-31.userapi.com/impg/n4h_asTDeV8LjAFoqiAqw-4OJQTapk1XZtt7xg/Z5_dHR0iAJo.jpg?size=984x591&quality=95&sign=c9720ae05bccdda1eb9b4a96a64ed80b&type=album"/>

> Download package window

&nbsp;

<img src="https://sun9-16.userapi.com/impg/OD-MDCbnwgs0jiOyP6k9DqaPPbZFi5_f2KQszg/phnE3EiYO_U.jpg?size=984x593&quality=95&sign=b36b916a6e1e468a5af19f8d48d16052&type=album"/>

> Settings window

## Work principle:

<pre>Install function         - pip install package-name

Uninstall function       - pip uninstall -y package-name

Upgrade function         - pip install --upgrade package-name

Show information         - pip show package-name

Show installed packages  - pip list

Download package archive - pip download package-name -d path </pre>

## package_work.py module

### get_installed_packages()

Getting and return installed packages list

> pip list

&nbsp;
### get_upgrade_packages()

Getting and return packages list witch you can upgrade

> pip list --outdated

&nbsp;
### get_package_info(package)

Getting information about package. Return list with information

> pip show <package-name>

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `package` | `string` | package name                      |

&nbsp;
### install_package(package)

Installing package. Return True or "ERROR"

> pip install <package-name>

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `package` | `string` | package name                      |

&nbsp;
### uninstall_package(package)

Uninstalling package. Return True or "ERROR"

> pip uninstall <package-name>

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `package` | `string` | package name                      |

&nbsp;
### upgrade_package(package)

Upgrade package. Return True or "ERROR"

> pip install --upgrade <package-name>

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `package` | `string` | package name                      |

&nbsp;
### download_package(package, directory)

Donwloading package`s .whl archive in user directory. Return True or "ERROR"

> pip download <package-name> -d <directory>

| Parameter   | Type     | Description                       |
| :---------- | :------- | :-------------------------------- |
| `package`   | `string` | package name                      |
| `directory` | `string` | path to download                  |

## Install:

### Install requirements

```bash
pip install dearpygui
pip install configparser
```

### Start script

Download files from repository and run main.py
