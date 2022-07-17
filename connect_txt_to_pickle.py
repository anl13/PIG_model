# This file shows how the txt files are packed to pickle file. 

import numpy as np 
import pickle 
from scipy.sparse import csc_matrix 

def combine_pickle():
    # read core data
    folder = "H:/examples/PIG_model/full_txt_files/"
    faces_vert = np.loadtxt(folder + "faces_vert.txt").astype(np.int64)
    faces_tex = np.loadtxt(folder + "faces_tex.txt").astype(np.int64)
    parents = np.loadtxt(folder + "parents.txt").astype(np.int64).squeeze()
    t_pose_joints = np.loadtxt(folder + "t_pose_joints.txt")
    textures = np.loadtxt(folder + "textures.txt")
    vertices = np.loadtxt(folder + "vertices.txt")

    J = np.zeros([62, 11239], np.float32)
    J_data = np.loadtxt(folder + "/J_regressor.txt")
    for k in range(J_data.shape[0]): 
        j = int(J_data[k][0])
        v = int(J_data[k][1])
        w = J_data[k][2] 
        J[j,v] = w 
    J_sparse = csc_matrix(J) 
    # To get J from J_sparse, just use J_sparse.todense() 

    weights = np.zeros([62, 11239])
    w_data = np.loadtxt(folder + "skinning_weights.txt") 
    for k in range(w_data.shape[0]): 
        j = int(w_data[k][0])
        v = int(w_data[k][1])
        w = w_data[k][2]
        weights[j,v] = w 
    weight_sparse = csc_matrix(weights) 

    data_dict = {
        "faces_vert": faces_vert,
        "faces_tex": faces_tex, 
        "parents": parents,
        "t_pose_joints": t_pose_joints,
        "textures": textures, 
        "vertices" : vertices, 
        "J_regressor": J_sparse, 
        "skinning_weights": weight_sparse 
    } 
    with open("pkl_files/PIG_core.pkl", 'wb') as f: 
        pickle.dump(data_dict, f) 
    
    body_parts = np.loadtxt(folder + "/body_parts.txt").astype(np.int64).squeeze() 
    reduced_ids = np.loadtxt(folder + "/reduced_ids.txt").astype(np.int64).squeeze() 
    reduced_faces = np.loadtxt(folder + "reduced_faces.txt").astype(np.int64)
    sym = np.loadtxt(folder + "sym.txt").astype(np.int64).squeeze() 
    body_part_defs = [
        "NOT_BODY", # not used. 
        "MAIN_BODY",
        "HEAD",
        "L_EAR",
        "R_EAR",
        "L_F_LEG",
        "R_F_LEG",
        "L_B_LEG",
        "R_B_LEG",
        "TAIL",
        "JAW",
        "NECK",
        "OTHERS"
    ]
    data_dict.update({
        "body_parts": body_parts, 
        "body_part_defs": body_part_defs, 
        "reduced_ids": reduced_ids, 
        "reduced_faces": reduced_faces, 
        "sym": sym
    })

    with open("pkl_files/PIG_full.pkl", 'wb') as f: 
        pickle.dump(data_dict, f) 

if __name__ == "__main__":
    combine_pickle() 

