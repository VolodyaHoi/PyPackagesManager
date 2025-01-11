# Project: PyPackagesManager
# Author : VolodyaHoi [7nation]

# Comment tags
# [FUNCTION] - designation of the executed function
# [DPG]      - designation of dearpygui elements
# [LIBS]     - designation of lib
# [OTHER]    - esignation of comments that are not included in the above-listed tags

# Configuration file description:
# hello_window | true - you will watch welcome window. false - no
# type         | input type (py -m pip, pip, python -m pip, etc)
# custom_type  | true - you can set your input type. false - you can choose default type 

# [LIBS] import libs

import dearpygui.dearpygui as dpg
import os
import configparser
from package_work import Package


# [OTHER] read configuration file

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
input_type = config['config']['type']
custom_type = config['config']['custom_type']

if custom_type == "true":
    cb_custom_type = True
else:
    cb_custom_type = False


# [LIBS] init package_work module for work with pip

pkg = Package(input_type)


# [OTHER] calculate positions for windows

download_window_pos_x = 1000 / 2 - 230 / 2 
download_window_pos_y = 600 / 2 - 100 / 2

welcome_window_pos_x = 1000 / 2 - 450 / 2
welcome_window_pos_y = 600 / 2 - 110 / 2

upgrade_window_pox_x = 1000 / 2 - 500 / 2
upgrade_window_pox_y = 600 / 2 - 300 / 2

install_window_pos_x = 1000 / 2 - 300 / 2
install_window_pos_y = 600 / 2 - 100 / 2

settings_window_pos_x = 1000 / 2 - 350 / 2
settings_window_pos_y = 600 / 2 - 140 / 2

error_window_pos_x = 1000 / 2 - 550 / 2
error_window_pos_y = 600 / 2 - 70 / 2

installtxt_window_pos_x = 1000 / 2 - 190 / 2
installtxt_window_pos_y = 600 / 2 - 25 / 2

help_window_pos_x = 1000 / 2 - 580 / 2
help_window_pos_y = 600 / 2 - 200 / 2


# [OTHER] init global values

global current_package, installed_packages
current_package = ""


# [DPG] create context dpg

dpg.create_context()


# [FUNCTION] opening info about package

def openInfo(user_data):
    global current_package
    dpg.delete_item(item="content_table")
    dpg.add_loading_indicator(radius=3, parent="content", tag="loading_indicator")
    dpg.configure_item(item="current_pkg", show=False)
    dpg.configure_item("btn_current_pkg", show=False)
    package = dpg.get_item_label(item=user_data)
    dpg.set_value(item=user_data, value=False)
    info = pkg.get_package_info(package)
    dpg.add_table(parent="content",policy=dpg.mvTable_SizingFixedFit, scrollX=False, borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, header_row=True, tag="content_table")
    dpg.add_table_column(label="Section", parent="content_table")
    dpg.add_table_column(label="Content", parent="content_table")
    if info != "ERROR":
        for line in info:
            with dpg.table_row(parent="content_table"):
                dpg.add_text(line[0])
                if line[1] == "":
                    dpg.add_text("none")
                else:
                    dpg.add_text(line[1])
        current_package = info[0][1]

        dpg.configure_item(item="current_pkg", show=True)
        dpg.set_value("current_pkg", " | current package: " + current_package)
        dpg.configure_item("btn_current_pkg", show=True)
    else:
        dpg.configure_item(item="error_window", show=True)
        dpg.set_value("error_message", "An unexpected error occurred when receiving information about the package")
    dpg.delete_item(item="loading_indicator")
    dpg.configure_item(item="content_table", scrollX=True)


# [FUNCTION] init "welcome" window

def startProgram():
    dpg.configure_item(item="main_window", show=True)
    dpg.configure_item(item="welcome_window", show=False)

    welcome_window = dpg.get_value(item="dsma_window")
    if welcome_window == True:
        config['config']['hello_window'] = "false"

        with open(config_path, 'w') as configfile:
            config.write(configfile)


