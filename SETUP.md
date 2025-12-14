# Flood Predictor — Setup and Workflow Guide

This document explains how to set up the Flood Predictor project for a shared NFS workspace and HTCondor/DAGMan, create a Python virtual environment, install requirements, and run the workflow from `/mnt/data/Flood_predictor`.

## Prerequisites
- Linux head/execute nodes with HTCondor installed (DAGMan support).
- NFS or other shared filesystem accessible at the same path on all nodes.
- Git installed.
- Python 3.8+ and `pip` available.

## 1. Clone the repository

On the submission host in the mount that will submit the DAG:

```bash
git clone https://github.com/SeenNow/Flood_predictor.git
cd Flood_predictor
```
This should put all files on the from github on your system

## 2. Make sure the .py ,.sub, and .dag files are executable
if you are in Flood_predictor directory
```bash
chmod +x *
```
Or if in mnt/data directory use
```bash
chmod -R +x Flood_predictor
```

## 3. Set up Python environment

On a node that can access `/mnt/data/Flood_predictor`:

First, ensure `venv` is installed (it's usually included with Python 3.3+, but may need to be installed separately):

```bash
# For Debian/Ubuntu:
sudo apt-get install python3-venv
```
Then create and activate the virtual environment:

```bash
cd /mnt/data/Flood_predictor
```
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
```bash
pip install -U pip
```
```bash
pip install -r requirement.txt
```

If you don't have `requirement.txt`, install the core packages manually:

```bash
pip install pandas numpy seaborn matplotlib scikit-learn scipy requests
```

## 4. Quick Start — install and run

Minimal steps to install requirements and run a script from `/mnt/data/Flood_predictor`:

```bash
cd /mnt/data/Flood_predictor
. venv/bin/activate             
pip install -r requirement.txt

# Run one script (example):
venv/bin/python task_a_ingestion.py

# Or submit the DAG with DAGMan:
condor_submit_dag flood.dag
```

Make sure `flood.sub` points at the same virtualenv Python, for example:

```
executable = /mnt/data/Flood_predictor/venv/bin/python
arguments = $(script_name)
initialdir = /mnt/data/Flood_predictor
should_transfer_files = NO
```


## 5. Verify locally

Activate the venv and run the pipeline scripts to verify they work:

```bash
. venv/bin/activate
python task_a_ingestion.py
python task_b_preprocessing.py
python task_c_feature_engineering.py
python task_d_split.py
python task_e1_rainfall.py
python task_e2_water.py
python task_f_merge.py
python task_g_validation.py
python task_h_visualize.py
```

## 7. Submit the DAG

Validate and submit the DAG:

```bash
condor_submit_dag flood.dag
```

