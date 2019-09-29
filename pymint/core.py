import copy
import datetime as dt
import logging
from pathlib import Path
from typing import Callable, Iterable, List, Tuple

import pandas as pd

from pymint import processing

logger = logging.getLogger(__name__)


class FileManager:
    """Provide an API for loading data from the file system."""

    _data: pd.DataFrame
    _fname: Path
    _processed_data: pd.DataFrame
    _processing_queue: List[Callable]

    def __init__(self, fname: Path):
        """Initialize the FileManager after checking the existence of `fname`.
        
        Args:
            fname (Path): the file name (relative or absolute) to manage
        """
        if not fname.is_file():
            raise ValueError(f"Could not find '{str(fname)}'")

        self._fname = fname
        self._data = None

        self._processed_data = None
        self._processing_queue = [processing.set_sign_from_type]

    @property
    def data(self) -> pd.DataFrame:
        """Get the data loaded from the file.
        
        If the data has not been loaded, load it.
        """
        if not self._data:
            self._data = self.load()
        return self._data.copy()

    @property
    def fname(self) -> Path:
        """Get the name of the file."""
        return self._fname

    def load(self, parse_as: str = "csv") -> pd.DataFrame:
        """Load the data from the file, and return it as a DataFrame.
        
        Also, format the field names to underscore-separated lowercase words.
        
        Returns:
            data (pd.DataFrame): the data loaded from the file
        """
        if parse_as == "csv" or self._fname.suffix == ".csv":
            logger.info(f"loading {str(self._fname)}")
            data = pd.read_csv(self._fname)
        else:
            raise ValueError(f"could not parse {str(self._fname)} as {parse_as}")

        data["Date"] = data.Date.apply(lambda d: dt.datetime.strptime(d, "%m/%d/%Y"))
        data.columns = data.columns.str.lower().str.replace(" ", "_")
        data.sort_values(by="date", inplace=True)
        return data

    def process(
        self,
        data: pd.DataFrame,
        inplace: bool = True,
        stages: Iterable[Callable[[pd.DataFrame, bool], pd.DataFrame]] = [],
    ) -> pd.DataFrame:
        """Run all data processing functions on the data, and return the result.
        
        Args:
            data (pd.DataFrame): the data to process

            inplace (bool): if True, operate on the DataFrame in place (i.e. don't 
                            make copies)

            stages (Iterable[Callable[[pd.DataFrame, bool], pd.DataFrame]]): 
                            new data processing stages to run; each stage is defined by
                            a callable accepting `data: pd.DataFrame` and `inplace: bool`

        Returns:
            data (pd.DataFrame): a copy of the raw data post-processing
        """
        stages_ = copy.copy(self._processing_queue)
        for stage in stages:
            stages_.append(stage)

        if not inplace:
            data = data.copy()

        while len(stages_):
            func = stages_.pop(0)
            data = func(data=data, inplace=inplace)

        return data

    @property
    def processed_data(self) -> pd.DataFrame:
        """Get the processed data.
        
        Process the data first if it hasn't already been processed.
        
        Returns:
            data (pd.DataFrame): the processed data
        """
        if not self._processed_data:
            # the data property returns a copy, so just do everything after that point
            # in place
            self._processed_data = self.process(self.data, inplace=True)
        return self._processed_data.copy()