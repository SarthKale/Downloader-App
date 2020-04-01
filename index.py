import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import urllib.request
import pafy
import humanize

ui, _ = loadUiType('main.ui')


class Main(QMainWindow, ui):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.initUi()
        self.handleButton()

    def initUi(self):
        '''Contains all UI chnges in loading'''
        print("UI Initiated")
        self.vrem.setText("")
        self.prem.setText("")
        self.tabWidget.tabBar().setVisible(False)
        self.moveGBox1()
        self.moveGBox2()
        self.moveGBox3()
        self.moveGBox4()

    def handleButton(self):
        '''Maintains the Functionalities of the Butttons'''
        print("Button Clicked")
        # For Solo Download
        self.downloadButton_t1.clicked.connect(self.download)
        self.browseButton_t1.clicked.connect(self.handleBrowse)

        # For Video Download
        self.dataButton.clicked.connect(self.get_VideoData)
        self.vbrowseButton_t2.clicked.connect(self.videoBrowse)
        self.vdownloadButton_t2.clicked.connect(self.downloadVideo)

        # For Playlist Download
        self.pbrowseButton_t2.clicked.connect(self.playlistBrowse)
        self.pdownloadButton_t2.clicked.connect(self.downloadPlaylist)

        # For Traversing between Pages
        self.homeButton.clicked.connect(self.pageHome)
        self.downloadButton.clicked.connect(self.pageDownload)
        self.ytButton.clicked.connect(self.pageYoutube)
        self.setButton.clicked.connect(self.pageSettings)

        # For Changing Themes
        self.darkOrangeB.clicked.connect(self.themeDarkOrange)
        self.DarkB.clicked.connect(self.themeDark)
        self.darkBlueB.clicked.connect(self.themeDarkBlue)
        self.darkGrayB.clicked.connect(self.themeDarkGray)

        # For Page Call
        self.fileDownload.clicked.connect(self.pageCall1)
        self.videoDownload.clicked.connect(self.pageCall2)
        self.playlistDownload.clicked.connect(self.pageCall3)
        self.setChanges.clicked.connect(self.pageCall4)

    def handleProgress(self, blocknum, blocksize, totalsize):
        """Calculates and Manages Progress"""
        print("Progress Started")
        read_data = blocknum * blocksize
        if totalsize > 0:
            dpercent = read_data * 100 / totalsize
            self.progressBar_t1.setValue(dpercent)
            QApplication.processEvents()

    def handleBrowse(self):
        '''Manages Browsing within the OS'''
        print("Browsing Location")
        location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        self.location_t1.setText(str(location[0]))

    def download(self):
        '''Controls Downloading of files'''
        print("Download Started")
        url = self.url_t1.text()
        location = self.location_t1.text()
        if url == '' or location == '':
            QMessageBox.warning(self, "Invalid Entries", "Invalid URL or Browse Location")
        else:
            try:
                urllib.request.urlretrieve(url, location, self.handleProgress)
            except Exception:
                QMessageBox.warning(self, "Download", "Invalid URL or Browse Location")
                return
        QMessageBox.information(self, "Download Completed", "Download Successful!")
        self.url_t1.setText('')
        self.location_t1.setText('')
        self.progressBar_t1.setValue(0)

    def get_VideoData(self):
        '''Utilizes Video related Data'''
        print("Video Data Retrival")
        vurl = self.vurl_t2.text()
        if vurl == '':
            QMessageBox.warning(self, "Invalid Entries", "Invalid Video URL")
        else:
            video = pafy.new(vurl, ydl_opts={"nocheckcertificate": True})

        qualities = video.streams
        for stream in qualities:
            size = humanize.naturalsize(stream.get_filesize())
            data = "{} {} {} {}".format(stream.mediatype, stream.extension, stream.quality, size)
            self.vquality.addItem(data)

    def videoBrowse(self):
        print("Browse Video")
        location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        self.vlocation_t2.setText(str(location[0]))

    def downloadVideo(self):
        print("Youtube Video Download")
        vurl = self.vurl_t2.text()
        vlocation = self.vlocation_t2.text()
        if vurl == '' or vlocation == '':
            QMessageBox.warning(self, "Invalid Entries", "Invalid URL or Browse Location")
        else:
            video = pafy.new(vurl, ydl_opts={"nocheckcertificate": True})
            vstream = video.streams
            quality = self.vquality.currentIndex()
            download = vstream[quality].download(filepath=vlocation, callback=self.videoProgress)
        QMessageBox.information(self, "Download Completed", "Download Successful!")
        self.vurl_t2.setText('')
        self.vlocation_t2.setText('')
        self.vprogressBar_t2.setValue(0)

    def videoProgress(self, total, recieved, ratio, rate, time):
        print("Video Progress Start")
        read_data = recieved
        if total > 0:
            dpercent = read_data * 100 / total
            self.vprogressBar_t2.setValue(dpercent)
            remtime = round(time / 60, 2)
            st = " {} minutes remaining".format(remtime)
            self.vrem.setText(st)
            QApplication.processEvents()

    def playlistBrowse(self):
        print("Browse Playlist")
        location = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.plocation_t2.setText(str(location[0]))

    def downloadPlaylist(self):
        print("Youtube Playlist Download")
        purl = self.purl_t2.text()
        plocation = self.plocation_t2.text()
        if purl == '' or plocation == '':
            QMessageBox.warning(self, "Invalid Entries", "Invalid URL or Browse Location")
        else:
            playlist = pafy.get_playlist(purl, ydl_opts={"nocheckcertificate": True})
            plvideos = playlist["items"]
            self.tvlcd.display(len(plvideos))
            print(len(plvideos))
            os.chdir(plocation)
            if os.path.exists(str(playlist["title"])):
                os.chdir(str(playlist["title"]))
            else:
                os.mkdir(str(playlist["title"]))
                os.chdir(str(playlist["title"]))
            vcurrent = 1
            quality = self.pquality.currentIndex()
            for video in plvideos:
                self.cvlcd.display(vcurrent)
                current_video = video["pafy"]
                vstream = current_video.streams
                download = vstream[quality].download(callback=self.playlistProgress)
                QApplication.processEvents()
                vcurrent += 1

    def playlistProgress(self, total, recieved, ratio, rate, time):
        print("Playlist Progress Start")
        read_data = recieved
        if total > 0:
            dpercent = read_data * 100 / total
            self.pprogressBar_t2.setValue(dpercent)
            remtime = round(time / 60, 2)
            st = " {} minutes remaining".format(remtime)
            self.prem.setText(st)
            QApplication.processEvents()

    def pageHome(self):
        print("Home Page")
        self.tabWidget.setCurrentIndex(0)

    def pageDownload(self):
        print("Download Page")
        self.tabWidget.setCurrentIndex(1)

    def pageYoutube(self):
        print("Youtube Page")
        self.tabWidget.setCurrentIndex(2)

    def pageSettings(self):
        print("Settings Page")
        self.tabWidget.setCurrentIndex(3)

    def themeDarkOrange(self):
        print("Dark Orange Theme")
        style = open("themes/darkorange.css", "r")
        style = style.read()
        self.setStyleSheet(style)

    def themeDarkBlue(self):
        print("DarkBlue")
        style = open("themes/darkblu.css", "r")
        style = style.read()
        self.setStyleSheet(style)

    def themeDark(self):
        print("Dark Theme")
        style = open("themes/qdark.css", "r")
        style = style.read()
        self.setStyleSheet(style)

    def themeDarkGray(self):
        print("Dark Gray")
        style = open("themes/qdarkgray.css", "r")
        style = style.read()
        self.setStyleSheet(style)

    def moveGBox1(self):
        # GBox1 Animation
        print("GBox1")
        animation1 = QPropertyAnimation(self.groupBox_1, b"geometry")
        animation1.setDuration(1000)
        animation1.setStartValue(QRect(0, 0, 0, 0))
        animation1.setEndValue(QRect(90, 30, 280, 150))
        self.animation1 = animation1
        animation1.start()

    def moveGBox2(self):
        # GBox2 Animation
        print("GBox2")
        animation2 = QPropertyAnimation(self.groupBox_2, b"geometry")
        animation2.setDuration(1000)
        animation2.setStartValue(QRect(0, 0, 0, 0))
        animation2.setEndValue(QRect(500, 30, 280, 150))
        self.animation2 = animation2
        animation2.start()

    def moveGBox3(self):
        # GBox3 Animation
        print("GBox3")
        animation3 = QPropertyAnimation(self.groupBox_3, b"geometry")
        animation3.setDuration(1000)
        animation3.setStartValue(QRect(0, 0, 0, 0))
        animation3.setEndValue(QRect(90, 250, 280, 150))
        self.animation3 = animation3
        animation3.start()

    def moveGBox4(self):
        # GBox4 Animation
        print("GBox4")
        animation4 = QPropertyAnimation(self.groupBox_4, b"geometry")
        animation4.setDuration(1000)
        animation4.setStartValue(QRect(0, 0, 0, 0))
        animation4.setEndValue(QRect(500, 250, 280, 150))
        self.animation4 = animation4
        animation4.start()

    def pageCall1(self):
        print("Call Solo Download")
        self.tabWidget.setCurrentIndex(1)

    def pageCall2(self):
        print("Call Youtube Video Page")
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget_2.setCurrentIndex(0)

    def pageCall3(self):
        print("Call Youtube Playlist Page")
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget_2.setCurrentIndex(1)

    def pageCall4(self):
        print("Call Settings Page")
        self.tabWidget.setCurrentIndex(3)


def major():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    # getch() for Python Output Window
    app.exec_()

if __name__ == '__main__':
    major()
