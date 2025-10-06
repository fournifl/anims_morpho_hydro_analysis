from anim.core import intertidal_vs_hydro


def main(conf):
    if conf.app_name == "anim_intertidal_vs_hydro":
        intertidal_vs_hydro.run(
            conf.input_directory_a,
            conf.waves,
            conf.water_level,
            conf.storms_resume_file,
            conf.transects,
            conf.transects_to_plot,
            conf.profile_mvt_files,
            conf.output_dir,
            conf.variables_to_plot,
            conf.height_ratios,
        )

    return
