mkdir example
cd example
wget https://kiharalab.org/emsuites/complexmodeler/input/20031.mrc
wget https://kiharalab.org/emsuites/complexmodeler/input/20031.fasta
cd ..
mkdir DiffModeler/best_model
mkdir DiffModeler/data
cd DiffModeler/best_model
wget https://huggingface.co/zhtronics/DiffModelerWeight/resolve/main/diffusion_best.pth.tar
cd ..
wget https://huggingface.co/datasets/zhtronics/BLAST_RCSB_AFDB/resolve/main/data.tar.gz.aa
wget https://huggingface.co/datasets/zhtronics/BLAST_RCSB_AFDB/resolve/main/data.tar.gz.ab
wget https://huggingface.co/datasets/zhtronics/BLAST_RCSB_AFDB/resolve/main/data.tar.gz.ac
cat data.tar.gz.aa data.tar.gz.ab data.tar.gz.ac >data.tar.gz
tar -xzvf data.tar.gz
cd ..
