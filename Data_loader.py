import pandas as pd
from pathlib import Path
from matrix import Matrix

_EXTENSIONS={
    ".xlsx":   pd.read_excel,
    ".xls":    pd.read_excel,
    ".csv":    pd.read_csv
}
def Data_Loader(path):
    file_extension=Path(path).suffix.lower()
    extension=_EXTENSIONS.get(file_extension)

    if extension is None:
        valid_format=", ".join(_EXTENSIONS.keys())
        raise ValueError(f"Unsupported format: '{file_extension}'. Valid formats: {valid_format}")

    raw_data=extension(path)

    data=raw_data.select_dtypes(include="number")
    meta_data=raw_data.select_dtypes(exclude="number")

    data_matrix=Matrix(data.values)

    return data_matrix,meta_data


