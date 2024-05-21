import pandas as pd
import numpy as np
import re
from toolbiox.lib.common.math.set import merge_same_element_set
from toolbiox.lib.xuyuxing.map.base import haversine
from toolbiox.lib.common.os import cmd_run
from biogeoloc.cls import Accession, AccessionSet
import time


class GeneSysAccSet(AccessionSet):
    def __init__(self, name=None, date=None):
        date = date if date else time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())
        name = name if name else "GeneSys"

        default_ID_items = {
            'genesys_id': list,
            'pi_id': list,
            'is_id': list,
        }

        default_passport_items = {
            'local_adapted': bool,
        }

        super(GeneSysAccSet, self).__init__(name=name, date=date,
                                            default_ID_items=default_ID_items, default_passport_items=default_passport_items)

    def load(self, genesys_metadata_dir):
        # 载入数据目录
        genesys_df = load_genesys_dir(genesys_metadata_dir)
        # 根据ID之间的关系进行聚类
        id_map_group, gs2pi_dict, gs2is_dict = cluster_all_ids(genesys_df)
        # 解析重复的ID
        non_dup_df, coord_contradictory_list = parse_duplicated_ids(
            id_map_group, genesys_df, gs2pi_dict, gs2is_dict)
        # 保留那些有经纬度信息的数据
        georefed_genesys_df = non_dup_df[non_dup_df.lat.notnull(
        ) | non_dup_df.lon.notnull()]

        print("There are %d samples in Genesys, in which %d samples are non-duplicated (%d data have conflicted coord information) and %d samples have georeference information." %
              (len(genesys_df), len(non_dup_df), len(coord_contradictory_list), len(georefed_genesys_df)))

        # 生成Accession对象, 并添加到AccessionSet中
        uniq_num = 0
        uniq_id_format = "u%%0%dd" % len(str(len(non_dup_df)))
        for i in range(len(non_dup_df)):
            row = non_dup_df.iloc[i]
            pi_id_list = row.pi_id.split(",") if len(row.pi_id) > 0 else []
            is_id_list = row.is_id.split(",") if len(row.is_id) > 0 else []
            gs_id_list = row.gs_id.split(",") if len(row.gs_id) > 0 else []

            uniq_id = uniq_id_format % uniq_num
            s = Accession(uniq_id,
                          lat=row.lat,
                          lon=row.lon,
                          passport={"local_adapted": row.local_adapted},
                          sources=['Genesys'],
                          pi_id_list=pi_id_list,
                          is_id_list=is_id_list,
                          genesys_id_list=gs_id_list,
                          )
            uniq_num += 1

            self.add(s)


# PI_ID_format = r'PI ?\d+[A-Z]?'
# IS_ID_format = r'IS ?\d+[A-Z]?'
PI_ID_format = r'PI ?\d+'
IS_ID_format = r'IS ?\d+'