# [FUNCTION] init installed packages list and create table

def initPackagesList():
    global installed_packages
    list = pkg.get_installed_packages()
    packages_count = 0
    if list != "ERROR":
        installed_packages = list
        for line in list:
            with dpg.table_row(parent="main_table"):
                dpg.add_selectable(label=line[0], callback=openInfo, span_columns=True)
                dpg.add_selectable(label=line[1], callback=openInfo, span_columns=True)
            packages_count+=1
        dpg.set_value("installed_pkg_count_main", "Installed packages: " + str(packages_count))
    else:
        dpg.configure_item(item="error_window", show=True)
        dpg.set_value("error_message", "An unexpected error occurred while receiving the installed packages")


# [FUNCTION] uninstall selected package

def uninstallCurrentPackage():
    global current_package
    dpg.set_value("current_pkg", " | uninstalling " + current_package + " ..")
    dpg.configure_item("btn_current_pkg", show=False)
    dpg.delete_item("content_table")
    dpg.add_table(parent="content", scrollX=False, borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, header_row=True, tag="content_table")
    dpg.add_table_column(label="Section", parent="content_table")
    dpg.add_table_column(label="Content", parent="content_table")
    dpg.add_loading_indicator(radius=1.5, parent="status_bar", tag="loading_indicatornum2")
    result = pkg.uninstall_package(current_package)
    if result != "ERROR":
        dpg.configure_item(item="current_pkg", show=True)
        dpg.set_value("current_pkg", " | " + current_package + " uninstalled!")
        dpg.delete_item(item="loading_indicatornum2")
        updateData()
    else:
        dpg.configure_item(item="error_window", show=True)
        dpg.set_value("error_message", "An unexpected error occurred when deleting the " + current_package + " package")


# [FUNCTION] install package 

def installPackage():
    global installed_packages
    need_install = True
    package = dpg.get_value("pkg_name")
    dpg.configure_item(item="status_group", show=True)
    dpg.configure_item(item="status_indicator", show=True)
    dpg.set_value("status", "Installing " + package + " ..")
    dpg.configure_item(item="install_btn", enabled=False)
    dpg.configure_item(item="install_window", no_close=True)
    for i in range(0, len(installed_packages)):
        if installed_packages[i][0] == package:
            closeInstallWindow()
            dpg.configure_item(item="error_window", show=True)
            dpg.set_value("error_message", package + " already installed!")
            need_install = False
            break
    if need_install == True:
        result = pkg.install_package(package)
        if result != "ERROR":
            dpg.set_value("status", package + " installed! Updating data..")
            dpg.configure_item(item="status_indicator", show=False)
            dpg.set_value(item="pkg_name", value="")
            dpg.configure_item(item="install_btn", enabled=True)
            updateData()
            dpg.set_value("status", package + " installed!")
            dpg.configure_item(item="install_window", no_close=False)
        else:
            closeInstallWindow()
            dpg.configure_item(item="error_window", show=True)
            dpg.set_value("error_message", "An unexpected error occurred when installing the " + package + " package")


# [FUNCTION] update installed packages list and table

def updateData():
    dpg.delete_item("main_table")
    dpg.delete_item("content_table")
    dpg.add_table(parent="main_table_child", borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, header_row=True, tag="main_table")
    dpg.add_table_column(label="Package", parent="main_table")
    dpg.add_table_column(label="Version", parent="main_table")
    dpg.add_loading_indicator(radius=3, parent="main_table_child", tag="loading_indicatornum3")
    dpg.configure_item("btn_current_pkg", show=False)
    dpg.configure_item("current_pkg", show=False)
    dpg.add_table(parent="content", scrollX=False, borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, header_row=True, tag="content_table")
    dpg.add_table_column(label="Section", parent="content_table")
    dpg.add_table_column(label="Content", parent="content_table")
    initPackagesList()
    dpg.delete_item("loading_indicatornum3")


# [FUNCTION] configuration install window when its closing

