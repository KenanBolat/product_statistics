import glob
from datetime import timedelta
import os

import numpy as np
import datetime
import pandas as pd
import xarray

# SNOW = range(0,300)
# CLOUD = 42 #yok
LAND = 0
SEA = -20
NODATA1 = -1
NODATA2 = -2
# TODO find important and nodata values and test values

start = datetime.datetime.now()

mode = "HSAF_h12"

if mode == 'HSAF_h12':
    # Looks for the merged product
    working_path = r"/external/b/HSAF_archive_bak_191212/h12_extract"
    # working_path = r"/external/b/HSAF_archive_bak_191212/test"
elif mode == "TSMS":
    # Looks for the Mountainous product (Unmerged TSMS produced)
    working_path = r'/external/b/TSMS_archive/h10_HDF'

start_day = datetime.datetime.strptime("20121128", "%Y%m%d")

end_day = datetime.datetime.strptime("20191231", "%Y%m%d")
date_list_h12 = [start_day + timedelta(n) for n in range(int((end_day - start_day).days) + 1)]

d_s_format = "%Y%m%d"
grib2_files = [file_ for file_ in glob.glob1(working_path, "*.grib2")]
result = []

important_values = range(300)  # they need to be changed 0 = land 0-300 arası = snow


for en, date_ in enumerate(date_list_h12):
    print(datetime.datetime.now() - start)
    merge = 0
    date_in = date_.strftime(d_s_format)
    try:
        match = list(filter(lambda x: x.find(date_in) != -1, grib2_files))
        if len(match) > 0:
            name_file = os.path.join(working_path, match[0])
            f_ = xarray.open_dataset(name_file, engine='cfgrib')
            grib2_array = f_.get("rssc")
            test_points = [grib2_array.values[143, 257],
                           grib2_array.values[148, 252],
                           grib2_array.values[138, 236],
                           grib2_array.values[114, 113],
                           grib2_array.values[117, 129]]

            if all(item in important_values for item in test_points):
                merge = 1
            else:
                print("No data found in {}".format(date_))

            a = np.unique(grib2_array, return_counts=True)
            unique, counts = np.unique(grib2_array, return_counts=True)
            b = dict(zip(unique, counts / grib2_array.size * 100))

            if NODATA1 not in b.keys(): b[NODATA1] = 0
            if NODATA2 not in b.keys(): b[NODATA2] = 0
            if SEA not in b.keys(): b[SEA] = 0
            if LAND not in b.keys(): b[LAND] = 0

            snow = 100 - (b[LAND] + b[SEA] + b[NODATA1] + b[NODATA2])
            data_count = grib2_array.size
            c = ['H12', date_in, merge, snow, b[LAND], b[SEA], b[NODATA1] + b[NODATA2], grib2_array.size]

            c.extend(test_points)
            result.append(c)
            f_.close()
        else:
            result.append(['H12', date_in, merge, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            f_.close()

    except BaseException as be:
        print("Problem")
        merge = be
        result.append(['H12', date_in, merge, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        f_.close()
        continue

print(datetime.datetime.now() - start)

data_frame = pd.DataFrame(result,
                          columns=['Product', "Date", "MERGE", "SNOW%", "LAND %", "SEA %", "NODATA%",
                                   "DATA Count", "Test_P_1", "Test_P_2", "Test_P_3", "Test_P_4", "Test_P_5"])
data_frame.to_csv(datetime.datetime.now().strftime(d_s_format) + "_" + mode + ".csv")
