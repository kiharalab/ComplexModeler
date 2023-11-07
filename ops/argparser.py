#
# Copyright (C) 2020 Xiao Wang
# Email:xiaowang20140001@gmail.com wang3702@purdue.edu
#
import argparse

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-F',type=str,required=True, help='input map path')#File path for decoy dir
    parser.add_argument("-P",type=str,help="input fasta path")
    parser.add_argument("--resolution",type=float,default=5,help="resolution for diffusion and structure refinement")
    parser.add_argument("--gpu",type=str,default=None,help="specify the gpu we will use")
    parser.add_argument("--output",type=str,help="Output directory")
    parser.add_argument("--contour",type=float,default=0,help="Contour level for input map, suggested 0.5*[author_contour]. (Float), Default value: 0.0")
    parser.add_argument("--refine",action="store_true",help="Optional Input. Do the last step refinement or not (Suggested to set as True).")
    parser.add_argument("--gpu_only",action="store_true",help="only run GPU related part, server use only")
    args = parser.parse_args()
    params = vars(args)
    return params
