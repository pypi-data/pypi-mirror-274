import numpy as np

import noko
from noko.csv_output import CSVOutputEngine
import noko.np


def test_summarize_array(tmp_path):
    run_name = "test_summarize_array"
    output = CSVOutputEngine(runs_dir=tmp_path, run_name=run_name)
    output.log_row_inner(
        noko.Row(
            table_name="test_table1",
            raw={"a": np.arange(10)},
            step=10,
        )
    )
    f_name = f"{tmp_path}/{run_name}/test_table1.csv"
    data = noko.csv_output.load_csv_file(f_name)
    assert data["a.mean"] == [4.5]
    assert data["a.min"] == [0]
    assert data["a.max"] == [9]
    assert data["a.std"][0] > 2.5
