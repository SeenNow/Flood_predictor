
# Flood Predictor — Step-by-Step Setup & Run Guide

This guide details exactly how to configure and run the Flood Predictor workflow on a shared NFS cluster (HTCondor).

## Step 1: Clone the Repository
Run this on your submit node (ensure you are inside the NFS mount):

```bash
cd /mnt/data
git clone https://github.com/SeenNow/Flood_predictor.git
cd Flood_predictor
```



## Step 2: Fix File Permissions

HTCondor jobs run as a generic user and need write access to this directory to save logs and data. You must grant full read/write permissions.

```bash
# Grant read/write/execute permissions to everyone
chmod -R 777 /mnt/data/Flood_predictor
```



## Step 3: Configure Python Environment

Create a virtual environment directly on the NFS drive so all worker nodes can use it.

```bash
# 1. Create the virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Upgrade pip and install dependencies
pip install -U pip
pip install -r requirement.txt

```

If you don't have `requirement.txt`, install the core packages manually:

```bash
pip install pandas numpy seaborn matplotlib scikit-learn scipy requests
```

## Step 4: Run the Program

Submit the DAG workflow to HTCondor. The repository includes a pre-configured `flood.sub` designed for NFS environments.

```bash
# If re-running after a failure, use -f to overwrite old logs
condor_submit_dag -f flood.dag
```



## Step 5: Monitor Progress

**Check the Queue:**
See if your jobs are Idle (I) or Running (R).

```bash
condor_q
```

**Watch the Workflow Manager:**
See exactly which step (A, B, C...) is running.

```bash
tail -f flood.dag.dagman.out
```

**Watch the Current Job's Log:**
Replace `A_Ingest` with the name of the job currently running (e.g., `B_Preprocess`).

```bash
tail -f A_Ingest.log
```

**Verify Output:**
Once the pipeline finishes, check for the final results:

```bash
ls -l predictions.csv flood_prediction_trends.png
```

