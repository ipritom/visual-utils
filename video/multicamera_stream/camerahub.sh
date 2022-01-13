#!/bin/bash
source /home/[username]/anaconda3/etc/profile.d/conda.sh
conda --version;
conda activate zmqRnd;
python camera1.py & python camera2.py
wait