def closeInstallWindow():
    dpg.configure_item(item="status_group", show=False)
    dpg.configure_item(item="status_indicator", show=False)
    dpg.set_value(item="pkg_name", value="")
    dpg.configure_item(item="install_btn", enabled=True)
    dpg.configure_item(item="install_window", show=False, no_close=False)


# [FUNCTION] init packages list for install
    
def openPackagesList(sender, app_data):
    global packages
    file_path = app_data['file_path_name']
    count_pkg = 0
    packages = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                count_pkg+=1
                packages.append(line.strip())
        dpg.configure_item(item="installtxt_window", width=500, height=300, pos=(1000 / 2 - 500 / 2, 600 / 2 - 300 / 2))
        dpg.set_value("choosed_file", "Choosed file -> " + file_path)
        dpg.configure_item(item="choose_btn", show=False)
        dpg.configure_item(item="choosed_file", show=True)
        dpg.configure_item(item="info_pkg", show=True)
        dpg.configure_item(item="pkg_listbox", show=True)
        dpg.configure_item(item="installtxt_packages", num_items=count_pkg, items=packages)
        dpg.configure_item(item="delete_btn", show=True)
        dpg.configure_item(item="installtxt_btn", show=True)
    except:
        dpg.configure_item(item="error_window", show=True)
        dpg.set_value("error_message", "An unexpected error occurred when opening packages list")


# [FUNCTION] configuration install (from list) window

def closeInstalltxtWindow():
    dpg.configure_item(item="installtxt_window", width=190, height=70, pos=(1000 / 2 - 190 / 2, 600 / 2 - 25 / 2), show=False)
    dpg.configure_item(item="choose_btn", show=True)
    dpg.configure_item(item="choosed_file", show=False)
    dpg.configure_item(item="info_pkg", show=False)
    dpg.configure_item(item="pkg_listbox", show=False)
    dpg.configure_item(item="installtxt_packages", num_items=2, items=["package1", "package2"])
    dpg.configure_item(item="delete_btn", show=False)
    dpg.configure_item(item="installtxt_btn", show=False)
    dpg.configure_item(item="reset_btn", show=False)
    dpg.configure_item(item="installtxt_status", show=False)


# [FUNCTION] reset install (from list) window

def resetInstalltxtWindow():
    dpg.configure_item(item="installtxt_window", width=190, height=70, pos=(1000 / 2 - 190 / 2, 600 / 2 - 25 / 2), show=True)
    dpg.configure_item(item="choose_btn", show=True)
    dpg.configure_item(item="choosed_file", show=False)
    dpg.configure_item(item="info_pkg", show=False)
    dpg.configure_item(item="pkg_listbox", show=False)
    dpg.configure_item(item="installtxt_packages", num_items=2, items=["package1", "package2"])
    dpg.configure_item(item="delete_btn", show=False)
    dpg.configure_item(item="installtxt_btn", show=False)
    dpg.configure_item(item="reset_btn", show=False)
    dpg.configure_item(item="installtxt_status", show=False)


# [FUNCTION] delete selected package from list

def deleteSelectedPackage():
    global packages
    del_pkg = dpg.get_value("installtxt_packages")
    packages.remove(del_pkg)
    dpg.configure_item(item="installtxt_packages", items=packages, num_items=len(packages))
    if packages == []:
        closeInstalltxtWindow()
        dpg.configure_item(item="installtxt_window", show=True)


# [FUNCTION] install packages from list

