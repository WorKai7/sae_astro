import sys
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QSlider, QHBoxLayout, QVBoxLayout, QListWidget, QAbstractItemView, QPushButton, QLineEdit, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class Vue(QMainWindow):

    open_files_signal = pyqtSignal()
    save_signal = pyqtSignal(int)
    downloadClicked = pyqtSignal(list)
    searchClicked = pyqtSignal(str, str, str, str, float)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logiciel d'astrophotographie")
        self.setMinimumSize(1080, 600)

        self.main_widget = MainWidget()

        self.setCentralWidget(self.main_widget)

        menu_bar = self.menuBar()

        menu_file = menu_bar.addMenu("Fichier")
        menu_file.addAction("Ouvrir", self.send_open_files)
        save_menu = menu_file.addMenu("Enregister..")
        save_menu.addAction("Haute qualité", self.high_save)
        save_menu.addAction("Moyenne qualité", self.medium_save)
        save_menu.addAction("Basse qualité", self.low_save)

        menu_display = menu_bar.addMenu("Affichage")
        menu_display.addAction("Activer les axes", self.enable_axis)
        menu_display.addAction("Désactiver les axes", self.disable_axis)
        self.main_widget.left.file_list.download.clicked.connect(self.send_download)
        self.main_widget.left.filters.search.clicked.connect(self.send_search)

    
    def send_search(self):
        name = self.main_widget.left.filters.name.text()
        type = self.main_widget.left.filters.type.currentText()
        telescope = self.main_widget.left.filters.telescope.currentText()
        wavelength = self.main_widget.left.filters.wavelength.currentText()
        radius = self.main_widget.left.filters.radius.value()/10

        if all(param is not None and param != "Sélection.." for param in [name, type, telescope, wavelength, radius]):
            self.searchClicked.emit(name, type, telescope, wavelength, radius)
        else:
            self.statusBar().showMessage("Filtres incomplets")

    def send_download(self):
        self.downloadClicked.emit(self.main_widget.left.file_list.list.selectedIndexes())

    def send_open_files(self):
        self.open_files_signal.emit()
    
    def high_save(self):
        self.send_save(3000)

    def medium_save(self):
        self.send_save(1000)

    def low_save(self):
        self.send_save(300)

    def send_save(self, quality: int):
        self.save_signal.emit(quality)

    def enable_axis(self):
        self.main_widget.center.fig.gca().axis("on")
        self.main_widget.center.update()

    def disable_axis(self):
        self.main_widget.center.fig.gca().axis("off")
        self.main_widget.center.update()
    



class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QHBoxLayout() ; self.setLayout(self.main_layout)

        self.left = Left()
        self.center = Center()
        self.right = Right() 

        self.main_layout.addWidget(self.left, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.center, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.right, alignment=Qt.AlignmentFlag.AlignCenter)

    
class Left(QWidget):
    def __init__(self):
        super().__init__()

        self.hlayout = QHBoxLayout() ; self.setLayout(self.hlayout)

        self.filters = Filters()
        self.file_list = FileList()
        
        self.hlayout.addWidget(self.filters)
        self.hlayout.addWidget(self.file_list)


class FileList(QWidget):
    def __init__(self):
        super().__init__()

        self.vlayout = QVBoxLayout() ; self.setLayout(self.vlayout)
        
        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.download = QPushButton("Télécharger")

        self.vlayout.addWidget(self.list)
        self.vlayout.addWidget(self.download)




