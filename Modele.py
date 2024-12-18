from astropy.io import fits
from astropy.visualization import PercentileInterval
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom

class Modele:
    def __init__(self):
        self.__files_opened = ["images/Tarantula/Tarantula_Nebula-halpha.fit", "images/Tarantula/Tarantula_Nebula-oiii.fit", "images/Tarantula/Tarantula_Nebula-sii.fit"]
        self.current_file = ""

    
    def get_opened_files(self):
        return self.__files_opened
        

    def resize(self, data, target_shape):
        if data.shape != target_shape:
            zoom_factors = [t / s for s, t in zip(data.shape, target_shape)]
            return zoom(data, zoom_factors, order=1)
        return data

    def get_fig(self, files: list, **kwargs):
        # Récupération des données des fichiers entrés
        data_list = [fits.getdata(file) for file in files]

        # Récupération de la première couche si la donnée est en 3D
        data_list = [data[0] if len(data.shape) == 3 else data for data in data_list]

        # Resize
        data_list = [self.resize(data, data_list[0].shape) for data in data_list]

        # Print de la taille de chaque image pour vérif
        for data in data_list:
            print(data.shape)

        # Contraste
        interval = PercentileInterval(kwargs.get("contrast_percentile", 99))
        norm_list = [interval(data) for data in data_list]

        # Couleurs custom
        if len(files) == 3:
            norm_list[0] *= kwargs.get("custom_red", 1)
            norm_list[1] *= kwargs.get("custom_green", 1)
            norm_list[2] *= kwargs.get("custom_blue", 1)

        # Gamma
        norm_list = [np.power(norm, 1 / kwargs.get("gamma", 1)) for norm in norm_list]

        # Combinaison
        combined_image = np.dstack(norm_list)

        # Affichage
        try:
            fig, ax = plt.subplots()
            ax.imshow(combined_image, cmap='gray')
            return fig
        except TypeError as e:
            print("Erreur de dimensions des images:", e)


# get_fig("images/Tarantula/Tarantula_Nebula-halpha.fit", "images/Tarantula/Tarantula_Nebula-oiii.fit", "images/Tarantula/Tarantula_Nebula-sii.fit", gamma=2)
# get_fig("images/f001a1hr.fits", "images/f001a25o.fits", "images/f001a066.fits", contrast_percentile=95, gamma=0.8)