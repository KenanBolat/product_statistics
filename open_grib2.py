import xarray
import matplotlib.pyplot as plt
import scipy.misc
f_ = r"/external/b/HSAF_archive_bak_191212/h13_extract/h13_20191120_day_merged.grib2"

xs = xarray.open_dataset(f_, engine='cfgrib')
a_=xs.get("rssc")
x_show = plt.imshow(a_)


# scipy.misc.toimage(a_, cmin=0.0, cmax=).save('outfile.jpg')