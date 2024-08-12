import json
import os
import sqlite3

from pyemmo.definitions import ROOT_DIR


def create_material_json(json_folder, mat_db, mode="sep"):

    if mat_db.split(".")[-1] != "db":
        raise TypeError("Not correct file type, please provide db file type")
    source_path = os.path.join(ROOT_DIR, "pyemmo", "script", "material")
    json_folder_path = os.path.join(source_path, json_folder)
    if not os.path.isdir(json_folder_path):
        os.makedirs(json_folder_path)

    mat_dbPath = os.path.join(source_path, mat_db)
    connection = sqlite3.connect(mat_dbPath)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Material;")
    mat_tbl = cursor.fetchall()

    if mode == "all":
        # create 1 json for all materials
        mat_dict = {}
        for row in mat_tbl:
            # print(row)
            mat_dict[row[0]] = {}
            mat_dict[row[0]]["name"] = row[1]
            mat_dict[row[0]]["conductivity"] = row[2]
            mat_dict[row[0]]["relPermeability"] = row[3]
            mat_dict[row[0]]["remanence"] = row[4]
            if row[5] == "linear":
                mat_dict[row[0]]["linear"] = True
            else:
                mat_dict[row[0]]["linear"] = False
            # Create BH Curve for default temperature
            mat_dict[row[0]]["BHCurve"] = {}
            cursor.execute("SELECT * FROM BH_CURVE WHERE ID = %d" % row[0])
            bh_data = cursor.fetchall()
            cursor.execute("SELECT DISTINCT Temp from BH_CURVE WHERE ID = %d" % row[0])
            temp_list = cursor.fetchall()
            for temp in temp_list:
                if temp[0] == "no information":
                    temp_key = "default"
                else:
                    temp_key = temp[0]
                mat_dict["BHCurve"][temp_key] = [
                    [row[1], row[2]] for row in bh_data if row[3] == temp[0]
                ]
                # mat_dict[row[0]]["BHCurve"][temp_key] = {}
                # mat_dict[row[0]]["BHCurve"][temp_key]["H"] = [row[1] for row in bh_data if row[3] == temp[0]]
                # mat_dict[row[0]]["BHCurve"][temp_key]["B"] = [row[2] for row in bh_data if row[3] == temp[0]]
            with open(os.path.join(json_folder_path, f"{row[1]}.json"), "w") as file:
                json.dump(mat_dict, file, indent="\t")

        with open(os.path.join(source_path, f"material_db_all.json"), "w") as file:
            json.dump(mat_dict, file, indent="\t")
    else:
        # create separate json for each material
        for row in mat_tbl:
            mat_dict = {}
            mat_dict["ID"] = row[0]
            mat_dict["name"] = row[1]
            mat_dict["conductivity"] = row[2]
            mat_dict["relPermeability"] = row[3]
            mat_dict["remanence"] = row[4]
            # mat_dict["BHCurve_type"] = row[5]
            if row[5] == "linear":
                mat_dict["linear"] = True
            else:
                mat_dict["linear"] = False
            # Create BH Curve for default temperature
            mat_dict["BHCurve"] = {}
            cursor.execute("SELECT * FROM BH_CURVE WHERE ID = %d" % row[0])
            bh_data = cursor.fetchall()
            cursor.execute("SELECT DISTINCT Temp from BH_CURVE WHERE ID = %d" % row[0])
            temp_list = cursor.fetchall()
            for temp in temp_list:
                if temp[0] == "no information":
                    temp_key = "default"
                else:
                    temp_key = temp[0]
                mat_dict["BHCurve"][temp_key] = [
                    [row[1], row[2]] for row in bh_data if row[3] == temp[0]
                ]
                # mat_dict["BHCurve"][temp_key]["H"] = [row[1] for row in bh_data if row[3] == temp[0]]
                # mat_dict["BHCurve"][temp_key]["B"] = [row[2] for row in bh_data if row[3] == temp[0]]
            with open(os.path.join(json_folder_path, f"{row[1]}.json"), "w") as file:
                json.dump(mat_dict, file, indent="\t")


if __name__ == "__main__":
    create_material_json("material_json", "Material_new.db")
