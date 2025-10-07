import matplotlib.pyplot as plt

from anim.core.hydro import (
    get_storm_dates_in_out,
    read_csv_waves,
    read_storms_resume,
    read_water_level,
)
from anim.core.img import get_list_of_imgs, read_img
from anim.core.morpho import get_beach_profiles_at_transects


def plot_vertical_lines_over_storms(
    ax,
    dates_start_in,
    dates_end_in,
    dates_start_out,
    dates_end_out,
    angle_min_threshold,
    angle_max_threshold,
    legend=False,
):
    # Lines over storms between angle min,max thresholds
    label = f"storm direction in [{angle_min_threshold}, {angle_max_threshold}] °N"
    for ii in range(dates_end_in.__len__()):
        if (ii == 0) * legend:
            ax.axvspan(
                dates_start_in[ii],
                dates_end_in[ii],
                alpha=0.1,
                color="salmon",
                label=label,
            )
        else:
            ax.axvspan(dates_start_in[ii], dates_end_in[ii], alpha=0.1, color="salmon")

    # Others
    label = f"storm direction out of [{angle_min_threshold}, {angle_max_threshold}] °N"
    for ii in range(dates_end_out.__len__()):
        if (ii == 0) * legend:
            ax.axvspan(
                dates_start_out[ii],
                dates_end_out[ii],
                alpha=0.1,
                color="aqua",
                label=label,
            )
        else:
            ax.axvspan(dates_start_out[ii], dates_end_out[ii], alpha=0.1, color="aqua")


def plot_img(axs, img, date_img, transect, transect_pix, variables_to_plot_chosen):
    if "cam_a_img" in variables_to_plot_chosen:
        axs["cam_a_img"].imshow(img)
        axs["cam_a_img"].plot(
            [x[0] for x in transect_pix[transect]],
            [x[1] for x in transect_pix[transect]],
            "r",
            label=f"transect {transect}",
        )
        axs["cam_a_img"].axis("off")
        axs["cam_a_img"].text(
            0.35,
            0.85,
            f"{date_img.strftime('%Y/%m/%d %H:%M')}",
            transform=axs["cam_a_img"].transAxes,
            fontsize=22,  # Taille de police
            color="white",  # Couleur du texte
            fontweight="bold",  # Style gras
            bbox=dict(  # Encadré autour du texte
                boxstyle="round,pad=0.4",  # Forme et espacement interne
                facecolor="royalblue",  # Couleur de fond
                edgecolor="black",  # Couleur de la bordure
                alpha=0.7,  # Transparence
            ),
        )
        axs["cam_a_img"].legend()


def plot_water_level(axs, water_level, start, end, variables_to_plot_chosen, date_img):
    if "water_level" in variables_to_plot_chosen:
        axs["water_level"].axvline(x=date_img, color="k", label="image's date")
        axs["water_level"].plot(
            water_level.index,
            water_level["water_level"],
            linestyle="-",
            linewidth=1,
            markersize=0.01,
            label="Water level",
        )
        axs["water_level"].set_xlim([start, end])
        axs["water_level"].set_xticks([])
        axs["water_level"].grid(color="lightgray", linestyle="-.", linewidth=0.5)
        axs["water_level"].yaxis.set_tick_params(labelsize=16)
        axs["water_level"].set_ylabel("water level (m IGN69)", fontsize=16)
        axs["water_level"].legend(loc="upper right", fontsize=18)
        return axs


def plot_hs(
    axs, wave_data, waves, start, end, thresholds, variables_to_plot_chosen, date_img
):
    if "hs" in variables_to_plot_chosen:
        axs["hs"].axvline(x=date_img, color="k")
        axs["hs"].plot(
            wave_data.index,
            wave_data[waves.key_hs],
            linestyle="-",
            color="black",
            linewidth=1,
            markersize=0.01,
            label="Hs",
            alpha=0.5,
        )
        axs["hs"].set_xlim([start, end])
        axs["hs"].set_xticks([])
        axs["hs"].grid(color="lightgray", linestyle="-.", linewidth=0.5)
        axs["hs"].legend(loc="upper right", fontsize=18)
        axs["hs"].set_ylabel("Hs (m)", fontsize=16)

        # Dots over thresholds
        for ii in range(thresholds.shape[0]):
            aux = "p_" + str(thresholds["percentile"][ii])
            indexes = wave_data[aux]
            axs["hs"].plot_date(
                wave_data.index[indexes],
                wave_data[waves.key_hs][indexes],
                color=thresholds["colors"][ii],
                linewidth=1.5,
                markersize=1.5,
                label="_nolegend_",
            )

            axs["hs"].hlines(
                thresholds["threshold"][ii],
                wave_data.index[0],
                wave_data.index[-1],
                linestyles="--",
                linewidth=0.5,
                colors=thresholds["colors"][ii],
                label=aux,
            )
        axs["hs"].yaxis.set_tick_params(labelsize=16)
        return axs


