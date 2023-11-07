

import os
from ops.argparser import argparser
from ops.os_operation import mkdir
import time
import shutil
def init_save_path(origin_map_path):
    save_path = os.path.join(os.getcwd(), 'Predict_Result')
    mkdir(save_path)
    map_name = os.path.split(origin_map_path)[1].replace(".mrc", "")
    map_name = map_name.replace(".map", "")
    map_name = map_name.replace("(","").replace(")","")
    save_path = os.path.join(save_path, map_name)
    mkdir(save_path)
    return save_path,map_name
def set_up_envrionment(params):
    if params['resolution']>20:
        print("maps with %.2f resolution is not supported! We only support maps with resolution 0-20A!"%params['resolution'])
        exit()
    gpu_id = params["gpu"]
    if gpu_id is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id
    cur_map_path = os.path.abspath(params['F'])
    if cur_map_path.endswith(".gz"):
        from ops.os_operation import unzip_gz
        cur_map_path = unzip_gz(cur_map_path)

    if params['output'] is None:
        save_path,map_name = init_save_path(cur_map_path)
    else:
        save_path=params['output']
        map_name="input"
        mkdir(save_path)
    save_path = os.path.abspath(save_path)
    from CryoREAD.data_processing.Unify_Map import Unify_Map
    cur_map_path = Unify_Map(cur_map_path,os.path.join(save_path,map_name+"_unified.mrc"))
    from CryoREAD.data_processing.Resize_Map import Resize_Map
    cur_map_path = Resize_Map(cur_map_path,os.path.join(save_path,map_name+".mrc"))
    from CryoREAD.data_processing.map_utils import segment_map
    cur_new_map_path = os.path.join(save_path,map_name+"_segment.mrc")
    cur_map_path = segment_map(cur_map_path,cur_new_map_path,contour=0) #save the final prediction prob array space
    return save_path,cur_map_path

if __name__ == "__main__":
    params = argparser()
    save_path,cur_map_path = set_up_envrionment(params)
    #parse fasta files to determine if run fasta CryoREAD version or not
    from ops.fasta_utils import read_fasta,write_drna_fasta
    fasta_path = os.path.abspath(params['P'])
    chain_dict,dna_id_list = read_fasta(fasta_path)
    #generate a dna fasta file for dna/rna
    if len(dna_id_list)!=0:
        dna_fasta_path = os.path.join(save_path,"DRNA.fasta")
        dna_fasta_path = write_drna_fasta(dna_fasta_path,chain_dict,dna_id_list)
    #first run predictions

