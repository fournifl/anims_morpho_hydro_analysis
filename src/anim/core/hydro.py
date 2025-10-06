import numpy as np
import pandas as pd


def read_csv_waves(waves):
    # read csv
    wave_data = pd.read_csv(waves.file)

    # convert date to datetime
    wave_data[waves.key_t] = pd.to_datetime(wave_data[waves.key_t])

    # set date as index
    wave_data = wave_data.set_index(wave_data[waves.key_t])

    # set nan instead of fill_value
    wave_data[waves.key_dir][wave_data[waves.key_dir] == 999.999] = np.nan
    wave_data[waves.key_dir][wave_data[waves.key_dir] > 360] = np.nan

    # convert direction (0, 360) to (-180, 180)
    if waves.convert_direction_0_360_to_m180_180:
        wave_data.loc[wave_data[waves.key_dir] > 180, waves.key_dir] -= 360

    # remove aberrant wave height values
    wave_data[waves.key_hs][wave_data[waves.key_hs] > waves.threshold_aberrant_hs] = (
        np.nan
    )

    # remove aberrant wave period values
    wave_data[waves.key_period][
        wave_data[waves.key_period] > waves.threshold_aberrant_period
    ] = np.nan

    # compute wave thresholds
    thresholds = pd.DataFrame(columns=["percentile", "threshold", "colors"])
    thresholds["percentile"] = np.array([0.5, 0.7, 0.8, 0.9, 0.95, 0.98, 0.99])
    thresholds["threshold"] = [
        wave_data[waves.key_hs].quantile(p) for p in thresholds["percentile"]
    ]
    thresholds["colors"] = (
        "greenyellow",
        "yellow",
        "gold",
        "orange",
        "orangered",
        "red",
        "darkred",
    )

    # setting wave masks
    for ii in range(thresholds.shape[0]):
        wave_data["p_" + str(thresholds["percentile"][ii])] = (
            wave_data[waves.key_hs] > thresholds["threshold"][ii]
        )

    # filter by direction
    wave_data["filtered_by_direction"] = (
        wave_data[waves.key_dir] > waves.angle_min_threshold
    ) & (wave_data[waves.key_dir] < waves.angle_max_threshold)

    return wave_data, thresholds


def get_storm_dates_in_out(wave_data, percentile_min_threshold, key_dir):
    # storm in the analysis
    indexes_in = (
        wave_data["filtered_by_direction"]
        & wave_data[percentile_min_threshold]
        & ~np.isnan(wave_data[key_dir])
    )

    # getting start-end of storms IN
    # if last index is True, move it to False to have a "close" event
    if indexes_in[-1]:
        indexes_in[-1] = False
    # if first index is True, move it to False to have a "close" event
    if indexes_in[0]:
        indexes_in[0] = False

    start_end_index = np.array(indexes_in[1:].astype(int)) - np.array(
        indexes_in[0:-1].astype(int)
    )
    start_end_index = np.insert(start_end_index, 0, 0)
    start = start_end_index == 1
    end = start_end_index == -1
    dates_start_in = np.array(wave_data.index[start])
    dates_end_in = np.array(wave_data.index[end])

    # Storm out of analysis
    indexes_out = (
        ~wave_data["filtered_by_direction"]
        & wave_data[percentile_min_threshold]
        & ~np.isnan(wave_data[key_dir])
    )

    # if last index is True, move it to False to have a "close" event
    if indexes_out[-1]:
        indexes_out[-1] = False
    # if first index is True, move it to False to have a "close" event
    if indexes_out[0]:
        indexes_out[0] = False

    # Getting start-end of storms OUT
    start_end_index = np.array(indexes_out[1:].astype(int)) - np.array(
        indexes_out[0:-1].astype(int)
    )
    start_end_index = np.insert(start_end_index, 0, 0)
    start = start_end_index == 1
    end = start_end_index == -1
    dates_start_out = np.array(wave_data.index[start])
    dates_end_out = np.array(wave_data.index[end])

    return dates_start_in, dates_start_out, dates_end_in, dates_end_out


def read_storms_resume(storms_resume_file):
    storms_resume = pd.read_csv(storms_resume_file, sep=",")
    storms_resume["Hs_peak_date"] = pd.to_datetime(
        storms_resume["Hs_peak_date"], format="%Y-%m-%d %H:%M:%S"
    )
    storms_resume = storms_resume.set_index(storms_resume["Hs_peak_date"])
    storms_resume = storms_resume.sort_index()
    return storms_resume


def read_water_level(water_level_file):
    water_level = pd.DataFrame(pd.read_pickle(water_level_file))
    water_level = water_level.set_index(water_level["dates"])
    water_level = water_level.sort_index()
    water_level_daily = water_level.resample("1440T").mean()
    return water_level, water_level_daily
