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

    # Décorateur pour voir la mémoire dans le terminal
    @profile
    def get_fig(self, files: list, **kwargs):
        combined_image = None

        # On traite chaque fichier 1 par 1 pour réduire l'utilisation de la mémoire à un instant T
        for i, file in enumerate(files):
            # Récupération de la première couche (PRIMARY)
            data = fits.getdata(file, 0)

            # On préremplis l'image finale de 0
            if combined_image is None:
                target_shape = data.shape
                combined_image = np.zeros((*target_shape, len(files)), dtype=np.float32)
            
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

    def search(self, type:str, telescope:str, wavelength:str, radius:float):
        result= Observations.query_criteria(dataproduct_type=[type], obs_collection=telescope, wavelength_region=wavelength, radius= str(radius)+ " deg")[0]
        obs_id = result["obsid"]
        self.products = Observations.get_product_list(obs_id)
        return self.products

    def download(self, product):
        fit_product = Observations.filter_products(product, extension="fits")
        Observations.download_products(fit_product)
# get_fig("images/Tarantula/Tarantula_Nebula-halpha.fit", "images/Tarantula/Tarantula_Nebula-oiii.fit", "images/Tarantula/Tarantula_Nebula-sii.fit", gamma=2)
# get_fig("images/f001a1hr.fits", "images/f001a25o.fits", "images/f001a066.fits", contrast_percentile=95, gamma=0.8)