def installPackagesFromTxt():
    global packages, installed_packages
    installed = 0
    not_installed = 0
    dpg.configure_item(item="delete_btn", show=False)
    dpg.configure_item(item="installtxt_window", no_close=True)
    dpg.configure_item(item="installtxt_group", show=True)
    dpg.configure_item(item="installtxt_status", show=True)
    dpg.configure_item(item="loading_installtxt", show=True)
    dpg.configure_item(item="installtxt_btn", show=False)
    for i in range(0, len(packages)):
        already_installed = False
        dpg.set_value("installtxt_status", "installing " + packages[i] + " ..")
        for j in range(0, len(installed_packages)):
            if packages[i] == installed_packages[j][0]:
                already_installed = True
                packages[i] = packages[i] + "......already installed"
                installed+=1

        if already_installed != True:
            result = pkg.install_package(packages[i])
            if result != "ERROR":   
                packages[i] = packages[i] + "......installed"
                installed+=1
            else:
                packages[i] = packages[i] + "......not installed (error)"
                not_installed+=1
        dpg.configure_item(item="installtxt_packages", num_items=len(packages), items=packages)
    dpg.set_value("installtxt_status", "Installed packages: " + str(installed) + ". Not installed: " + str(not_installed) + ". Updating data..")
    updateData()
    dpg.set_value("installtxt_status", "Installed packages: " + str(installed) + ". Not installed: " + str(not_installed) + ".")
    dpg.configure_item(item="loading_installtxt", show=False)
    dpg.configure_item(item="installtxt_window", no_close=False)
    dpg.configure_item(item="reset_btn", show=True)


# [FUNCTION] select folder/directory for download package`s .whl archive

def selectDirForDownload(sender, app_data):
    global path_to_folder

    path_to_folder = app_data['file_path_name']
    dpg.set_value("dir_for_download", "Path to download -> " + path_to_folder)
    dpg.configure_item(item="dir_for_download", show=True)
    dpg.configure_item(item="btn_choose_dir", show=False)
    dpg.configure_item(item="pkg_download", show=True)
    dpg.configure_item(item="btn_download", show=True)
    dpg.configure_item(item="download_window", width=450, pos=(1000 / 2 - 450 / 2, 600 / 2 - 100 / 2))


# [FUNCTION] download package
    
def downloadPackage():
    global path_to_folder
    dpg.configure_item(item="download_status", show=True)
    dpg.configure_item(item="indicator_download", show=True)
    dpg.configure_item(item="btn_download", enabled=False)
    dpg.configure_item(item="download_window", no_close=True)
    package = dpg.get_value("pkg_download")
    dpg.set_value("download_status", "Downloading " + package + " ..")
    try:
        result = pkg.download_package(package, path_to_folder)
        if result != "ERROR":
            dpg.set_value("download_status", package + " downloaded!")
            resetDownloadWindow()
        else:
            resetDownloadWindow()
            dpg.configure_item(item="error_window", show=True)
            dpg.set_value("error_message", "An unexpected error occurred when downloading " + package + " package")
    except:
        resetDownloadWindow()
        dpg.configure_item(item="error_window", show=True)
        dpg.set_value("error_message", "An unexpected error occurred when downloading " + package + " package")


# [FUNCTION] reset download window

def resetDownloadWindow():
    dpg.configure_item(item="btn_choose_dir", show=True)
    dpg.configure_item(item="dir_for_download", show=False)
    dpg.configure_item(item="btn_download", enabled=True)
    dpg.configure_item(item="indicator_download", show=False)
    dpg.configure_item(item="download_window", no_close=False)
    dpg.configure_item(item="pkg_download", show=False)
    dpg.configure_item(item="btn_download", show=False)
    dpg.configure_item(item="download_window", width=230, pos=(1000 / 2 - 230 / 2, 600 / 2 - 100 / 2))


# [FUNCTION] configuration download window when its closing

def closeDownloadWindow():
    dpg.configure_item(item="btn_choose_dir", show=True)
    dpg.configure_item(item="dir_for_download", show=False)
    dpg.configure_item(item="btn_download", enabled=True)
    dpg.configure_item(item="download_status", show=False)
    dpg.configure_item(item="indicator_download", show=False)
    dpg.configure_item(item="pkg_download", show=False)
    dpg.configure_item(item="btn_download", show=False)
    dpg.configure_item(item="download_window", width=230, pos=(1000 / 2 - 230 / 2, 600 / 2 - 100 / 2))


# [FUNCTION] get not updated packages list and configure upgrade window

