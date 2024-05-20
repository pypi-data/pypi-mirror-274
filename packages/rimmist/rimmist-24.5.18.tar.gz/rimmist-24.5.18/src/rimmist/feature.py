


#
from typing import Any

import joblib  # 1.1.0
import numpy as np  # 1.23.1
import pandas as pd  # 1.4.3

from utils import SQLite3



#
class FeatureApp(object):
    '''
    this class contains pure logic only, errors and exceptions are ignored temporarily

    do not use __init__(self), use class attribute instead
    '''
    output: dict[str, np.nan] = joblib.load('./config/feature_app.joblib')


    #
    @staticmethod
    def f_clean(df: pd.DataFrame) -> pd.DataFrame:
        '''
        contains pure and portable python logic only
        incompatible with online data structure

        future:
            handling errors and exceptions
            handling pre-installed packages
            optimising interval calculation
        unnecessary:
            handling self packages
        '''
        # conversion
        for c in ['sample_time', 'install_time', 'upgrade_time']:
            df[c] = pd.to_datetime(df[c].astype(str).str.slice(0, 19), errors='coerce', format=None)

        # backtrack
        df = df[df.install_time.lt(df.sample_time) & df.upgrade_time.lt(df.sample_time)]
        df = df.sort_values(['install_time', 'upgrade_time', 'package_name']).drop_duplicates('package_name', keep='last')

        # config
        df_config = SQLite3.f_read('feature.sqlite3', 'app')
        df = df.merge(df_config, on='package_name', how='left')
        del df_config

        # field
        df['sample_date'] = df.sample_time.dt.floor('D')
        df['install_date'] = df.install_time.dt.floor('D')
        df['upgrade_date'] = df.upgrade_time.dt.floor('D')
        df['init_date'] = df.install_date.min()

        df['install_datediff'] = (df.sample_date - df.install_date) / np.timedelta64(1, 'D')
        df['install_duration'] = (df.install_date - df.init_date) / np.timedelta64(1, 'D')

        df['upgrade_datediff'] = (df.sample_date - df.upgrade_date) / np.timedelta64(1, 'D')
        df['upgrade_duration'] = (df.upgrade_date - df.init_date) / np.timedelta64(1, 'D')

        return df


    #
    @staticmethod
    def f_1d(df: pd.DataFrame) -> None:
        '''
        None = 1
            count = 1

        install_time = 54 = 3 * 16 + 6 * 1
            install_datediff, install_duration, install_interval = 3 * 16
            install_quarter, install_month, install_week, install_dayofweek, install_day, install_hour = 6 * 1

        upgrade_time = 54 = 3 * 16 + 6 * 1
            upgrade_datediff, upgrade_duration, upgrade_interval = 3 * 16
            upgrade_quarter, upgrade_month, upgrade_week, upgrade_dayofweek, upgrade_day, upgrade_hour = 6 * 1

        package_name
            package_category (google, self-defined) = n * 2
            package_status (200 or 404) = 1 * 2
            package_download (google) = 1 * 16
            package_score (google) = 1 * 16

        '''
        # field
        df['install_interval'] = df.install_date.diff().dt.days
        df['upgrade_interval'] = df.upgrade_date.diff().dt.days

        # 1d - None
        FeatureApp.output['count_dinf'] = df.shape[0]

        # 1d - install_time - datediff, duration, interval
        for c in ['install_datediff', 'install_duration', 'install_interval']:
            FeatureApp.output.update(FeatureApp.__f_calc_statistical_domain(df[c]))

        # 1d - install_time - quarter, month, week, dayofweek, day, hour
        for unit in ['quarter', 'month', 'week', 'dayofweek', 'day', 'hour']:
            obj = df.install_time.dt if unit != 'week' else df.install_time.dt.isocalendar()
            FeatureApp.output[f'install_{unit}_mode_dinf'] = getattr(obj, unit).mode()[0]

        # 1d - upgrade_time - datediff, duration, interval
        for c in ['upgrade_datediff', 'upgrade_duration', 'upgrade_interval']:
            FeatureApp.output.update(FeatureApp.__f_calc_statistical_domain(df[c]))

        # 1d - upgrade_time - quarter, month, week, dayofweek, day, hour
        for unit in ['quarter', 'month', 'week', 'dayofweek', 'day', 'hour']:
            obj = df.upgrade_time.dt if unit != 'week' else df.upgrade_time.dt.isocalendar()
            FeatureApp.output[f'upgrade_{unit}_mode_dinf'] = getattr(obj, unit).mode()[0]

        return None


    #
    def __f_calc_statistical_domain(srs: pd.Series) -> dict[str, Any]:
        '''
        based on wikipedia: descriptive_statistics, statistical_dispersion

        1 = mode
        2 = count + ratio
        16 = 3 + 4 + 4 + 5
        count, ratio, nunique?
        max, min, range
        mean, median, mode, iqr
        std, var, skew, kurt
        aad, mad, oad, cv, vmr
        '''
        dct, prefix = {}, srs.name  #?

        for method in ['max', 'min', 'mean', 'median', 'mode', 'std', 'var', 'skew', 'kurt']:
            dct[f'{prefix}_{method}_dinf'] = getattr(srs, method)()

        dct[f'{prefix}_mode_dinf'] = dct[f'{prefix}_mode_dinf'][0] if dct[f'{prefix}_mode_dinf'].size else np.nan  #? KeyError
        dct[f'{prefix}_range_dinf'] = dct[f'{prefix}_max_dinf'] - dct[f'{prefix}_min_dinf']
        dct[f'{prefix}_iqr_dinf'] = srs.quantile(0.75) - srs.quantile(0.25)
        dct[f'{prefix}_aad_dinf'] = srs.sub(dct[f'{prefix}_mean_dinf']).abs().mean()
        dct[f'{prefix}_mad_dinf'] = srs.sub(dct[f'{prefix}_median_dinf']).abs().mean()
        dct[f'{prefix}_oad_dinf'] = srs.sub(dct[f'{prefix}_mode_dinf']).abs().mean()
        dct[f'{prefix}_cv_dinf'] = dct[f'{prefix}_std_dinf'] / dct[f'{prefix}_mean_dinf'] if dct[f'{prefix}_mean_dinf'] != 0 else np.nan  # ZeroDivisionError
        dct[f'{prefix}_vmr_dinf'] = dct[f'{prefix}_var_dinf'] / dct[f'{prefix}_mean_dinf'] if dct[f'{prefix}_mean_dinf'] != 0 else np.nan  # ZeroDivisionError

        return dct


    #
    



        

        



