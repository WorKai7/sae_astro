from astroquery.mast import Observations

# Faut mettre un nom d'objet ou il trouve des trucs ou alors changer le telescope pour trouver des images mais après il faut qu'elles soient en 2d
result = Observations.query_criteria(objectname="NGC 346", dataproduct_type="image", obs_collection="JWST", wavelength_region="OPTICAL", radius="0.5 deg")[0]
print(result)

# Id de l'observation
obs_id = result["obsid"]
products = Observations.get_product_list(obs_id)
print(products)

fits_products = Observations.filter_products(products, extension="fits")
print(fits_products)

Observations.download_products(fits_products)
