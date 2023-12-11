from modules.data_processing import adb_extract
from modules.data_processing import cache
from modules.data_processing import clipboard
from modules.data_processing import shared_prefs
from modules.data_processing import contacts
from modules.data_processing import adb_extract
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class viewData_Thread(QThread):
    progress_signal=pyqtSignal(int)
    result_signal=pyqtSignal()
    finished_signal=pyqtSignal()

    def __init__(self,android_version,modelname,wiping_aplication):
        super().__init__()
        self.android_version=android_version
        self.modelname=modelname
        self.wiping_application=wiping_aplication
    def run(self):
        signal=0
        device=adb_extract.get_device()
        destination_dir='/data'
        if self.android_version<11:
            clipboard_folder='clipboard' #destination_dir=data
        elif self.android_version==11:
            clipboard_folder='semclipboard'#destination_dir=data
        else:
            destination_dir='/data/data'
            clipboard_folder='com.samsung.android.honeyboard'
            clipboard_name='databases/ClipItem.db'

        if 'Pixel' in self.modelname:
            clipboard_folder='com.google.android.inputmethod.latin'
            clipboard_name='databases/gboard_clipboard.db'
            gallery_folder=''
        self.progress_signal.emit(signal)
        signal+=20
        adb_extract.extract_data(device,clipboard_folder,destination_dir)

        self.progress_signal.emit(signal)
        signal+=20
        #adb extract all data except clipboard data
        data_list=['com.sec.android.gallery3d','com.samsung.android.providers.contacts']
        data_list.extend(self.wiping_application)
        destination_dir='/data/data'
        for file_name in data_list:
            adb_extract.extract_data(device,file_name,destination_dir)
            self.progress_signal.emit(signal)
            signal+=10

        # application folder
        for package_name in self.wiping_application:
            shared_prefs.full_shared_prefs('extractdata',package_name)
            folder_destination_dir=f'./extractdata/{package_name}/cache/image_manager_disk_cache'
            folder_renamed_files_dir=f'./result/cache/{package_name}'
            cache.cache_image(folder_destination_dir,folder_renamed_files_dir)
        self.progress_signal.emit(signal)
        signal+=20
        #gallery cache
        gallery_destination_dir='./extractdata'
        gallery_renamed_files_dir='./result/gallery3d_cache'

        cache.cache_image(gallery_destination_dir,gallery_renamed_files_dir)
        self.progress_signal.emit(signal)
        signal+=10
        #clipboard
        if 'Pixel'not in self.modelname:
            if self.android_version<12:
                clipboard.clipboardFile_wiping('extractdata',clipboard_folder)
            else:
                clipboard.clipboardDB_wiping('extractdata',clipboard_folder,clipboard_name)

        #contacts
        contacts.contacts_wiping('extractdata','com.samsung.android.providers.contacts/databases/contacts2.db')
        self.progress_signal.emit(signal)
        signal+=10
        self.result_signal.emit()
        self.finished_signal.emit()