def getNotUpdatedPackages():
    global upgrade_packages
    upgrade_packages = []
    dpg.configure_item(item="update_btn", enabled=False)
    dpg.configure_item(item="update_indicator", show=True)
    dpg.configure_item(item="upgrade_listbox", show=False)
    dpg.configure_item(item="delete_upg_btn", show=False)
    dpg.configure_item(item="upgrade_pkg_btn", show=False)
    dpg.configure_item(item="upgrade_window", no_close=True, height=250)
    dpg.set_value("upgrade_count", "Updating..")
    dpg.configure_item(item="upgrade_status", show=False)
    packages_upg = pkg.get_upgrade_packages()
    if packages_upg != "ERROR":
        count = len(packages_upg)
        dpg.configure_item(item="upgrade_window", height=300)
        for i in range(0, len(packages_upg)):
            if packages_upg[i][0] != "pip":
                array = packages_upg[i][0] + " " + packages_upg[i][1] + "->" + packages_upg[i][2]
                upgrade_packages.append(array)
            else:
                count-=1

        dpg.set_value("upgrade_count", "Not updated packages: " + str(count))
        if count == 0:
            dpg.configure_item(item="upgrade_listbox", items=["Nothing to upgrade"], num_items=1, show=True)
            dpg.configure_item(item="delete_upg_btn", show=False)
            dpg.configure_item(item="upgrade_pkg_btn", show=False)
            dpg.configure_item(item="upgrade_window", height=250, no_close=False)
        else:
            dpg.configure_item(item="upgrade_listbox", items=upgrade_packages, num_items=count, show=True)
            dpg.configure_item(item="delete_upg_btn", show=True)
            dpg.configure_item(item="upgrade_pkg_btn", show=True)
            dpg.configure_item(item="upgrade_window", height=300, no_close=False)
        dpg.configure_item(item="update_btn", enabled=True)
        dpg.configure_item(item="update_indicator", show=False)
    else:
        dpg.configure_item(item="update_btn", enabled=True)
        dpg.configure_item(item="update_indicator", show=False)
        dpg.configure_item(item="delete_upg_btn", show=True)
        dpg.configure_item(item="upgrade_pkg_btn", show=True)
        dpg.configure_item(item="upgrade_window", show=False, no_close=False)
        dpg.configure_item(item="error_window", show=True)
        dpg.set_value("error_message", "An unexpected error occurred while receiving the upgrading packages")


# [FUNCTION] delete selected package from upgrade list

def deleteUpgradePackage():
    package = dpg.get_value("upgrade_listbox")
    upgrade_packages.remove(package)
    dpg.configure_item(item="upgrade_listbox", items=upgrade_packages, num_items=len(upgrade_packages))
    dpg.set_value("upgrade_count", "Not updated packages: " + str(len(upgrade_packages)))
    
    if upgrade_packages == []:
        dpg.configure_item(item="upgrade_listbox", items=["empty"], num_items=1)
        dpg.configure_item(item="delete_upg_btn", show=False)
        dpg.configure_item(item="upgrade_pkg_btn", show=False)
        dpg.configure_item(item="upgrade_window", height=250)

    
# [FUNCTION] upgrade packages

def upgradePackages():
    upgraded_packages = 0
    not_upgraded_packages = 0

    dpg.configure_item(item="upgrade_window", no_close=True)
    dpg.configure_item(item="update_btn", enabled=False)
    dpg.configure_item(item="delete_upg_btn", show=False)
    dpg.configure_item(item="upgrade_pkg_btn", show=False)
    dpg.set_value("upgrade_count", "Upgrading packages..")
    dpg.configure_item(item="upgrade_status", show=True)
    dpg.configure_item(item="indicator_upgrade", show=True)

    for i in range(0, len(upgrade_packages)):
        package = upgrade_packages[i].split(" ")[0]
        dpg.set_value("upgrade_status", "Upgrading " + package + "..")
        result = pkg.upgrade_package(package)
        if result != "ERROR":
            upgraded_packages+=1
            upgrade_packages[i] = package + "......upgraded"
        else:
            not_upgraded_packages+=1
            upgrade_packages[i] = package + "......not upgraded (error)"
        dpg.configure_item(item="upgrade_listbox", items=upgrade_packages, num_items=len(upgrade_packages))
        
    dpg.configure_item(item="indicator_upgrade", show=False)
    dpg.set_value("upgrade_status", "Packages upgraded. Upgraded: " + str(upgraded_packages) + " Not upgraded: " + str(not_upgraded_packages))
    dpg.set_value("upgrade_count", "Upgraded!")
    dpg.configure_item(item="update_btn", enabled=True)
    dpg.configure_item(item="upgrade_window", no_close=False)


