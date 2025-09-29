# Google Cloud - Creating a Persistent Disk Lab

## Overview
Compute Engine allows you to create and run virtual machines on Google infrastructure. Persistent disks provide primary storage for your virtual machine instances that exist independently of your machine - if a VM instance is deleted, the attached persistent disk retains its data and can be attached to another instance.

**Duration:** 30 minutes  
**Credits:** 1 Credit  
**Level:** Introductory

### Types of Persistent Disks:
- **Standard persistent disk**
- **SSD Persistent disk**

---

## What You'll Learn
- Create a new VM instance and attach a persistent disk
- Format and mount a persistent disk

## Prerequisites
- Familiarity with standard Linux text editors (vim, emacs, nano)

---

## Setup and Requirements

### Step 1: Start the Lab
1. Click **"Start Lab"**
2. If payment is required, select your payment method
3. Click **"Open Google Cloud console"**
4. Sign in using provided credentials:
   - Username: (copy from Lab Details pane)
   - Password: (copy from Lab Details pane)

⚠️ **Important:** Only use the provided student account.

### Step 2: Activate Cloud Shell
1. Click **Activate Cloud Shell** icon in the top right
2. Click **Continue** and **Authorize**
3. Verify setup:
```bash
gcloud auth list
gcloud config list project
```

### Step 3: Set Region and Zone
```bash
# Set zone and region (replace with provided values)
gcloud config set compute/zone Zone
gcloud config set compute/region Region

# Create variables
export REGION=Region
export ZONE=Zone
```

---

## Task 1: Create a New Instance

Create a Compute Engine virtual machine instance with only a boot disk:

```bash
gcloud compute instances create gcelab --zone $ZONE --machine-type e2-standard-2
```

**Expected Output:**
```
Created [...].
NAME       ZONE           MACHINE_TYPE  PREEMPTIBLE INTERNAL_IP EXTERNAL_IP    STATUS
gcelab     Zone e2-standard-2             10.240.X.X  X.X.X.X        RUNNING
```

The newly created VM will have a default 10 GB persistent disk as the boot disk.

✅ **Checkpoint:** New instance created in specified zone.

---

## Task 2: Create a New Persistent Disk

Create a new disk named `mydisk` in the same zone as your VM:

```bash
gcloud compute disks create mydisk --size=200GB --zone $ZONE
```

**Expected Output:**
```
NAME   ZONE          SIZE_GB TYPE        STATUS
mydisk Zone 200      pd-standard READY
```

✅ **Checkpoint:** New persistent disk created in specified zone.

---

## Task 3: Attaching a Disk

### Step 1: Attach the Persistent Disk

Attach the new disk (`mydisk`) to your VM instance (`gcelab`):

```bash
gcloud compute instances attach-disk gcelab --disk mydisk --zone $ZONE
```

**Expected Output:**
```
Updated [https://www.googleapis.com/compute/v1/projects/.../zones/Zone/instances/gcelab].
```

### Step 2: Find the Persistent Disk in the VM

SSH into the virtual machine:

```bash
gcloud compute ssh gcelab --zone $ZONE
```

**SSH Setup Process:**
- Enter **Y** to continue when prompted
- Press **ENTER** twice for no passphrase when creating SSH keys

### Step 3: Locate the Disk Device

List disk devices to find your attached disk:

```bash
ls -l /dev/disk/by-id/
```

**Expected Output:**
```
lrwxrwxrwx 1 root root  9 Feb 27 02:24 google-persistent-disk-0 -> ../../sda
lrwxrwxrwx 1 root root 10 Feb 27 02:24 google-persistent-disk-0-part1 -> ../../sda1
lrwxrwxrwx 1 root root  9 Feb 27 02:25 google-persistent-disk-1 -> ../../sdb
lrwxrwxrwx 1 root root  9 Feb 27 02:24 scsi-0Google_PersistentDisk_persistent-disk-0 -> ../../sda
lrwxrwxrwx 1 root root 10 Feb 27 02:24 scsi-0Google_PersistentDisk_persistent-disk-0-part1 -> ../../sda1
lrwxrwxrwx 1 root root  9 Feb 27 02:25 scsi-0Google_PersistentDisk_persistent-disk-1 -> ../../sdb
```

