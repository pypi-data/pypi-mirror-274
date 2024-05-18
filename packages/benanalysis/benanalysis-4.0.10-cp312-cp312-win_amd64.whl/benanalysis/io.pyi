from __future__ import annotations
import benanalysis._benpy_core
__all__ = ['load_ben_scan_binary_data', 'load_ben_scan_data', 'load_csv']
def load_ben_scan_binary_data(buffer: list[int]) -> dict[str, benanalysis._benpy_core.Scan]:
    """
        Reads binary data and returns a map from the spectrum name to
        the Scan data.
    """
def load_ben_scan_data(file_path: str) -> dict[str, benanalysis._benpy_core.Scan]:
    """
        Reads a BenWin+ .ben data file and returns a map from the spectrum name to
        the Scan data.
    """
def load_csv(file_path: str) -> benanalysis._benpy_core.Scan:
    """
    Load a new Scan object from csv file (or general char delimited)
    """
