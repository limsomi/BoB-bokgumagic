import shutil
import os

def init():
    if os.path.exists('result'):
            shutil.rmtree('result')
    if os.path.exists('extractdata'):
        shutil.rmtree('extractdata')
    os.makedirs('result')
    os.makedirs('extractdata')
    os.makedirs('result/clipboard')
    os.makedirs('result/clipboard/image')
    os.makedirs('result/clipboard/html')