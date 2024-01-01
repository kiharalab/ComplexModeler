

import os
import sys

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
    if params['contour']<0:
        #change contour level to 0 and increase all the density
        from CryoREAD.data_processing.map_utils import increase_map_density
        cur_map_path = increase_map_density(cur_map_path,os.path.join(save_path,map_name+"_increase.mrc"),params['contour'])
        params['contour']=0
    from CryoREAD.data_processing.map_utils import segment_map
    cur_new_map_path = os.path.join(save_path,map_name+"_segment.mrc")
    cur_map_path = segment_map(cur_map_path,cur_new_map_path,contour=0) #save the final prediction prob array space
    return save_path,cur_map_path

if __name__ == "__main__":
    params = argparser()
    save_path,cur_map_path = set_up_envrionment(params)
    #parse fasta files to determine if run fasta CryoREAD version or not
    from ops.fasta_utils import read_fasta,write_drna_fasta,write_fasta
    fasta_path = os.path.abspath(params['P'])
    chain_dict,dna_id_list = read_fasta(fasta_path)
    #generate a dna fasta file for dna/rna
    if len(dna_id_list)!=0:
        dna_fasta_path = os.path.join(save_path,"DRNA.fasta")
        dna_fasta_path = write_drna_fasta(dna_fasta_path,chain_dict,dna_id_list)
    #first run DNA/RNA predictions
    running_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(running_dir)
    cryoread_script = os.path.join(os.getcwd(),"CryoREAD")
    best_model_path = os.path.join(cryoread_script,"best_model")
    cryoread_script = os.path.join(cryoread_script,"main.py")
    half_contour = params['contour']/2
    command_line=f"python3 %s --mode=0 -F={cur_map_path} -M {best_model_path} " \
                 f"--contour={half_contour} " \
                 f"--batch_size=4 --prediction_only --output {save_path} "%(cryoread_script)
    os.system(command_line)
    protein_map_path = os.path.join(save_path,"mask_protein.mrc")
    if not os.path.exists(protein_map_path):
        print("protein detection failed")
        sys.exit(1)
    #run diffmodeler, which also mostly used gpu
    protein_fasta_path = os.path.join(save_path,"protein.fasta")
    protein_fasta_path = write_fasta(protein_fasta_path,chain_dict,[key for key in chain_dict.keys() if key not in dna_id_list])

    #run diffmodeler
    diffmodeler_script = os.path.join(os.getcwd(),"DiffModeler")
    diffmodeler_script = os.path.join(diffmodeler_script,"main.py")
    diffmodeler_config = os.path.join(os.getcwd(),"DiffModeler")
    diffmodeler_config = os.path.join(diffmodeler_config,"config")
    diffmodeler_config = os.path.join(diffmodeler_config,"diffmodeler.json")
    resolution = params['resolution']
    protein_cif = os.path.join(save_path,"DiffModeler.cif")
    if not os.path.exists(protein_cif):
        #specifically designed for server
        command_line=f"python3 {diffmodeler_script} --mode=2 -F={protein_map_path} -P={protein_fasta_path} " \
                 f"--config={diffmodeler_config} --contour={half_contour}  " \
                 f"--resolution={resolution} --output {save_path}"
        os.system(command_line)

    if not os.path.exists(protein_cif):
        print("protein structure modeling DiffModeler failed")
        sys.exit(1)
    if params['gpu_only']:
        print("GPU part finished")
        sys.exit(1)
    if len(dna_id_list)!=0:
        command_line=f"python3 %s --mode=0 -F={cur_map_path} -P={dna_fasta_path}" \
                 f"--contour={half_contour} " \
                 f"--batch_size=4  --output {save_path} --rule_soft=0 " \
                     f"--resolution={resolution} --thread 4 "%(cryoread_script)

    else:
        command_line=f"python3 %s --mode=0 -F={cur_map_path} " \
                 f"--contour={half_contour} " \
                 f"--batch_size=4  --output {save_path}  --no_seqinfo " \
                     f"--resolution={resolution}  "%(cryoread_script)
    if params['refine']:
        #refine the DNA/RNA structure
        command_line+=" --refine"
    os.system(command_line)
    if params['refine']:
        cryoread_pdb_path = os.path.join(save_path,"CryoREAD.pdb")
    else:
        cryoread_pdb_path = os.path.join(save_path,"CryoREAD_norefine.pdb")
    from ops.pdb_utils import pdb2cif,reindex_cif
    dna_cif_path = os.path.join(save_path,"CryoREAD.cif")
    if os.path.exists(cryoread_pdb_path):
        pdb2cif(cryoread_pdb_path,dna_cif_path)

    #combine two cif file
    from ops.os_operation import cat_file
    combine_file = os.path.join(save_path,"protein_drna.cif")
    if os.path.exists(dna_cif_path):
        cat_file([protein_cif,dna_cif_path],combine_file)
    else:
        cat_file([protein_cif],combine_file)
    final_output = os.path.join(save_path,"ComplexModeler.cif")
    reindex_cif(combine_file,final_output)
    print("Final output kept in %s, Enjoy!"%final_output)

