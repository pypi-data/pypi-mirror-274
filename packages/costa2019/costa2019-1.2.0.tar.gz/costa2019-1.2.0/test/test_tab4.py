import pandas as pd

from costa2019 import pth_clean


def test_temps_are_all_positive():
    df = pd.read_csv(pth_clean / "tab4.csv", sep=";", comment="#", parse_dates=['date'],
                     index_col=['variety', 'modality', 'date'])

    assert (df > 0).all().all()
