

def pdb2cif(pdb_file, cif_file):
    # Read the PDB file
    with open(pdb_file, 'r') as f:
        pdb_lines = f.readlines()

    cif_lines = []
    current_model = 0
    atom_serial = 0

    for line in pdb_lines:
        if line.startswith('ATOM') or line.startswith('HETATM'):
            # x=float(line[30:38])
            # y=float(line[38:46])
            # z=float(line[46:54])
            # line = line[:21] + new_chain_id + line[22:30]+" %.3f %.3f %.3f "%(x,y,z)+line[54:]
            atom_serial += 1
            new_line=""
            new_line += line[:4]+"\t"
            new_line += line[6:11]+"\t"
            new_line += line[12:16]+"\t"
            new_line += line[16]+"\t"
            new_line += line[17:20]+"\t"
            new_line += line[20:22]+"\t"
            new_line += line[22:26]+"\t"
            new_line += line[26]+"\t"
            new_line += line[30:38]+"\t"
            new_line += line[38:46]+"\t"
            new_line += line[46:54]+"\t"
            new_line += line[54:60]+"\t"
            new_line += line[60:66]+"\t"
            new_line += "\n"
            cif_lines.append(new_line)

        # if line.startswith('ENDMDL'):
        #     current_model += 1
        #     atom_serial = 0

    # Write the modified structure to a new CIF file
    with open(cif_file, 'w') as f:
        f.write("data_DRNA\n#\n")
        # f.write("_audit_creation_method     'Diffusion Fitting'\n")
        # f.write("_audit_creation_date       \n")
        # f.write("_audit_author_name         'Xiao Wang'\n")
        # f.write("_entry.id                   %s\n" % new_chain_id)
        # f.write("\n")
        f.write("loop_\n")
        f.write("_atom_site.group_PDB\n")
        f.write("_atom_site.id\n")
        f.write("_atom_site.label_atom_id\n")
        f.write("_atom_site.label_comp_id\n")
        f.write("_atom_site.label_asym_id\n")
        f.write("_atom_site.label_seq_id\n")
        f.write("_atom_site.Cartn_x\n")
        f.write("_atom_site.Cartn_y\n")
        f.write("_atom_site.Cartn_z\n")
        f.write("_atom_site.occupancy\n")
        f.write("_atom_site.B_iso_or_equiv\n")

        for line in cif_lines:
            f.write(line)

def reindex_cif(final_pdb_path,final_cif_path):
    """

    :param final_pdb_path: simply combined cif file
    :param final_cif_path: final output cif renumber atom and sequence
    :return:
    """
    begin_check=False
    block_list=[]
    with open(final_pdb_path,'r') as rfile:
        for line in rfile:
            if "loop_" in line:
                begin_check=True
                continue

            if begin_check and "_atom_site" in line:
                block_list.append(line.strip("\n").replace(" ",""))
                continue
            if begin_check and "_atom_site" not in line:
                begin_check=False

    atom_ids = block_list.index('_atom_site.id')
    try:
        seq_ids = block_list.index('_atom_site.label_seq_id')
    except:
        seq_ids = block_list.index('_atom_site.auth_seq_id')
    atom_id=1
    seq_id=1
    prev_seq_id=None
    with open(final_pdb_path,'r') as rfile:
        with open(final_cif_path,'w') as wfile:
            for line in rfile:
                if len(line)>4 and line[:4]=="ATOM":
                    split_info=line.strip("\n").split()
                    current_seq_id = int(split_info[seq_ids])
                    if prev_seq_id is not None and current_seq_id!=prev_seq_id:
                        seq_id+=1
                    for j,item in enumerate(split_info):
                        if j==atom_ids:
                            wfile.write("%d  "%atom_id)

                        elif j!=seq_ids:
                            wfile.write("%s  "%item)
                        else:
                            wfile.write("%d  "%seq_id)
                    wfile.write("\n")
                    prev_seq_id=current_seq_id
                    atom_id+=1
                else:
                    wfile.write(line)
