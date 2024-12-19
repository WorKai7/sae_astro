import sys
from PyQt6.QtWidgets import QApplication, QFileDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from Vue import Vue
from Modele import Modele

class Controller:
    def __init__(self):
        
        self.vue = Vue()
        self.modele = Modele()

        self.vue.open_files_signal.connect(self.open_files)
        self.vue.save_signal.connect(self.save_as)
        self.vue.searchClicked.connect(self.search)
        self.vue.downloadClicked.connect(self.download)
        self.vue.main_widget.right.sliderChanged.connect(self.update_vue)

        self.update_vue()

        self.vue.show()

    def open_files(self):
        filenames = QFileDialog.getOpenFileNames(caption="Selectionnez des fichiers", directory="./images", filter="Fichiers FITS (*.fits *.fit)")[0]
        self.modele.files_opened = filenames
        self.update_vue()

    def save_as(self, quality: int):
        filename = QFileDialog.getSaveFileName(caption="Enregistrer sous..", directory="./images/images_enregistrees")[0] + ".jpg"
        if filename != '.jpg':
            self.vue.main_widget.center.fig.gca().axis("off")
            self.vue.main_widget.center.fig.savefig(filename, format="jpg", bbox_inches='tight', pad_inches=0, dpi=quality)
            self.vue.main_widget.center.fig.gca().axis("on")
            self.vue.statusBar().showMessage("Image enregistrée sous le nom '" + filename + "'..", 3000)
            self.modele.current_file = filename

    def search(self, name:str, type:str, telescope:str, wavelength:str, radius:float):
        self.vue.main_widget.left.file_list.list.clear()
        products = self.modele.search(name, type, telescope, wavelength, radius)
        for product in products:
            self.vue.main_widget.left.file_list.list.addItem(product["description"])
        self.vue.statusBar().showMessage("Recherche terminée", 2000)

    def download(self, indexes):
        self.modele.download([index.row() for index in indexes])
    
    def update_vue(self):
        if self.modele.files_opened:
            try:
                self.vue.main_widget.center.fig = self.modele.get_fig_opti(self.modele.files_opened,
                                                                    contrast_percentile=self.vue.main_widget.right.contrast.value()/100,
                                                                    gamma=self.vue.main_widget.right.gamma.value()/100,
                                                                    custom_red=self.vue.main_widget.right.r.value()/100,
                                                                    custom_green=self.vue.main_widget.right.g.value()/100,
                                                                    custom_blue=self.vue.main_widget.right.b.value()/100)
            except TypeError:
                try:
                    self.vue.main_widget.center.fig = self.modele.get_fig(self.modele.files_opened,
                                                                    contrast_percentile=self.vue.main_widget.right.contrast.value()/100,
                                                                    gamma=self.vue.main_widget.right.gamma.value()/100,
                                                                    custom_red=self.vue.main_widget.right.r.value()/100,
                                                                    custom_green=self.vue.main_widget.right.g.value()/100,
                                                                    custom_blue=self.vue.main_widget.right.b.value()/100)
                except TypeError:
                    self.vue.statusBar().showMessage("Erreur: trop, pas assez ou mauvaises dimensions de fichiers sélectionnés", 3000)
            
            self.vue.main_widget.center.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec())