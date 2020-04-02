"""
Downloader-App:- This is a Python Language program to built a Desktop Application in  which we can use to download various types of files like documents, videos, installer packages, etc, whose links are available online. 
Only the thing to note is that while giving file-name, we need to specify it's extention with the file-name(Ex: abc.docx).
"""
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

"""
Main:- This is the class that integrates all the functionalities of the application and manages them according to their respective calls.
"""
class Main(QMainWindow, ui):

    """
    __init__:- This is the constructor method of the class responsible for initiating the application developed.
    """
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.initUi()
        self.handleButton()

    """
    initUi:- This method enables the initial UI of the application.
    """
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

    """
    handleButton:- This method operates and manages the buttons and corresponding calls for the respective methods.
    """
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

    """
    handleProgress:- This method manages and controls the progress display bar for the file being downloaded.
    Variables:-
        totalsize(int) - holds total number of bits present in the file.
        read_data(int) - holds the total data downloaded.
        dpercent(int) - holds the ratio of read_data to totalsize.
        blocksize(int) - holds the size of each block of bits.
        blocknum(int) - holds the index for currently downloading block.
    """
    def handleProgress(self, blocknum, blocksize, totalsize):
        """Calculates and Manages Progress"""
        print("Progress Started")
        read_data = blocknum * blocksize
        if totalsize > 0:
            dpercent = read_data * 100 / totalsize
            self.progressBar_t1.setValue(dpercent)
            QApplication.processEvents()

    """
    handleBrowse:- This method is used to refer the download location of the file to the application.
    Variables:-
        location(string) - holds the destination address where the file is needed to be downloaded.
    """
    def handleBrowse(self):
        '''Manages Browsing within the OS'''
        print("Browsing Location")
        location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        self.location_t1.setText(str(location[0]))

    """
    download:- This method is used to perform the generic downloading which occurs according to the bit-data of the file.
    Variable:-
        url(string) - holds the actual url of the file.
        location(string) - holds the destination address where the file is needed to be downloaded.
    """
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

    """ 
    get_VideoData:- This method is used to retrive data about the video from youtube using a pafy object.
    Variables:- 
        vurl(string) - holds the actual url of the video.
        video(pafy object) - holds the pafy type instance of the video.
        qualities(array of strings) - holds the value of all possible qualities for which the video is available.
        size(string) - holds the size of the file for corresponding quality.
        data(string) - displays entire data regarding a quality for the video.
    """
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

    """ 
    videoBrowse:- This method is used to refer the download location of the video to the application.
    Variables:-
        location(string) - holds the destination address where the video is needed to be downloaded.
    """
    def videoBrowse(self):
        print("Browse Video")
        location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        self.vlocation_t2.setText(str(location[0]))

    """ 
    downloadVideo:- This method calls for the video from the online database and controls and manages it's downloading.
    Variables:- 
        vurl(string) - holds the actual url of the playlist.
        vlocation(string) - holds the destination address where the video is needed to be downloaded.
        quality(string) - holds the quality at which the video is to be downloaded.
        current_video(pafy object) - holds the pafy type instance of a single video.
        vstream(quality-refering object) - holds the available qualities present for the video.
        download(bit-object) - holds and downloads data bitwise.
    """
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

    """ 
    videoProgress:- This method manages and controls the progress display bar for the video being downloaded.
    Variables:-
        total(int) - holds total number of frames present in the video.
        recieved(int) - holds the total data downloaded.
        ratio(int) - holds the ratio of total to recieved.
        time(time object) - holds the estimated time suggested by the youtube.
        rate(int) - holds the ratio of time(in seconds) to total undownloaded data.
        remtime(int) - holds the actual remaining time for video that is being downloaded.
        st(string) - used to display the remtime on screen while the download is in progress.
    """
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

    """ 
    playlistBrowse:- This method is used to refer the download location of the playlist to the application.
    Variables:-
        location(string) - holds the destination address where the playlist is needed to be downloaded.
    """
    def playlistBrowse(self):
        print("Browse Playlist")
        location = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.plocation_t2.setText(str(location[0]))

    """
    downloadPlaylist:- This method calls for the playlist from the online database and controls and manages it's downloading.
    Variables:- 
        purl(string) - holds the actual url of the playlist.
        plocation(string) - holds the destination address where the playlist is needed to be downloaded.
        playlist(pafy object) - holds the pafy type instance of the playlist used to refer data from youtube.
        plvideos(sub-pafy object) - holds the pafy type instance of a single video from the playlist, used to refer data from youtube.
        vcurrent(int) - holds the currently downloading video's position in playlist.
        quality(string) - holds the quality at which the video is to be downloaded.
        current_video(pafy object) - holds the pafy type instance of a single video.
        vstream(quality-refering object) - holds the quality to be downloaded for the current downloading video.
        download(bit-object) - holds and downloads data bitwise.
    """
    def downloadPlaylist(self):
        print("Youtube Playlist Download")
        purl = self.purl_t2.text()
        plocation = self.plocation_t2.text()
        if purl == '' or plocation == '':
            QMessageBox.warning(self, "Invalid Entries", "Invalid URL or Browse Location")
        else:
            playlist = pafy.get_playlist(purl)
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
                download = vstream[quality].download(callback=self.playlistProgress, ydl_opts={"nocheckcertificate": True})
                QApplication.processEvents()
                vcurrent += 1

    """ 
    playlistProgress:- This method manages and controls the progress display bar for every video present in the playlist being downloaded.
    Variables:-
        total(int) - holds total number of videos present in the playlist.
        recieved(int) - holds the total data downloaded.
        ratio(int) - holds the ratio of total to recieved.
        time(time object) - holds the estimated time suggested by the youtube.
        rate(int) - holds the ratio of time(in seconds) to total undownloaded data.
        remtime(int) - holds the actual remaining time for each video that is being downloaded.
        st(string) - used to display the remtime on screen while the download is in progress.
    """
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

    """ 
    pageShifts:- The nevigation buttons present in the left margin of the application can be utilized to directly nevigate between pages. The following 4 methods controls the narration descriped.
    """
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

    """ 
    theme:- The Application can be operated in 4 themes namely Dark Orange, Default, Dark and Dark Blue. The following 4 methods are used to alter between various themes available.
    Variable:-
        style(file object) - For all the following 4 methods this variables holds the instance for altering between the themes.
    """
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

    """ 
    moveGBOX :- The following 4 methods gives animation feature just once when the application is launched.
    Variables:- 
        animation1, animation2, animation3, animation4(objects) -
            They all hold instances for animation call for the followinf 4 methods, respectively.
    """
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

    """ 
    pageCalls :- The application consist of 4 major pages(Home, Generic Download, Youtube Download, Settings) and each of the following 4 methods manages the switching between these pages.
    """
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

""" 
major :- This is the Main method that begins and controls the execution of the complete program.
Variables :-
    app(object) - holds the Instance of the application as whole.
    window(object) - holds the display mechanism of the entire application.
"""
def major():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    # getch() for Python Output Window
    app.exec_()

if __name__ == '__main__':
    major()
