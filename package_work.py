# Project: PyPackageManager | package_work class
# Author : VolodyaHoi [7nation]


# import subprocess module for send pip commands in cmd or terminal

import subprocess


# init Package class

class Package:

    # set input type (pip, py -m pip, python -m pip, etc.)

    def __init__(self, type):
        self.input_type = type


    # get installed packages list | pip list

    def get_installed_packages(self):
        try:
            result = subprocess.run(self.input_type + " list", capture_output=True, text=True)
            if result.returncode != 0:
                return "ERROR"

            matrix = [line.split() for line in result.stdout.strip().split('\n')]

            for i in range(0, 2):
                del matrix[0]

            return matrix
        except:
            return "ERROR"
        

    # get packages list which can be upgraded | pip list --outdated

    def get_upgrade_packages(self):
        try:
            result = subprocess.run(self.input_type + " list --outdated", capture_output=True, text=True)
            if result.returncode != 0:
                return "ERROR"

            matrix = [line.split() for line in result.stdout.strip().split('\n')]

            for i in range(0, 2):
                del matrix[0]

            return matrix
        except:
            return "ERROR"
        

    # get information about package (author, version, etc) | pip show [package-name]

    def get_package_info(self, package):
        try:
            result = subprocess.run(self.input_type + " show " + package, capture_output=True, text=True)
            if result.returncode != 0:
                return "ERROR"

            matrix = [line.split(': ', 1) for line in result.stdout.strip().split('\n')]
            for i in range(0, len(matrix)):
                for j in range(0, len(matrix[0])):
                    try:
                        matrix[i][j]
                    except:
                        matrix[i].append("none")
            return matrix
        except:
            return "ERROR"
        

    # install package | pip install [package-name]

    def install_package(self, package):
        try:
            result = subprocess.run(self.input_type + " install " + package, capture_output=True, text=True)
            if result.returncode != 0:
                return "ERROR"
            return True
        except:
            return "ERROR"
        

    # uninstall package | pip uninstall -y [package-name]

    def uninstall_package(self, package):
        try:
            package_installed = False
            packages = self.get_installed_packages()
            for i in range(0, len(packages)):
                if packages[i][0] == package:
                    package_installed = True
                    break
                
            if package_installed == True:
                result = subprocess.run(self.input_type + " uninstall -y " + package, capture_output=True, text=True)
                if result.returncode != 0:
                    return "ERROR"

                return True
            else:
                return "ERROR"
        except:
            return "ERROR"
        

    # upgrade package | pip install --upgrade [package-name]

    def upgrade_package(self, package):
        try:
            result = subprocess.run(self.input_type + " install --upgrade " + package, capture_output=True, text=True)
            if result.returncode != 0:
                return "ERROR"

            return True
        except:
            return "ERROR"


    # download package`s .whl archive | pip download [package-name] -d [path]

    def download_package(self, package, directory):
        try:
            result = subprocess.run(self.input_type + " download " + package + " -d " + directory, capture_output=True, text=True)
            if result.returncode != 0:
                return "ERROR"

            return True
        except:
            return "ERROR"