class Filters(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumWidth(125)
        self.vlayout = QVBoxLayout() ; self.setLayout(self.vlayout)

        self.label = QLabel("Filtres")
        self.name_label = QLabel("Nom:")
        self.name = QLineEdit()
        self.type_label = QLabel("Type d'image:")
        self.type = QComboBox()
        self.type.addItems(["Sélection..", "image", "spectrum", "cube", "table", "lightcurve", "grism", "document"])
        self.telescope_label = QLabel("Téléscope:")
        self.telescope = QComboBox()
        self.telescope.addItems(["Sélection..", "HST", "JWST", "TESS", "Kepler", "GALEX", "SDSS"])
        self.wavelength_label = QLabel("Longueur d'onde:")
        self.wavelength = QComboBox()
        self.wavelength.addItems(["Sélection..", "OPTICAL", "INFRARED", "ULTRAVIOLET", "X-RAY", "RADIO"])
        self.radius_label = QLabel("Rayon:  0.1deg")
        self.radius = QSlider(orientation=Qt.Orientation.Horizontal)
        self.radius.setRange(1, 20)
        self.radius.setValue(1)
        self.search = QPushButton("Rechercher")

        self.vlayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vlayout.addSpacing(30)
        self.vlayout.addWidget(self.name_label)
        self.vlayout.addWidget(self.name)
        self.vlayout.addWidget(self.type_label)
        self.vlayout.addWidget(self.type)
        self.vlayout.addWidget(self.telescope_label)
        self.vlayout.addWidget(self.telescope)
        self.vlayout.addWidget(self.wavelength_label)
        self.vlayout.addWidget(self.wavelength)
        self.vlayout.addWidget(self.radius_label)
        self.vlayout.addWidget(self.radius)
        self.vlayout.addSpacing(30)
        self.vlayout.addWidget(self.search, alignment=Qt.AlignmentFlag.AlignCenter)


        self.radius.valueChanged.connect(self.change_radius)


    def change_radius(self, val:int):
        self.radius_label.setText("Rayon:  " + str(val/10) + "deg")

class Center(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(600)

        self.hlayout = QHBoxLayout() ; self.setLayout(self.hlayout)

        self.fig = plt.figure()
        self.plot = FigureCanvas(self.fig)

        self.hlayout.addWidget(self.plot)

    def update(self):
        self.plot = FigureCanvas(self.fig)
        self.hlayout.itemAt(0).widget().deleteLater()
        self.hlayout.addWidget(self.plot)
        super().update()


class Right(QWidget):

    sliderChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setMaximumWidth(200)

        self.vlayout = QVBoxLayout() ; self.setLayout(self.vlayout)

        self.label = QLabel("Modifiez votre image ici !")
        self.r_label = QLabel("Rouge: 100%")
        self.r = QSlider(Qt.Orientation.Horizontal)
        self.g_label = QLabel("Vert: 100%")
        self.g = QSlider(Qt.Orientation.Horizontal)
        self.b_label = QLabel("Bleu: 100%")
        self.b = QSlider(Qt.Orientation.Horizontal)
        self.contrast_label = QLabel("Plage relative: 99%")
        self.contrast = QSlider(Qt.Orientation.Horizontal)
        self.gamma_label = QLabel("Gamma: 10%")
        self.gamma = QSlider(Qt.Orientation.Horizontal)

        self.r.setRange(0, 1000)
        self.g.setRange(0, 1000)
        self.b.setRange(0, 1000)
        self.contrast.setRange(7000, 10000)
        self.gamma.setRange(0, 1000)
        self.r.setValue(100)
        self.g.setValue(100)
        self.b.setValue(100)
        self.contrast.setValue(9900)
        self.gamma.setValue(100)

        self.vlayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vlayout.addSpacing(50)
        self.vlayout.addWidget(self.r_label)
        self.vlayout.addWidget(self.r)
        self.vlayout.addWidget(self.g_label)
        self.vlayout.addWidget(self.g)
        self.vlayout.addWidget(self.b_label)
        self.vlayout.addWidget(self.b)
        self.vlayout.addSpacing(30)
        self.vlayout.addWidget(self.contrast_label)
        self.vlayout.addWidget(self.contrast)
        self.vlayout.addWidget(self.gamma_label)
        self.vlayout.addWidget(self.gamma)

        
        self.r.sliderReleased.connect(self.sliderChanged.emit)
        self.g.sliderReleased.connect(self.sliderChanged.emit)
        self.b.sliderReleased.connect(self.sliderChanged.emit)
        self.contrast.sliderReleased.connect(self.sliderChanged.emit)
        self.gamma.sliderReleased.connect(self.sliderChanged.emit)

        self.r.valueChanged.connect(self.r_changed)
        self.g.valueChanged.connect(self.g_changed)
        self.b.valueChanged.connect(self.b_changed)
        self.contrast.valueChanged.connect(self.contrast_changed)
        self.gamma.valueChanged.connect(self.gamma_changed)

    def r_changed(self, val: int):
        self.r_label.setText("Rouge: " + str(val) + "%")

    def g_changed(self, val: int):
        self.g_label.setText("Vert: " + str(val) + "%")

    def b_changed(self, val: int):
        self.b_label.setText("Bleu: " + str(val) + "%")

    def contrast_changed(self, val: int):
        self.contrast_label.setText("Plage relative: " + str(round(val/100, 2)) + "%")

    def gamma_changed(self, val: int):
        self.gamma_label.setText("Gamma: " + str(round(val/10, 2)) + "%")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    vue = Vue()
    vue.show()
    sys.exit(app.exec())