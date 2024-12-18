import sys
import matplotlib
matplotlib.use('QtAgg')
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QSlider, QHBoxLayout, QVBoxLayout, QListWidget, QAbstractItemView, QPushButton, QLineEdit, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Vue(QMainWindow):

    open_one_signal = pyqtSignal()
    open_more_signal = pyqtSignal()
    save_as_signal = pyqtSignal()
    save_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logiciel d'astrophotographie")
        self.setMinimumSize(1080, 600)

        self.main_widget = MainWidget()

        self.setCentralWidget(self.main_widget)

        menu_bar = self.menuBar()

        menu_file = menu_bar.addMenu("Fichier")
        menu_file.addAction("Ouvrir 1 fichier", self.send_open_one)
        menu_file.addAction("Ouvrir plusieurs fichiers", self.send_open_more)
        menu_file.addAction("Enregister sous", self.send_save_as)
        menu_file.addAction("Enregistrer", self.send_save)

    
    def send_open_one(self):
        self.open_one_signal.emit()
    
    def send_open_more(self):
        self.open_more_signal.emit()
    
    def send_save_as(self):
        self.save_as_signal.emit()
    
    def send_save(self):
        self.save_signal.emit()
    



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

    downloadClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.vlayout = QVBoxLayout() ; self.setLayout(self.vlayout)
        
        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.download = QPushButton("Télécharger")

        self.vlayout.addWidget(self.list)
        self.vlayout.addStretch()
        self.vlayout.addWidget(self.download)

        self.download.clicked.connect(self.downloadClicked.emit)


class Filters(QWidget):

    searchClicked = pyqtSignal()

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
        self.search.clicked.connect(self.searchClicked.emit)

    def change_radius(self, val:int):
        self.radius_label.setText("Rayon:  " + str(val) + "deg")

class Center(QWidget):
    def __init__(self):
        super().__init__()

        self.hlayout = QHBoxLayout() ; self.setLayout(self.hlayout)

        self.fig = Figure()
        self.plot = FigureCanvas(self.fig)

        self.hlayout.addWidget(self.plot)

    def update(self):
        self.hlayout.itemAt(0).widget().deleteLater()
        self.hlayout.addWidget(self.plot)
        self.plot.draw()
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
        self.contrast_label = QLabel("Contraste: 99%")
        self.contrast = QSlider(Qt.Orientation.Horizontal)
        self.gamma_label = QLabel("Gamma: 10%")
        self.gamma = QSlider(Qt.Orientation.Horizontal)

        self.r.setRange(0, 1000)
        self.g.setRange(0, 1000)
        self.b.setRange(0, 1000)
        self.contrast.setRange(5000, 10000)
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
        self.contrast_label.setText("Contraste: " + str(val/100) + "%")

    def gamma_changed(self, val: int):
        self.gamma_label.setText("Gamma: " + str(val/10) + "%")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    vue = Vue()
    vue.show()
    sys.exit(app.exec())