from anim.core.hydro import (
    get_storm_dates_in_out,
    read_csv_waves,
    read_storms_resume,
    read_water_level,
)
from anim.core.img import read_img
from anim.core.morpho import get_beach_profiles_at_transects


def plot(
    img,
    wave_data,
    water_level,
    dates_start_in,
    dates_start_out,
    dates_end_in,
    dates_end_out,
    storms_resume,
    beach_profiles,
    mesh_time,
    mesh_cross_sh_d,
    height_ratios,
    variables_to_plot,
):
    # calculate number of subplots
    n = sum(variables_to_plot.values())




def run(
    input_directory_a,
    waves,
    f_water_level,
    storms_resume_file,
    transects,
    transects_to_plot,
    profile_mvt_files,
    output_dir,
    variables_to_plot,
    height_ratios,
):
    # list of camera images
    ls_imgs = sorted(input_directory_a.glob("*.jpg"))

    # read wave data
    wave_data, thresholds = read_csv_waves(waves)

    # get storm dates whose direction can either impact beach, or not
    dates_start_in, dates_start_out, dates_end_in, dates_end_out = (
        get_storm_dates_in_out(wave_data, waves.percentile_min_threshold, waves.key_dir)
    )

    # Reading storms resume file
    if storms_resume_file is not None:
        storms_resume = read_storms_resume(storms_resume_file)

    # read water level
    water_level, water_level_daily = read_water_level(f_water_level)

    # Load wavecams' beach profiles
    if profile_mvt_files is not None:
        (
            beach_profiles,
            beach_slopes,
            mesh_time,
            mesh_cross_sh_d,
            time,
            slope_at_bmme,
            slope_at_nm,
            slope_at_pmme,
            bmme,
            nm,
            pmme,
        ) = get_beach_profiles_at_transects(profile_mvt_files, transects)

    # loop though images
    for f_img in ls_imgs:
        img, date_img = read_img(f_img)
        plot(
            img,
            wave_data,
            water_level,
            dates_start_in,
            dates_start_out,
            dates_end_in,
            dates_end_out,
            storms_resume,
            beach_profiles,
            mesh_time,
            mesh_cross_sh_d,
            height_ratios,
            variables_to_plot,
        )