def plot_tp(
    axs, wave_data, waves, start, end, thresholds, variables_to_plot_chosen, date_img
):
    if "tp" in variables_to_plot_chosen:
        axs["tp"].axvline(
            x=date_img,
            color="k",
        )
        axs["tp"].plot(
            wave_data.index,
            wave_data[waves.key_per],
            linestyle="-",
            color="black",
            linewidth=1,
            markersize=0.01,
            label="Tp",
            alpha=0.5,
        )
        # Dots over thresholds
        for ii in range(thresholds.shape[0]):
            aux = "p_" + str(thresholds["percentile"][ii])
            indexes = wave_data[aux]
            axs["tp"].plot_date(
                wave_data.index[indexes],
                wave_data[waves.key_per][indexes],
                color=thresholds["colors"][ii],
                linewidth=1.5,
                markersize=1.5,
                label="_nolegend_",
            )

        axs["tp"].set_xlim([start, end])
        axs["tp"].set_xticks([])
        axs["tp"].grid(color="lightgray", linestyle="-.", linewidth=0.5)
        axs["tp"].legend(loc="upper right", fontsize=18)
        axs["tp"].yaxis.set_tick_params(labelsize=16)
        axs["tp"].set_ylabel("Tp (s)", fontsize=16)
        return axs


def plot_dir(
    axs, wave_data, waves, start, end, thresholds, variables_to_plot_chosen, date_img
):
    if "dir" in variables_to_plot_chosen:
        axs["dir"].axvline(x=date_img, color="k")
        axs["dir"].plot(
            wave_data.index,
            wave_data[waves.key_dir],
            linestyle="-",
            color="black",
            linewidth=1,
            markersize=0.01,
            label="Dp",
            alpha=0.5,
        )

        # Dots over thresholds
        for ii in range(thresholds.shape[0]):
            aux = "p_" + str(thresholds["percentile"][ii])
            indexes = wave_data[aux]
            axs["dir"].plot_date(
                wave_data.index[indexes],
                wave_data[waves.key_dir][indexes],
                color=thresholds["colors"][ii],
                linewidth=1.5,
                markersize=1.5,
                label="_nolegend_",
            )
        axs["dir"].set_xlim([start, end])
        axs["dir"].set_xticks([])
        axs["dir"].grid(color="lightgray", linestyle="-.", linewidth=0.5)
        axs["dir"].legend(loc="upper right", fontsize=18)
        axs["dir"].yaxis.set_tick_params(labelsize=16)
        axs["dir"].set_ylabel("Dir (°N)", fontsize=16)
        return axs


def plot_beach_profile(
    fig,
    axs,
    beach_profiles,
    mesh_time,
    mesh_cross_sh_d,
    transect,
    start,
    end,
    variables_to_plot_chosen,
    date_img,
):
    if "beach_profile" in variables_to_plot_chosen:
        # plot beach profiles
        axs["beach_profile"].axvline(x=date_img, color="k")
        pcol = axs["beach_profile"].pcolor(
            mesh_time[transect],
            mesh_cross_sh_d[transect],
            beach_profiles[transect],
            shading="auto",
            cmap="terrain",
            vmin=-3,
            vmax=3.5,
        )
        axs["beach_profile"].set_xlim([start, end])
        axs["beach_profile"].set_ylim([10, 55])
        axs["beach_profile"].set_ylabel("cross shore distance (m)", fontsize=16)
        # colorbar
        cbar = fig.colorbar(pcol, ax=axs["beach_profile"], aspect=10)
        cbar.set_label(
            f"Profile height at {transect} (m IGN69)", rotation=90, fontsize=18
        )
        # contours of beach profiles
        ctrs = axs["beach_profile"].contour(
            mesh_time[transect],
            mesh_cross_sh_d[transect],
            beach_profiles[transect],
            levels=[-1, -0.5, 0.5, 1, 2],
            linewidths=1.5,
            colors="dimgray",
        )
        axs["beach_profile"].clabel(
            ctrs, ctrs.levels, inline=True, fmt="%i m", fontsize=18
        )
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=14)
        return axs


