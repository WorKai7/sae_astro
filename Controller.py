import sys
from PyQt6.QtWidgets import QApplication, QFileDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from Vue import Vue
from Modele import Modele

class Controller:
    def __init__(self):
        
        self.vue = Vue()
        self.modele = Modele()

        self.vue.open_one_signal.connect(self.open_one)
        self.vue.open_more_signal.connect(self.open_more)
        self.vue.save_as_signal.connect(self.save_as)
        self.vue.save_signal.connect(self.save)
        self.vue.main_widget.left.filters.searchClicked.connect(self.search)
        self.vue.main_widget.left.file_list.downloadClicked.connect(self.download)
        self.vue.main_widget.right.sliderChanged.connect(self.update_vue)

        self.update_vue()

        self.vue.show()

    
    def open_one(self):
        filename = QFileDialog.getOpenFileName(caption="Selectionnez des fichiers", directory="./images", filter="Fichiers FITS (*.fits *.fit)")[0]
        self.modele.files_opened = [filename]
        self.update_vue()

    def open_more(self):
        filenames = QFileDialog.getOpenFileNames(caption="Selectionnez des fichiers", directory="./images", filter="Fichiers FITS (*.fits *.fit)")[0]
        self.modele.files_opened = filenames
        self.update_vue()

    def save_as(self):
        filename = QFileDialog.getSaveFileName(caption="Enregistrer sous..", directory="./images/images_sauvegardees")[0] + ".jpg"
        if filename != '.jpg':
            self.vue.main_widget.center.fig.gca().axis("off")
            self.vue.main_widget.center.fig.savefig(filename, format="jpg", bbox_inches='tight', pad_inches=0, dpi=300)
            self.vue.main_widget.center.fig.gca().axis("on")
            self.vue.statusBar().showMessage("Image enregistrée sous le nom '" + filename + "'..", 3000)
            self.modele.current_file = filename
    
    def save(self):
        if len(self.modele.current_file) > 0:
            self.vue.main_widget.center.fig.gca().axis("off")
            self.vue.main_widget.center.fig.savefig(self.modele.current_file, format="jpg", bbox_inches='tight', pad_inches=0, dpi=300)
            self.vue.main_widget.center.fig.gca().axis("on")
        else:
            self.save_as()

    def search(self):
        pass

    def download(self):
        pass
    
    def update_vue(self):
        if self.modele.files_opened:
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