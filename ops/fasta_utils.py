

from collections import  defaultdict

def read_fasta(input_fasta_path):
    AA20='ARNDCQEGHILKMFPSTWYV'
    dnarna="AUTCG"
    chain_dict=defaultdict(list)#key: chain_list, value: nuc sequence
    current_id=None

    tmp_chain_list=[chr(i) for i in range(ord('A'), ord('Z') + 1)]  # uppercase letters
    tmp_chain_list.extend([chr(i) for i in range(ord('a'), ord('z') + 1)])  # lowercase letters
    dna_id_list=[]
    with open(input_fasta_path,'r', encoding='utf-8-sig') as file:
        for line in file:
            if line[0]==">":
                current_id = line.strip("\n")
                current_id = current_id.replace(">","")
                current_id = current_id.replace(" ","")

            else:
                line=line.strip("\n").replace(" ","")
                for item in line:
                    if item not in AA20 and item not in dnarna:
                        continue
                    chain_dict[current_id].append(item)
    #check the chain id
    for key in chain_dict:
        current_list = chain_dict[key]
        current_list = set(current_list)
        if len(current_list)<=10:
            check_flag=False
            for item in current_list:
                if item not in dnarna:
                    check_flag=True
            if check_flag:
                print("skip invalid sequence %s"%key)
                print("including element: ",current_list)
            else:
                dna_id_list.append(key)

    print("read chain info from fasta:",chain_dict)
    return chain_dict,dna_id_list

def write_drna_fasta(dna_fasta_path,chain_dict,dna_id_list):
    with open(dna_fasta_path,'w') as wfile:
        for key in chain_dict:
            if key not in dna_id_list:
                continue
            id_list = key.split(",")
            for chain_id in id_list:
                if chain_id=="":
                    continue
                wfile.write(">%s\n"%chain_id)
                fasta_list = chain_dict[key]
                for item in fasta_list:
                    wfile.write(item)
                wfile.write("\n")
    return dna_fasta_path

def write_fasta(dna_fasta_path,chain_dict,dna_id_list):
    with open(dna_fasta_path,'w') as wfile:
        for key in chain_dict:
            if key not in dna_id_list:
                continue
            wfile.write(">%s\n"%key)
            fasta_list = chain_dict[key]
            for item in fasta_list:
                wfile.write(item)
            wfile.write("\n")
    return dna_fasta_path