def load_genesys_dir(genesys_metadata_dir):

    genesys_core_file = genesys_metadata_dir + "/core.csv"
    genesys_names_file = genesys_metadata_dir + "/names.csv"
    cmd_string = "sed '1s/$/,/' geo.csv > geo_new.csv"
    cmd_run(cmd_string, cwd=genesys_metadata_dir, silence=True)
    genesys_geo_file = genesys_metadata_dir + "/geo_new.csv"

    genesys_core = pd.read_csv(genesys_core_file)
    genesys_core = genesys_core.replace({np.nan: None})
    genesys_names = pd.read_csv(genesys_names_file)
    genesys_names = genesys_names.replace({np.nan: None})
    genesys_geo = pd.read_csv(genesys_geo_file)
    genesys_geo = genesys_geo.replace({np.nan: None})

    # acceNumb
    genesysid2acceNumb = {}

    for i in range(len(genesys_core)):
        row = genesys_core.iloc[i]
        genesysid = row["genesysId"]
        acceNumb = row["acceNumb"]
        if genesysid in genesysid2acceNumb:
            print("Warning: genesysid {} is duplicated".format(genesysid))
        else:
            if acceNumb is not None:
                genesysid2acceNumb[genesysid] = acceNumb

    # sampStat
    genesysid2sampStat = {}

    for i in range(len(genesys_core)):
        row = genesys_core.iloc[i]
        genesysid = row["genesysId"]
        sampStat = int(row["sampStat"]) if row["sampStat"] else None
        if genesysid in genesysid2sampStat:
            print("Warning: genesysid {} is duplicated".format(genesysid))
        else:
            if sampStat is not None:
                genesysid2sampStat[genesysid] = sampStat

    # names
    genesysid2names = {}

    for i in range(len(genesys_names)):
        row = genesys_names.iloc[i]
        genesysid = row["genesysId"]
        name = row["name"]
        if name is not None:
            genesysid2names.setdefault(genesysid, []).append(name)

    for i in genesysid2names:
        genesysid2names[i] = list(set(genesysid2names[i]))

    # coords
    genesysid2coords = {}

    for i in range(len(genesys_geo)):
        row = genesys_geo.iloc[i]
        genesysid = row["genesysId"]
        lat = row["latitude"]
        lon = row["longitude"]
        if genesysid in genesysid2coords:
            print("Warning: row %d genesysid %s is duplicated" % (i, genesysid))
        else:
            if lat is not None:
                lat = float(lat)
            if lon is not None:
                lon = float(lon)

            if lat is not None and lon is not None:
                genesysid2coords[genesysid] = (lat, lon)

    genesysid_dict = {}
    for genesysid in genesysid2acceNumb:
        acceNumb = genesysid2acceNumb[genesysid] if genesysid in genesysid2acceNumb else None
        sampStat = genesysid2sampStat[genesysid] if genesysid in genesysid2sampStat else None
        names = ",".join(
            genesysid2names[genesysid]) if genesysid in genesysid2names else None
        coords = genesysid2coords[genesysid] if genesysid in genesysid2coords else None

        if acceNumb is None and sampStat is None and names is None and coords is None:
            continue

        genesysid_dict[genesysid] = {
            "acceNumb": acceNumb,
            "sampStat": sampStat,
            "names": names,
            "coords": coords
        }

    genesysid_df = pd.DataFrame(genesysid_dict).T

    return genesysid_df


def cluster_all_ids(genesys_df):

    id_map = []
    gs2pi_dict = {}
    gs2is_dict = {}
    for genesys_id in genesys_df.index:
        row = genesys_df.loc[genesys_id]

        acceNumb = [row.acceNumb] if row.acceNumb else []
        names = row.names.split(",") if row.names else []
        name_list = acceNumb + names

        pi_id_list = []
        is_id_list = []

        for name in name_list:
            # PI ID
            refinder = re.findall(PI_ID_format, name)
            for pi_id in refinder:
                pi_id = pi_id.replace(" ", "")
                pi_id_list.append(pi_id)

            # IS ID
            refinder = re.findall(IS_ID_format, name)
            for is_id in refinder:
                is_id = is_id.replace(" ", "")
                is_id_list.append(is_id)

        id_map.append([genesys_id])
        if len(pi_id_list):
            id_map.append(pi_id_list)
        if len(is_id_list):
            id_map.append(is_id_list)

        for i in pi_id_list:
            id_map.append([i, genesys_id])

        for j in is_id_list:
            id_map.append([j, genesys_id])

        gs2pi_dict[genesys_id] = pi_id_list
        gs2is_dict[genesys_id] = is_id_list

    id_map_group = merge_same_element_set(id_map)

    return id_map_group, gs2pi_dict, gs2is_dict


def if_local_adapted(gs_id_list, genesys_df):
    """
    https://www.genesys-pgr.org/documentation/basics
    4.1.4. Biological status of accession
    """
    local_adapted_flag = False
    for gs_id in gs_id_list:
        if genesys_df.loc[gs_id].sampStat:
            if genesys_df.loc[gs_id].sampStat <= 300:
                local_adapted_flag = True
                break
    return local_adapted_flag


def get_coord_from_gs_id_list(gs_id_list, genesys_df):
    for gs_id in gs_id_list:
        coord = genesys_df.loc[gs_id].coords
        if coord:
            return coord
    return None