# [FUNCTION] set settings configuration

def cbCustomInputType():
    cb_custom_type = dpg.get_value("cb_type")
    if cb_custom_type == True:
        dpg.configure_item(item="install_type_cb", enabled=False)
        dpg.configure_item(item="tb_custom_type", enabled=True)
        dpg.set_value(item="install_type_cb", value="*custom*")
    else:
        dpg.configure_item(item="install_type_cb", enabled=True)
        dpg.configure_item(item="tb_custom_type", enabled=False)
        dpg.set_value(item="install_type_cb", value="pip")
        dpg.set_value(item="tb_custom_type", value="")


# [FUNCTION] apply settings configuration

def btnCustomInputType():
    global pkg
    cb_custom_type = dpg.get_value("cb_type")
    if cb_custom_type == True:
        config['config']['type'] = dpg.get_value("tb_custom_type")
        config['config']['custom_type'] = "true"
        input_type = dpg.get_value("tb_custom_type")
        pkg = Package(input_type)
    else:
        config['config']['type'] = dpg.get_value("install_type_cb")
        config['config']['custom_type'] = "false"
        input_type = dpg.get_value("install_type_cb")
        pkg = Package(input_type)

    with open(config_path, 'w') as configfile:
        config.write(configfile)

    dpg.configure_item(item="settings_msg", show=True)


# [FUNCTION] set settings when program started

def setSettings():
    if cb_custom_type == True:
        dpg.configure_item(item="install_type_cb", enabled=False)
        dpg.configure_item(item="tb_custom_type", enabled=True)
        dpg.set_value(item="install_type_cb", value="*custom*")
    else:
        dpg.configure_item(item="install_type_cb", enabled=True)
        dpg.configure_item(item="tb_custom_type", enabled=False)
        dpg.set_value(item="install_type_cb", value="pip")
        dpg.set_value(item="tb_custom_type", value="")


# [DPG] dialog windows for pick folder/txt file

with dpg.file_dialog(directory_selector=False, show=False, callback=openPackagesList, tag="file_dialog", width=500 ,height=400):
    dpg.add_file_extension(".txt", color=(255, 0, 255, 255))

dpg.add_file_dialog(directory_selector=True, show=False, callback=selectDirForDownload, tag="dir_dialog", width=500 ,height=400)


# [DPG] main window setup

with dpg.window(label="Main window", tag="main_window", show=False, no_resize=True):
    with dpg.menu_bar(tag="menu_bar"):
        with dpg.menu(label="Operations"):
            dpg.add_menu_item(label="Update data", callback=updateData)
            with dpg.menu(label="Packages"):
                dpg.add_menu_item(label="Install packages", callback=lambda: dpg.configure_item(item="install_window", show=True))
                dpg.add_menu_item(label="Install from txt file", callback=lambda: dpg.configure_item(item="installtxt_window", show=True))
                dpg.add_menu_item(label="Upgrade", callback=lambda: dpg.configure_item(item="upgrade_window", show=True))
                dpg.add_menu_item(label="Download", callback=lambda: dpg.configure_item(item="download_window", show=True))
        with dpg.menu(label="Settings"):
            dpg.add_menu_item(label="Edit", callback=lambda: dpg.configure_item(item="settings_window", show=True))
        dpg.add_menu_item(label="Help", callback=lambda: dpg.configure_item(item="help_window", show=True))
    with dpg.group(horizontal=True, tag="status_bar"):
        dpg.add_text("Installed packages: n", tag="installed_pkg_count_main")
        dpg.add_text(" | current package: package-name", show=False, tag="current_pkg")
        dpg.add_button(label="Uninstall", show=False, tag="btn_current_pkg", callback=uninstallCurrentPackage)
    dpg.add_separator()
    with dpg.group(horizontal=True):
        with dpg.child_window(height=499, width=600, tag="main_table_child"):
            with dpg.table(borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, header_row=True, tag="main_table"):
                dpg.add_table_column(label="Package")
                dpg.add_table_column(label="Version")

        with dpg.child_window(height=499,tag="content"):
            with dpg.table(borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, header_row=True, tag="content_table"):
                dpg.add_table_column(label="Section")
                dpg.add_table_column(label="Content")


