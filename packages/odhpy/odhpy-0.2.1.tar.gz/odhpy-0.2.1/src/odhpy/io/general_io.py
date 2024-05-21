import os
import numpy as np
import pandas as pd
from odhpy import utils
from odhpy import io
import re

def read(filename, **kwargs):
    filename_lower = filename.lower()
    new_df = None
    if (filename_lower.endswith('.res.csv')):
        new_df = io.read_ts_csv(filename, **kwargs)
    elif (filename_lower.endswith('.csv')):
        new_df = io.read_res_csv(filename, **kwargs)
    elif (filename_lower.endswith('.idx')):
        new_df = io.read_idx(filename, **kwargs)
    elif (re.search(".[0-9]{2}d$", filename_lower)):
        new_df = io.read_iqqm_lqn_output (filename, **kwargs)
    else:
        raise ValueError(f"Unknown file extension: {filename}")