def return_one_gs_group(gs_id_list, genesys_df, gs2pi_dict, gs2is_dict, exclude_id_list=[]):

    pi_id_list = []
    is_id_list = []

    for gs_id in gs_id_list:
        pi_id_list += gs2pi_dict[gs_id]
        is_id_list += gs2is_dict[gs_id]

    pi_id_list = list(set(pi_id_list))
    is_id_list = list(set(is_id_list))

    pi_id_list = [i for i in pi_id_list if i not in exclude_id_list]
    is_id_list = [i for i in is_id_list if i not in exclude_id_list]

    coord = get_coord_from_gs_id_list(gs_id_list, genesys_df)
    local_adapted_flag = if_local_adapted(gs_id_list, genesys_df)

    return {"pi_id": ",".join(pi_id_list), "is_id": ",".join(is_id_list), "gs_id": ",".join([str(i) for i in gs_id_list]), "lat": coord[0] if coord else None, "lon": coord[1] if coord else None, "local_adapted": local_adapted_flag}


def parse_duplicated_ids(id_map_group, genesys_df, gs2pi_dict, gs2is_dict):

    non_dup_dict = {}

    coord_contradictory_list = []

    for id_group in id_map_group:
        # if "PI570501" in id_group:
        #     break

        pi_id_list = []
        is_id_list = []
        gs_id_list = []

        for tmp_id in id_group:
            tmp_id = str(tmp_id)

            if tmp_id.startswith("PI"):
                pi_id_list.append(tmp_id)
            elif tmp_id.startswith("IS"):
                is_id_list.append(tmp_id)
            else:
                gs_id_list.append(tmp_id)

        gs_id_list = [int(i) for i in gs_id_list]

        # print(pi_id_list)
        # print(is_id_list)
        # print(gs_id_list)

        if len(gs_id_list) == 1:
            # 如果都指向同一个genesys_id
            gs_id = gs_id_list[0]
            non_dup_dict[gs_id] = return_one_gs_group(
                [gs_id], genesys_df, gs2pi_dict, gs2is_dict, exclude_id_list=[])
        elif len(gs_id_list) > 1:
            # 如果有多个genesys_id
            # 根据经纬度信息进行聚类
            gs_id_groups = []

            for i in gs_id_list:
                ci = genesys_df.loc[i].coords
                # print(i, ci)
                if ci is None:
                    continue
                else:
                    gs_id_groups.append([i])
                    for j in gs_id_list:
                        cj = genesys_df.loc[j].coords
                        if cj is None or i == j:
                            continue
                        if haversine(ci, cj) < 10:
                            # 10km以内的坐标认为是同一个坐标
                            gs_id_groups.append([i, j])

            gs_id_groups = merge_same_element_set(gs_id_groups)

            if len(gs_id_groups) <= 1:
                # 如果只有0个或一个有效坐标，那么所有id本质都是一个样品
                non_dup_dict[gs_id_list[0]] = return_one_gs_group(
                    gs_id_list, genesys_df, gs2pi_dict, gs2is_dict)
            else:
                # 如果有多个有效坐标，报告涉及的genesys_id数量
                coord_contradictory_list.append(gs_id_list)
                # gs_id_groups = sorted(
                #     gs_id_groups, key=lambda x: len(x), reverse=True)
                # used_pi_is_id_list = []
                # for gs_id_group in gs_id_groups:
                #     non_dup_dict[gs_id_group[0]] = return_one_gs_group(
                #         gs_id_group, genesys_df, gs2pi_dict, gs2is_dict, used_pi_is_id_list)
                #     used_pi_is_id_list.extend(
                #         non_dup_dict[gs_id_group[0]]["pi_id"].split(","))
                #     used_pi_is_id_list.extend(
                #         non_dup_dict[gs_id_group[0]]["is_id"].split(","))

    non_dup_df = pd.DataFrame(non_dup_dict).T

    return non_dup_df, coord_contradictory_list


if __name__ == "__main__":
    from biogeoloc.genesys import GeneSysAccSet

    genesys_metadata_dir = "/lustre/home/xuyuxing/Work/Jesse/local_adaptation/0.reference/Georeference/genesys"
    sorghum_genesys_set = GeneSysAccSet()
    sorghum_genesys_set.load(genesys_metadata_dir)
    sorghum_genesys_set.build_index()

    q_id = 'PI207841'
    u_id = sorghum_genesys_set.search(q_id)
    vars(sorghum_genesys_set.accession_dict[u_id])