# [DPG] help window setup

with dpg.window(label="Help", tag="help_window", show=False, no_collapse=True, no_move=True, no_resize=True, width=580, height=200, pos=(help_window_pos_x, help_window_pos_y)):
    dpg.add_text('''                        Welcome to PyPackagesManager!
                 
With this program, you can interact with python packages using the pip tool.
                 
The program provides opportunities to view installed packages, their information,
install and remove packages, update and download them .whl archives.
                 
You can configure the installation method using settings or settings.ini.



Author: VolodyaHoi [7nation]
''')


# [DPG] settings window setup

with dpg.window(label="Settings", tag="settings_window", on_close=lambda: dpg.configure_item(item="settings_msg", show=False), show=False, no_collapse=True, no_move=True, no_resize=True, width=350, height=140, pos=(settings_window_pos_x, settings_window_pos_y)):
    dpg.add_combo(label="Install type", items=["pip", "py -m pip", "python -m pip", "py3 -m pip", "python3 -m pip"], default_value=input_type, tag="install_type_cb")
    dpg.add_checkbox(label="Custom install type", default_value=cb_custom_type, tag="cb_type", callback=cbCustomInputType)
    dpg.add_input_text(label="Enter type", hint=input_type, tag="tb_custom_type")
    dpg.add_separator()
    with dpg.group(horizontal=True):
        dpg.add_button(label="Confirm", callback=btnCustomInputType)
        dpg.add_text("Settings confirmed!", tag="settings_msg", show=False)


# [DPG] install window setup
    
with dpg.window(label="Install package", on_close=closeInstallWindow, no_close=False, tag="install_window", show=False, no_move=True, no_collapse=True, no_resize=True, width=300, height=100, pos=(install_window_pos_x, install_window_pos_y)):
    with dpg.group(horizontal=True):
        dpg.add_input_text(hint="package name", tag="pkg_name")
        dpg.add_button(label="Install", callback=installPackage, tag="install_btn")
    with dpg.group(horizontal=True, show=False, tag="status_group"):
        dpg.add_text("status..", tag="status")
        dpg.add_loading_indicator(tag="status_indicator", radius=1.5)


# [DPG] install (from list) window setup

with dpg.window(label="Install packages", no_close=False, on_close=closeInstalltxtWindow, tag="installtxt_window", show=False, no_move=True, no_collapse=True, no_resize=True, width=190, height=25, pos=(installtxt_window_pos_x, installtxt_window_pos_y)):
    with dpg.group(horizontal=True, show=True):    
        dpg.add_button(tag="choose_btn", label="Choose requarements.txt", callback=lambda: dpg.configure_item(item="file_dialog", show=True))
        dpg.add_text("Choosed file -> path/requarements.txt", tag="choosed_file", show=False)
    dpg.add_text("Next packages will be installed:", tag="info_pkg", show=False)
    with dpg.child_window(width=485, height=170, tag="pkg_listbox", show=False):
        dpg.add_listbox(num_items=2, width=470, items=["package1", "package2"], tag="installtxt_packages")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Delete selected package", callback=deleteSelectedPackage, tag="delete_btn", show=False)
        dpg.add_button(label="Install", tag="installtxt_btn", show=False, callback=installPackagesFromTxt)
        dpg.add_button(label="Reset window", show=False, tag="reset_btn", callback=resetInstalltxtWindow)
    with dpg.group(horizontal=True, show=False, tag="installtxt_group"):
        dpg.add_text("status", tag="installtxt_status")
        dpg.add_loading_indicator(radius=1.5, tag="loading_installtxt")
    

