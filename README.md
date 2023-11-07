
# ComplexModeler
<a href="https://github.com/marktext/marktext/releases/latest">
   <img src="https://img.shields.io/badge/ComplexModeler-v1.0.0-green">
   <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Mac%20-green">
   <img src="https://img.shields.io/badge/Language-python3-green">
   <img src="https://img.shields.io/badge/dependencies-tested-green">
   <img src="https://img.shields.io/badge/licence-GNU-green">
</a>  

ComplexModeler is a computational tool using CryoREAD and DiffModeler to automatically build full protein-DNA/RNA complex structure from cryo-EM maps at 0-5A resolution.  

Copyright (C) 2023 Xiao Wang, Han Zhu, Genki Terashi, Daisuke Kihara, and Purdue University. 

License: GPL v3. (If you are interested in a different license, for example, for commercial use, please contact us.) 

Contact: Daisuke Kihara (dkihara@purdue.edu)

For technical problems or questions, please reach to Xiao Wang (wang3702@purdue.edu).

## Citation:

Xiao Wang, Han Zhu, Genki Terashi & Daisuke Kihara. Protein Complex Structure Modeling with Diffusion Model and AlphaFold in cryo-EM maps.bioArxiv, 2023.
```
@article{wang2023DiffModeler,   
  title={Protein Complex Structure Modeling with Diffusion Model and AlphaFold in cryo-EM maps},   
  author={Xiao Wang, Han Zhu, Genki Terashi, and Daisuke Kihara},    
  journal={bioArxiv},    
  year={2023}    
}   
```

## Free Online Server: 
### Input map+single-chain structures: https://em.kiharalab.org/algorithm/ComplexModeler

## Introduction

<details>

For detailed introduction and protocol, please check [DiffModeler](https://github.com/kiharalab/DiffModeler) and [CryoREAD](https://github.com/kiharalab/CryoREAD)

</details>

## Installation

<details>

### System Requirements
CPU: >=8 cores <br>
Memory (RAM): >=50Gb. For maps with more than 3,000 nucleotides, memory space should be higher than 200GB if the sequence is provided. <br>
GPU: any GPU supports CUDA with at least 12GB memory. <br>
GPU is required for DiffModeler and CryoREAD.

## Installation  
### 1. [`Install git`](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) 
### 2. Clone the repository in your computer 
```
git clone --recurse-submodules https://github.com/kiharalab/ComplexModeler && cd ComplexModeler
```

### 3. Configure environment for ComplexModeler.
#### 3.1.1 Install anaconda
Install anaconda from https://www.anaconda.com/download#downloads.
#### 3.1.2 Install environment via yml file
Then create the environment via
```commandline
conda env create -f environment.yml
```
#### 3.1.3 Activate environment for running
Each time when you want to run this software, simply activate the environment by
```
conda activate ComplexModeler
conda deactivate(If you want to exit) 
```

### 4. Download the pre-trained model and database
Run the following command in the project direcotry
```commandline
chmod 777 set_up.sh
./set_up.sh
```
If it fails, you can run set_up.sh line by line in command line.

### 5. Install Other Dependency
Blast: Please follow the instructions in [NCBI website](https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html) to install Blast locally.
<br>(Optional but highly recommended):
Phenix: https://phenix-online.org/documentation/install-setup-run.html
Coot: https://www2.mrc-lmb.cam.ac.uk/personal/pemsley/coot/
To verify phenix is correctly installed for final refinement step, please run
```
phenix.real_space_refine -h
```
To veryify coot is correctly installed for final refinement step, please run
```
coot
```
If it can print out the help information of this function, then the refinemnt step of our program can be supported. 
<br>If not, please always remove --refine command line in all the commands, then ComplexModeler will build structure without refinement.


### 6. (Optional) Visualization software
Pymol (for structure visualization): https://pymol.org/2/    
Chimera (for map visualization): https://www.cgl.ucsf.edu/chimera/download.html  


</details>

# Usage



