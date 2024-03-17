import pandas as pd
from scipy.signal import butter, filtfilt


# todo: remove usage when hardware lowpass is installed. (put in depreciated)
class Filter:

    def butter_lowpass_filter(self, data: pd.DataFrame, column: str, cutoff: float, fs: float, order: int) -> pd.DataFrame:
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype="low", analog=False)
        data[f"{column}_lowpass"] = filtfilt(b, a, data[column])

        return data