The attached disk will be: `scsi-0Google_PersistentDisk_persistent-disk-1`

### Step 4: Format and Mount the Persistent Disk

**Create a mount point:**
```bash
sudo mkdir /mnt/mydisk
```

**Format the disk with ext4 filesystem:**
```bash
sudo mkfs.ext4 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/disk/by-id/scsi-0Google_PersistentDisk_persistent-disk-1
```

**Mount the disk:**
```bash
sudo mount -o discard,defaults /dev/disk/by-id/scsi-0Google_PersistentDisk_persistent-disk-1 /mnt/mydisk
```

### Step 5: Auto-mount on Restart

To ensure the disk remounts after VM restart, edit `/etc/fstab`:

```bash
sudo nano /etc/fstab
```

Add the following line below the UUID line:
```
/dev/disk/by-id/scsi-0Google_PersistentDisk_persistent-disk-1 /mnt/mydisk ext4 defaults 1 1
```

**Complete `/etc/fstab` should look like:**
```
# /etc/fstab: static file system information
UUID=12adc097-f36f-46f9-b377-b2a30cdf422f / ext4 rw,discard,errors=remount-ro,x-systemd.growfs 0 1
UUID=3A31-89F9 /boot/efi vfat defaults 0 0
/dev/disk/by-id/scsi-0Google_PersistentDisk_persistent-disk-1 /mnt/mydisk ext4 defaults 1 1
```

**Save and exit:** Press `CTRL+O`, `ENTER`, `CTRL+X`

✅ **Checkpoint:** Persistent disk attached and mounted successfully.

---

## Task 4: Test Your Knowledge

### Question 1: Can you prevent the destruction of an attached persistent disk when the instance is deleted?

**Answer:** 
- ✅ Yes, use the `–keep-disks` option with the `gcloud compute instances delete` command
- ✅ Yes, deselect the option `Delete boot disk when instance is deleted` when creating an instance

### Question 2: For migrating data from a persistent disk to another region, what is the correct order of steps?

**Steps:**
1. Attach disk
2. Create disk  
3. Create snapshot
4. Create instance
5. Unmount file system(s)

**Correct Order:** **(5, 3, 2, 4, 1)**
1. Unmount file system(s)
2. Create snapshot
3. Create disk
4. Create instance
5. Attach disk

---

## Task 5: Local SSDs

### Local SSD Overview
Compute Engine can attach local SSDs that are physically attached to the server hosting your VM instance.

### Local SSD Performance:
- **Latency:** Less than 1 ms
- **Read IOPS:** Up to 680,000
- **Write IOPS:** Up to 360,000

### Trade-offs:
- **Availability:** Not automatically replicated
- **Durability:** All data can be lost during host errors
- **Flexibility:** Requires special precautions for data backup

⚠️ **Note:** This lab does not cover local SSDs. To maximize local SSD performance, use a special Linux image that supports NVMe.

---

## Congratulations!

🎉 **You've successfully completed the lab!**

### What You Learned:
- ✅ How to create persistent disks
- ✅ How to attach persistent disks to VM instances
- ✅ How to format and mount persistent disks
- ✅ How to configure auto-mounting on restart
- ✅ Key differences between persistent disks and local SSDs

### Use Cases:
- Database servers setup and configuration
- Data storage that persists beyond VM lifecycle
- Shared storage between multiple instances

### Next Steps:
- Review [Persistent Disk Documentation](https://cloud.google.com/persistent-disk/docs)
- Learn more with [gcloud Documentation](https://cloud.google.com/sdk/gcloud)

---

**Lab ID:** GSP004  
**Last Updated:** January 15, 2024  
**Copyright:** Google LLC. All rights reserved.
