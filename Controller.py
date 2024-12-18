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
        pass

    def open_more(self):
        pass

    def save_as(self):
        filename = QFileDialog.getSaveFileName(caption="Enregistrer sous..", directory="./images/images_sauvegardees")[0] + ".jpg"
        if filename:
            self.vue.main_widget.center.fig.gca().axis("off")
            self.vue.main_widget.center.fig.savefig(filename, format="jpg", bbox_inches='tight', pad_inches=0, dpi=300)
            self.vue.main_widget.center.fig.gca().axis("on")
            self.vue.statusBar().showMessage("Image enregistrée sous le nom '" + filename + "'..", 3000)
            self.modele.current_file = filename

    def save(self):
        pass

    def search(self):
        pass

    def download(self):
        pass

    def update_vue(self):
        if self.modele.get_opened_files():
            self.vue.main_widget.center.fig.gca().clear()
            self.vue.main_widget.center.fig = self.modele.get_fig(self.modele.get_opened_files(),
                                                                  contrast_percentile=self.vue.main_widget.right.contrast.value()/100,
                                                                  gamma=self.vue.main_widget.right.gamma.value()/100,
                                                                  custom_red=self.vue.main_widget.right.r.value()/100,
                                                                  custom_green=self.vue.main_widget.right.g.value()/100,
                                                                  custom_blue=self.vue.main_widget.right.b.value()/100)
            
            self.vue.main_widget.center.plot = FigureCanvas(self.vue.main_widget.center.fig)
            self.vue.main_widget.center.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec())