import glob
from datetime import timedelta
import os
import h5py
import numpy as np
import datetime
import pandas as pd
import xarray

f_ = r"/external/b/HSAF_archive_bak_191212/h13_extract/h13_20191129_day_merged.grib2"
xs = xarray.open_dataset(f_, engine='cfgrib')
c = []

mode = "HSAF"

if mode == 'HSAF':
    # Looks for the merged product
    working_path = r'/external/b/HSAF_archive_bak_191212/h10_extract'
elif mode == "TSMS":
    # Looks for the Mountainous product (Unmerged TSMS produced)
    working_path = r'/external/b/TSMS_archive/h10_HDF'

start_day = datetime.datetime.strptime("20190427", "%Y%m%d")
end_day = datetime.datetime.strptime("20191231", "%Y%m%d")
date_list_h10 = [start_day + timedelta(n) for n in range(int((end_day - start_day).days) + 1)]

d_s_format = "%Y%m%d"
H5_files = [file_ for file_ in glob.glob1(working_path, "*.H5")]
important_values = [0, 42, 85]
for en, date_ in enumerate(date_list_h10):

    merge = 0
    date_in = date_.strftime(d_s_format)
    try:
        match = list(filter(lambda x: x.find(date_in) != -1, H5_files))
        if len(match) > 0:
            hf_h10 = h5py.File(os.path.join(working_path, match[0]), 'r')
            data_h10 = hf_h10['SC']
            test_points = [data_h10[524, 1579],
                           data_h10[549, 1547],
                           data_h10[562, 1642],
                           data_h10[352, 839],
                           data_h10[344, 914]]

            liste = [item in important_values for item in test_points]
            print(liste)
        else:
            pass
    except BaseException:
        pass
