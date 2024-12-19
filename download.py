from astroquery.skyview import SkyView

tests = SkyView.get_images(position="Eta Carinae", survey=["DSS"], save_dir="images/")
for test in tests:
    print(test)