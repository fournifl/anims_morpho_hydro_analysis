import pickle

import numpy as np
from georef.operators import Georef

from anim.core.geo import get_transects_pix_coordinates


def get_grid_z_of_beach_profiles_and_slopes(
    slope_results, method_fitting, order_of_done_fitting=3
):
    # gather individual beach profiles in a grid
    z_fitting_method = f"z_{method_fitting}"
    slope_fitting_method = f"slope_{method_fitting}_regular_x"
    regular_sl_cross_sh_d = slope_results["regular_cross_sh_d"]
    grid_z_profiles = np.zeros(
        (regular_sl_cross_sh_d.size, len(slope_results["dates"]))
    )
    grid_z_slopes = np.zeros((regular_sl_cross_sh_d.size, len(slope_results["dates"])))
    for i in range(len(slope_results["dates"])):
        if z_fitting_method == "z_spline_fitting":
            grid_z_profiles[:, i] = slope_results[z_fitting_method][i]
        else:
            grid_z_profiles[:, i] = slope_results[z_fitting_method][i][
                f"order_{order_of_done_fitting}"
            ]
            grid_z_slopes[:, i] = slope_results[slope_fitting_method][i][
                f"order_{order_of_done_fitting}"
            ]

    return grid_z_profiles, grid_z_slopes


def get_beach_profiles_at_transects(profile_mvt_files, transects, f_cam_params):
    beach_profiles = {}
    beach_slopes = {}
    mesh_time = {}
    mesh_cross_sh_d = {}
    slope_at_bmme = {}
    slope_at_nm = {}
    slope_at_pmme = {}
    method_fitting = "weighted_fitting"
    time = {}
    transect_start_end_coords = {}

    for i, transect in enumerate(transects):
        if profile_mvt_files[i] is not None:
            with open(profile_mvt_files[i], "rb") as file:
                slope_results = pickle.load(file)
            mesh_time[transect], mesh_cross_sh_d[transect] = np.meshgrid(
                slope_results["dates"], slope_results["regular_cross_sh_d"]
            )
            beach_profiles[transect], beach_slopes[transect] = (
                get_grid_z_of_beach_profiles_and_slopes(
                    slope_results,
                    method_fitting=method_fitting,
                    order_of_done_fitting=3,
                )
            )
            time[transect] = slope_results["dates"]
            slope_at_bmme[transect] = [
                slope_results[f"slope_{method_fitting}_at_bmme_nm_pmme"][i][
                    f"order_{3}_at_bmme"
                ]
                for i in range(len(slope_results["dates"]))
            ]
            slope_at_nm[transect] = [
                slope_results[f"slope_{method_fitting}_at_bmme_nm_pmme"][i][
                    f"order_{3}_at_nm"
                ]
                for i in range(len(slope_results["dates"]))
            ]
            slope_at_pmme[transect] = [
                slope_results[f"slope_{method_fitting}_at_bmme_nm_pmme"][i][
                    f"order_{3}_at_pmme"
                ]
                for i in range(len(slope_results["dates"]))
            ]
            transect_start_end_coords[transect] = slope_results[
                "transect_start_end_coords"
            ]

    # get georef parameters
    georef_params = Georef.from_param_file(f_cam_params)
    # get transects' pix coordinates
    transect_pix = get_transects_pix_coordinates(
        georef_params, transect_start_end_coords
    )

    bmme = slope_results["bmme"]
    nm = slope_results["nm"]
    pmme = slope_results["pmme"]
    return (
        transect_pix,
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
    )
