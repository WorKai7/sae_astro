from astroquery.mast import Observations

result = Observations.query_criteria(objectname="NGC 3132", dataproduct_type=["image"], obs_collection="HST", wavelength_region="OPTICAL", radius="0.1 deg")[0]

# Id de l'observation
obs_id = result["obsid"]
products = Observations.get_product_list(obs_id)

print(products)

fits_products = Observations.filter_products(products, extension="fits")

Observations.download_products(fits_products)