def plot(
    start,
    end,
    ls_imgs,
    waves,
    wave_data,
    water_level,
    dates_start_in,
    dates_start_out,
    dates_end_in,
    dates_end_out,
    storms_resume,
    beach_profiles,
    transect_pix,
    mesh_time,
    mesh_cross_sh_d,
    height_ratios,
    variables_to_plot,
    transects_to_plot,
    output_dir,
    angle_min_landward,
    angle_max_landward,
    thresholds,
):
    # variables to plot
    variables_to_plot_chosen = [
        key for key in variables_to_plot.keys() if variables_to_plot[key]
    ]

    # subplots' names
    subplots_names = [[item] for item in variables_to_plot_chosen]

    # height ratios
    height_ratios = [height_ratios[key] for key in variables_to_plot_chosen]

    # loop though images
    for transect in transects_to_plot:
        output_dir_transect = output_dir / "intertidal_vs_hydro" / transect
        output_dir_transect.mkdir(parents=True, exist_ok=True)
        for f_img in ls_imgs:
            img, date_img = read_img(f_img)

            # create subplot
            fig, axs = plt.subplot_mosaic(
                subplots_names,
                layout="constrained",
                gridspec_kw={"height_ratios": height_ratios},
                figsize=(22, 16),
            )

            # img
            plot_img(
                axs, img, date_img, transect, transect_pix, variables_to_plot_chosen
            )

            # water level
            plot_water_level(
                axs, water_level, start, end, variables_to_plot_chosen, date_img
            )

            # hs
            plot_hs(
                axs,
                wave_data,
                waves,
                start,
                end,
                thresholds,
                variables_to_plot_chosen,
                date_img,
            )

            # tp
            plot_tp(
                axs,
                wave_data,
                waves,
                start,
                end,
                thresholds,
                variables_to_plot_chosen,
                date_img,
            )

            # dir
            plot_dir(
                axs,
                wave_data,
                waves,
                start,
                end,
                thresholds,
                variables_to_plot_chosen,
                date_img,
            )

            # beach profile
            plot_beach_profile(
                fig,
                axs,
                beach_profiles,
                mesh_time,
                mesh_cross_sh_d,
                transect,
                start,
                end,
                variables_to_plot_chosen,
                date_img,
            )

            # vertical lines over storms
            for var in variables_to_plot_chosen:
                if var != "cam_a_img":
                    plot_vertical_lines_over_storms(
                        axs[var],
                        dates_start_in,
                        dates_end_in,
                        dates_start_out,
                        dates_end_out,
                        angle_min_landward,
                        angle_max_landward,
                        legend=True,
                    )
            print(f_img.name)
            fig.savefig(output_dir_transect / f_img.name)
            plt.close("all")


def run(
    input_directory_a,
    cam_params_path,
    waves,
    f_water_level,
    storms_resume_file,
    transects,
    transects_to_plot,
    profile_mvt_files,
    output_dir,
    variables_to_plot,
    height_ratios,
    start,
    end,
):
    # list of camera images
    ls_imgs = get_list_of_imgs(input_directory_a, start, end)

    # read wave data
    wave_data, thresholds = read_csv_waves(waves)

    # get storm dates whose direction can either impact beach, or not
    dates_start_in, dates_start_out, dates_end_in, dates_end_out = (
        get_storm_dates_in_out(
            wave_data, waves.wave_height_notable_percentile_min_threshold, waves.key_dir
        )
    )

    # Reading storms resume file
    if storms_resume_file is not None:
        storms_resume = read_storms_resume(storms_resume_file)

    # read water level
    water_level, water_level_daily = read_water_level(f_water_level)

    # Load wavecams' beach profiles
    if profile_mvt_files is not None:
        (
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
        ) = get_beach_profiles_at_transects(
            profile_mvt_files, transects, cam_params_path
        )

    # plot
    plot(
        start,
        end,
        ls_imgs,
        waves,
        wave_data,
        water_level,
        dates_start_in,
        dates_start_out,
        dates_end_in,
        dates_end_out,
        storms_resume,
        beach_profiles,
        transect_pix,
        mesh_time,
        mesh_cross_sh_d,
        height_ratios,
        variables_to_plot,
        transects_to_plot,
        output_dir,
        waves.angle_min_landward,
        waves.angle_max_landward,
        thresholds,
    )
