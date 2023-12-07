from modules.data_processing import adb_extract
from modules.data_processing import cache
from modules.data_processing import clipboard
from modules.data_processing import shared_prefs
from modules.data_processing import contacts
from modules.data_processing import usage
from modules.data_processing import mkdir
from modules.ui import view_usage
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import *
import os

def main():

    #adb extract usage
    device=adb_extract.get_device()
    android_version=int(adb_extract.get_androidVersion(device))
    modelname=adb_extract.get_modelname(device)
    mkdir.init()
    if android_version<11:
        destination_dir='/data/system/'
    else:
        destination_dir='/data/system_ce/0' 
    usage_name='usagestats'
    adb_extract.extract_data(device,usage_name,destination_dir)
    wiping_check,wiping_application=usage.usagestats(android_version)


    if wiping_check==True:
        print("wiping 흔적 없음")
        exit(0)
    else:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = view_usage.Usage_Window(android_version,modelname,wiping_application)
        ui.setupUi(MainWindow)
        MainWindow.show()
        app.exec_()
        # sys.exit(app.exec_())

        #adb extract clipboard data
        destination_dir='/data'
        if android_version<11:
            clipboard_folder='clipboard' #destination_dir=data
        elif android_version==11:
            clipboard_folder='semclipboard'#destination_dir=data
        else:
            destination_dir='/data/data'
            clipboard_folder='com.samsung.android.honeyboard'
            clipboard_name='databases/ClipItem.db'

        if 'Pixel' in modelname:
            clipboard_folder='com.google.android.inputmethod.latin'
            clipboard_name='databases/gboard_clipboard.db'
            gallery_folder=''
        adb_extract.extract_data(device,clipboard_folder,destination_dir)

        #adb extract all data except clipboard data
        data_list=['com.sec.android.gallery3d','com.samsung.android.providers.contacts']
        data_list.extend(wiping_application)
        destination_dir='/data/data'
        for file_name in data_list:
            adb_extract.extract_data(device,file_name,destination_dir)

        # application folder
        for package_name in wiping_application:
            shared_prefs.full_shared_prefs('extractdata',package_name)
            folder_destination_dir=f'./extractdata/{package_name}/cache/image_manager_disk_cache'
            folder_renamed_files_dir=f'./result/{package_name}'
            cache.cache_image(folder_destination_dir,folder_renamed_files_dir)

        #gallery cache
        gallery_destination_dir='./extractdata'
        gallery_renamed_files_dir='./result/gallery3d_cache'

        cache.cache_image(gallery_destination_dir,gallery_renamed_files_dir)

        #clipboard
        if 'Pixel'not in modelname:
            if android_version<11:
                clipboard.clipboardFile_wiping('extractdata',clipboard_folder)
            else:
                clipboard.clipboardDB_wiping('extractdata',clipboard_folder,clipboard_name)

        #contacts
        contacts.contacts_wiping('extractdata','com.samsung.android.providers.contacts/databases/contacts2.db')
        


if __name__=="__main__":
    main()