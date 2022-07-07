import pickle
import cloudpickle
import json
from prefect.orion.schemas.data import DataDocument
import os

# https://www.geeksforgeeks.org/how-to-iterate-over-files-in-directory-using-python/

directory = '.prefect/my_storage'
directory_blob = '.prefect/from_blob'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    print("File: ", f)

    with open(f, "rb") as buffered_reader:
        try:
            dict_obj = json.load(buffered_reader)
            flow_run_result = DataDocument.parse_obj(dict_obj).decode()
            print(flow_run_result)
        except:
            print("NOT Cloudpickle")