# [DPG] upgrade window setup

with dpg.window(label="Upgrade packages", tag="upgrade_window", no_close=False, show=False, no_collapse=True, no_resize=True, no_move=True, width=500, height=300, pos=(upgrade_window_pox_x, upgrade_window_pox_y)):
    with dpg.group(horizontal=True):
        dpg.add_text("Not updated packages: n", tag="upgrade_count")
        dpg.add_button(label="Update list", tag="update_btn", callback=getNotUpdatedPackages)
    with dpg.child_window(width=485, height=170, show=True):
        dpg.add_loading_indicator(tag="update_indicator", show=False)
        dpg.add_listbox(width=470, items=["package1", "package2"], num_items=2, tag="upgrade_listbox")
    with dpg.group(horizontal=True):
        dpg.add_button(label="Delete selected package", tag="delete_upg_btn", callback=deleteUpgradePackage)
        dpg.add_button(label="Upgrade packages", tag="upgrade_pkg_btn", callback=upgradePackages)
    with dpg.group(horizontal=True):
        dpg.add_text("status", tag="upgrade_status", show=False)
        dpg.add_loading_indicator(radius=1.5, tag="indicator_upgrade", show=False)
        

# [DPG] welcome window setup

with dpg.window(label="Welcome to PyPackagesManager!", tag="welcome_window", no_collapse=True, no_close=True, no_resize=True ,no_move=True, width=450, height=110, pos=(welcome_window_pos_x, welcome_window_pos_y)):
    dpg.add_text("This program help you working with python packages using pip")
    dpg.add_checkbox(label="Dont show me again", default_value=False, tag="dsma_window")
    dpg.add_separator()
    dpg.add_button(label="Start", callback=startProgram)


# [DPG] download window setup

with dpg.window(label="Download package", tag="download_window", no_close=False, on_close=closeDownloadWindow, show=False, no_move=True, no_collapse=True, width=230, height=100, no_resize=True, pos=(download_window_pos_x, download_window_pos_y)):
    dpg.add_button(label="Choose directory for download", callback=lambda: dpg.configure_item(item="dir_dialog", show=True), tag="btn_choose_dir", show=True)
    dpg.add_text("Path to download -> path/download", tag="dir_for_download", show=False)
    with dpg.group(horizontal=True):
        dpg.add_input_text(hint="package name..", tag="pkg_download", show=False)
        dpg.add_button(label="Download", tag="btn_download", callback=downloadPackage, show=False)
    with dpg.group(horizontal=True):
        dpg.add_text("status", tag="download_status", show=False)
        dpg.add_loading_indicator(radius=1.5, tag="indicator_download", show=False)


# [DPG] error window setup

with dpg.window(label="Error!", tag="error_window", show=False, no_move=True, no_collapse=True, no_resize=True, width=550, height=70, pos=(error_window_pos_x, error_window_pos_y)):
    dpg.add_text("error", tag="error_message")


# [OTHER] init welcome window

hello_window = config['config']['hello_window']
if hello_window == "true":
    dpg.configure_item(item="welcome_window", show=True)
elif hello_window == "false":
    dpg.configure_item(item="welcome_window", show=False)
    dpg.configure_item(item="main_window", show=True)


# [OTHER] init packages lists and settings

initPackagesList()
getNotUpdatedPackages()
setSettings()


# [DPG] dearpygui render start

dpg.create_viewport(title='PyPackagesManager', large_icon=script_dir+"/favicon.ico", small_icon=script_dir+"/favicon.ico", width=1000, height=600, resizable=False, max_height=600, max_width=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()
