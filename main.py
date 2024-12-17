from astropy.io import fits
from astropy.visualization import PercentileInterval
import numpy as np
import matplotlib.pyplot as plt

def show_img_from_single_file(file: str) -> None:
    data = fits.getdata(file)

    # Si il y a 3 dimensions, on prend le premier élément de 2 dimensions
    if len(data.shape) == 3:
        data = data[0]

    # Vérification de la taille
    if len(data.shape) == 2:
        # Normalisation
        interval = PercentileInterval(99)
        norm = interval(data)

        # Affichage
        plt.imshow(norm, cmap='gray')
        plt.colorbar()
        plt.show()

    else:
        print("Mauvaises dimensions d'image", str(data.shape))
        return




def show_img_from_rbg_files(file_r: str, file_g: str, file_b: str):
    data_r = fits.getdata(file_r)
    data_g = fits.getdata(file_g)
    data_b = fits.getdata(file_b)
    print(f"Dimensions de l'image rouge : {data_r.shape}")
    print(f"Dimensions de l'image verte : {data_g.shape}")
    print(f"Dimensions de l'image bleue : {data_b.shape}")


    if len(data_b.shape) == 3:
        data_b = data_b[0]
    if len(data_g.shape) == 3:
        data_g = data_g[0]
    if len(data_r.shape) == 3:
        data_r = data_r[0]

    # Normalisation
    interval = PercentileInterval(99)
    r_norm = interval(data_r)
    g_norm = interval(data_g)
    b_norm = interval(data_b)

    # Superposition des 3 images rgb
    rgb_image = np.dstack([r_norm, g_norm, b_norm])


    plt.imshow(rgb_image, cmap='gray')
    plt.colorbar()
    plt.show()


def combine_files(*args):
    data_list = [fits.getdata(file) for file in args]

    interval = PercentileInterval(99)
    norm_list = [interval(data) for data in data_list]

    combined_image = np.dstack(norm_list)

    plt.imshow(combined_image, cmap='gray')
    plt.colorbar()
    plt.show()


# show_img_from_rbg_files("Tarantula/Tarantula_Nebula-halpha.fit", "Tarantula/Tarantula_Nebula-oiii.fit", "Tarantula/Tarantula_Nebula-sii.fit")
# show_img_from_rbg_files("mastDownload/HST/w1140204t/w1140204t_c0f.fits", "mastDownload/HST/w1140204t/w1140204t_c1f.fits", "mastDownload/HST/w1140204t/w1140204t_c2f.fits")
combine_files("Tarantula/Tarantula_Nebula-halpha.fit", "Tarantula/Tarantula_Nebula-oiii.fit", "Tarantula/Tarantula_Nebula-sii.fit")
show_img_from_single_file("f001a066.fits")