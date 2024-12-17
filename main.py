from astropy.io import fits
from astropy.visualization import PercentileInterval, LogStretch, ImageNormalize
import numpy as np
import matplotlib.pyplot as plt
import os

def show_img_from_single_file(file: str) -> None:
    data = fits.getdata(file)

    if len(data.shape) == 3:
        data = data[0]
    elif len(data.shape) == 1:
        print("Mauvaises dimensions d'image", str(data.shape))
        return

    interval = PercentileInterval(99)
    norm = ImageNormalize(data, interval=interval, stretch=LogStretch())

    plt.imshow(data, cmap='gray', norm=norm)
    plt.colorbar()
    plt.show()



def show_img_from_rbg_files(file_r: str, file_g: str, file_b: str):
    data_r = fits.getdata(file_r)
    data_g = fits.getdata(file_g)
    data_b = fits.getdata(file_b)

    if len(data_b.shape) == 3:
        data_b = data_b[0]
    if len(data_g.shape) == 3:
        data_g = data_g[0]
    if len(data_r.shape) == 3:
        data_r = data_r[0]

    interval = PercentileInterval(99)
    r_norm = interval(data_r)
    g_norm = interval(data_g)
    b_norm = interval(data_b)

    # Superposition des 3 images rgb
    rgb_image = np.dstack([r_norm, g_norm, b_norm])


    plt.imshow(rgb_image, cmap='gray')
    plt.show()


show_img_from_rbg_files("Tarantula/Tarantula_Nebula-halpha.fit", "Tarantula/Tarantula_Nebula-oiii.fit", "Tarantula/Tarantula_Nebula-sii.fit")
# show_img_from_single_file("mastDownload/HST/ua010604m/ua010604m_c0f.fits")

# with fits.open("mastDownload/HST/ua010604m/ua010604m_cgr.fits") as hdul:
#     print(hdul[1].data)