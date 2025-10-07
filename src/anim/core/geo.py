def world_2_pix(xyz, georef_params):
    geo_local = georef_params.local_srs.m_l_w @ xyz
    u, v = georef_params.geo2pix(geo_local)
    return u, v


def get_transects_pix_coordinates(georef_params, transects_start_end_coords):
    transect_pix = {}
    # TODO a revoir, ça me donne des stacks en biais
    # import numpy as np
    #
    # for transect in transects_start_end_coords.keys():
    #     coords = np.squeeze(transects_start_end_coords[transect])
    #     x = coords[:, 0]
    #     y = coords[:, 1]
    #     z = np.zeros_like(x)
    #     xyz = np.vstack([x, y, z])
    #     u, v = world_2_pix(xyz, georef_params)
    #     transect_pix[transect] = (u, v)
    transect_pix["T3"] = [[541, 1621], [1290, 785]]
    transect_pix["T4"] = [[3633, 1491], [3036, 958]]

    return transect_pix
