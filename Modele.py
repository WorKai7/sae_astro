from astropy.io import fits
from astropy.visualization import PercentileInterval
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
from memory_profiler import profile
from astroquery.mast import Observations

class Modele:
    def __init__(self):
        self.files_opened = []
        self.current_file = ""
        

    def resize(self, data, target_shape):
        if data.shape != target_shape:
            zoom_factors = [t / s for s, t in zip(data.shape, target_shape)]
            return zoom(data, zoom_factors, order=1)
        return data

    # Fonction plus optimisé mais ne fonctionne pas toujours

    # Décorateur pour voir la mémoire dans le terminal
    @profile
    def get_fig_opti(self, files: list, **kwargs):
        combined_image = None

        # On traite chaque fichier 1 par 1 pour réduire l'utilisation de la mémoire à un instant T
        for i, file in enumerate(files):
            # Récupération de la première couche (PRIMARY)
            data = fits.getdata(file, 0)

            # On préremplis l'image finale de 0
            if combined_image is None:
                target_shape = data.shape
                combined_image = np.zeros((target_shape, len(files)), dtype=np.float32)
            print(combined_image.shape)
            
            # Resize
            data = self.resize(data, target_shape)

            # Normalisation
            interval = PercentileInterval(kwargs.get("contrast_percentile", 99))
            data = interval(data)

            # Couleurs custom
            data *= kwargs.get("custom_red", 1) if i == 0 else 1
            data *= kwargs.get("custom_green", 1) if i == 1 else 1
            data *= kwargs.get("custom_blue", 1) if i == 2 else 1

            # Gamma
            data = np.power(data, 1 / kwargs.get("gamma", 1))

            # Mise à jour de l'image finale
            combined_image[..., i] = data

        del data

        # Affichage
        fig, ax = plt.subplots()
        try:
            ax.imshow(combined_image)
            return fig
        except TypeError as e:
            raise e

    def get_fig(self, files: list, **kwargs):
        # Récupération des données des fichiers entrés
        data_list = [fits.getdata(file) for file in files]

        # Récupération de la première couche si la donnée est en 3D
        data_list = [data[0] if len(data.shape) == 3 else data for data in data_list]

        # Resize
        max_shape = max([data.shape for data in data_list])
        data_list = [self.resize(data, max_shape) for data in data_list]

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
            ax.imshow(combined_image)
            return fig
        except TypeError as e:
            print("Erreur de dimensions des images:", e)

    def search(self, name:str, type:str, telescope:str, wavelength:str, radius:float):
        print("Recherche pour", name, type, telescope, wavelength, radius)
        result = Observations.query_criteria(objectname=name, dataproduct_type=type, obs_collection=telescope, wavelength_region=wavelength, radius= str(radius)+ " deg")[0]
        obs_id = result["obsid"]
        self.products = Observations.get_product_list(obs_id)
        return self.products

    def download(self, indexes):
        products = self.products[indexes]
        print(products)
        fit_products = Observations.filter_products(products, extension="fits")
        Observations.download_products(fit_products, download_dir="images/")

