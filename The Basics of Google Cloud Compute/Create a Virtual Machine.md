# Google Cloud - Create a Virtual Machine Lab

## Overview
This lab guides you through creating virtual machines (VMs) on Google Cloud Platform using both web interface and command line. You will learn how to:
- Create a VM via Google Cloud Console
- Create a VM via gcloud command line
- Install NGINX web server and connect it to a VM

**Duration:** 40 minutes  
**Credits:** 1 Credit  
**Level:** Introductory

---

## Setup and Requirements

### Prerequisites:
- Internet browser (Chrome recommended)
- Use Incognito/private browser window
- Basic understanding of Linux text editors (vim, emacs, nano)

### Step 1: Start the Lab
1. Click **"Start Lab"**
2. If payment is required, select your payment method
3. Click **"Open Google Cloud console"**
4. Sign in using provided credentials:
   - Username: (copy from Lab Details pane)
   - Password: (copy from Lab Details pane)

⚠️ **Important:** Only use the provided student account, do not use personal accounts.

### Step 2: Activate Cloud Shell
1. Click **Activate Cloud Shell** icon in the top right corner
2. Click **Continue** and **Authorize**
3. Verify project ID:
```bash
gcloud config list project
```

### Step 3: Set Region and Zone
```bash
# Set region (replace REGION with provided region)
gcloud config set compute/region REGION

# Create region variable
export REGION=REGION

# Create zone variable (replace Zone with provided zone)
export ZONE=Zone
```

---

## Task 1: Create a VM Instance via Cloud Console

### Step 1: Access Compute Engine
1. From Navigation menu (☰) → **Compute Engine** → **VM Instances**
2. Click **"Create Instance"**

### Step 2: Configure Machine
| Field | Value | Notes |
|-------|-------|-------|
| Name | `gcelab` | VM instance name |
| Region | `<REGION>` | Region set above |
| Zone | `<ZONE>` | Zone set above |
| Series | `E2` | |
| Machine Type | `e2-medium` | 2-CPU, 4GB RAM |

### Step 3: Configure OS and Storage
1. Click **"OS and storage"**
2. Click **"Change"** and select:
   - Operating system: **Debian**
   - Version: **Debian GNU/Linux 12 (bookworm)**
   - Boot disk type: **Balanced persistent disk**
   - Size: **10 GB**

### Step 4: Configure Networking
1. Click **"Networking"**
2. Firewall: ✅ **Allow HTTP traffic**

### Step 5: Create VM
1. Click **"Create"** to create the VM
2. Wait about 1 minute for VM creation
3. Click **SSH** next to the `gcelab` instance name to connect

---

## Task 2: Install NGINX Web Server

### Step 1: Update OS
```bash
sudo apt-get update
```

### Step 2: Install NGINX
```bash
sudo apt-get install -y nginx
```

### Step 3: Verify NGINX is Running
```bash
ps auwx | grep nginx
```

### Step 4: Test Web Page
1. Return to Cloud Console
2. Click the **External IP** of the VM
3. Or open browser with address: `http://EXTERNAL_IP/`
4. You should see: **"Welcome to nginx!"**

✅ **Checkpoint:** VM created and NGINX installed successfully.

---

## Task 3: Create a VM Instance via gcloud Command

### Step 1: Create VM using Command Line
```bash
gcloud compute instances create gcelab2 --machine-type e2-medium --zone=$ZONE
```

**Expected Output:**
```
Created [...gcelab2].
NAME: gcelab2
ZONE: Zone  
MACHINE_TYPE: e2-medium
PREEMPTIBLE:
INTERNAL_IP: 10.128.0.3
EXTERNAL_IP: 34.136.51.150
STATUS: RUNNING
```

### Step 2: Check Default Options
```bash
gcloud compute instances create --help
```
*(Press CTRL+C to exit help)*

### Step 3: Connect via SSH using gcloud
```bash
gcloud compute ssh gcelab2 --zone=$ZONE
```
- Type **Y** to continue
- Press **Enter** to skip passphrase (leave empty)
- Type `exit` to disconnect from SSH

### Step 4: Verify VM Creation
1. Return to **Compute Engine > VM instances** in Console
2. Click **Refresh** 
3. You should see both instances: `gcelab` and `gcelab2`

✅ **Checkpoint:** Second VM created successfully via command line.

---

## Task 4: Test Your Knowledge

**Question:** Through which of the following ways can you create a VM instance in Compute Engine?

**Answer:**
- ✅ The gcloud command line tool  
- ✅ The Cloud console

---

## Congratulations!

🎉 **Congratulations!** You have successfully completed the lab:

- ✅ Created VM via Google Cloud Console
- ✅ Created VM via gcloud command line  
- ✅ Installed and configured NGINX web server
- ✅ Connected and managed VM instances

### Next Steps:
- Take the lab: **Get Started with Cloud Shell and gcloud**
- Or try: **Provision Services with Google Cloud Marketplace**

### Learn More:
- [Virtual machine instances documentation](https://cloud.google.com/compute/docs/instances)
- [Migrate VMs to Google Cloud](https://cloud.google.com/migrate/compute-engine)
- [VPC networks](https://cloud.google.com/vpc/docs)

---

**Lab ID:** GSP001  
**Last Updated:** September 15, 2025  
**Copyright:** Google LLC. All rights reserved.
