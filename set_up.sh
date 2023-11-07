mkdir DiffModeler/best_model
mkdir DiffModeler/data
cd DiffModeler/best_model
wget https://huggingface.co/zhtronics/DiffModelerWeight/resolve/main/diffusion_best.pth.tar
cd ..
cd data
wget https://huggingface.co/datasets/zhtronics/BLAST_RCSB_AFDB/resolve/main/data.tar.gz.aa
wget https://huggingface.co/datasets/zhtronics/BLAST_RCSB_AFDB/resolve/main/data.tar.gz.ab
wget https://huggingface.co/datasets/zhtronics/BLAST_RCSB_AFDB/resolve/main/data.tar.gz.ac
tar -xvzf data.tar.gz
cd ../..
