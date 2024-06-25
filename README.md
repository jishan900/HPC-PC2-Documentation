# Documentation for access in Noctua-1 Cluster 

An HPC cluster system consists of many server computers (nodes) that are connected via a high-speed network and operated in a data centre.
The server computers are built to execute computationally intensive research applications. This documentation will help those who want to install and run Noctua-1. 

## 1. Setting Up the VPN Tunnel

- Install personal network certificate
- Install OpenVPN (Visit the following link to download the configuration file for OpenVPN: [Download OpenVPN File](https://openvpn.net/community-downloads/))
- Start OpenVPN
- Download configuration file: (Visit the following link to download the configuration file for OpenVPN: [Download Configuration File](https://hilfe.uni-paderborn.de/VPN_unter_Windows)). Choose HPC-PC2 (Standard) and download it. 
- Import configuration file
- Establish VPN connection 

## 2. Access with SSH
- Use PuTTYgen to generate public and private keys. Send the public key to the following email address so they can add it to your profile (E-mail address: pc2-support@uni-paderborn.de). 

## 3. System-Specific Access

- The Jump-Host for Noctua 1 is **fe.noctua1.pc2.uni-paderborn.de**. Port 22 (SSH).
- The config file should be like this - 

```bash
  Host noctua-jumphost
    Hostname fe.noctua1.pc2.uni-paderborn.de
    User [USERNAME]
    IdentityFile C:/Users/Jishan/Downloads/PuTTY_and_SSH2_Key/private_key
    IdentitiesOnly yes
  
  Host noctua-ln1
    Hostname ln-0001
    User [USERNAME]
    ProxyJump noctua-jumphost
    IdentityFile C:/Users/Jishan/Downloads/PuTTY_and_SSH2_Key/private_key
    IdentitiesOnly yes
  
  Host noctua-ln2
    Hostname ln-0002
    User [USERNAME]
    ProxyJump noctua-jumphost
    IdentityFile C:/Users/Jishan/Downloads/PuTTY_and_SSH2_Key/private_key
    IdentitiesOnly yes

# Noctua 2
Host n2cn* n2lcn* n2gpu* n2fpga* n2dgx* n2hcn*
    HostName %h
    ProxyJump n2login2
    User [USERNAME]
    IdentityFile C:/Users/Jishan/Downloads/PuTTY_and_SSH2_Key/private_key
    IdentitiesOnly yes
    
# Noctua 1
Host cn-* gpu-*
    HostName %h
    ProxyJump noctua-ln2
    User [USERNAME]
    IdentityFile C:/Users/Jishan/Downloads/PuTTY_and_SSH2_Key/private_key
    IdentitiesOnly yes 
```
In your ~/.ssh/config and replace [USERNAME] with your username on Noctua and [PATH TO PRIVATE KEY] with the path to your private key of your ssh-key. Then you can use the short command ssh noctua1 to connect to Noctua. You will be asked for the password of your ssh-key when logging in instead of your user password.

## 4. Setting Up Remote Tunnels with VS Code

This guide provides detailed instructions on how to set up and use remote tunnels with Visual Studio Code. This allows you to remotely run and manage your coding sessions on another machine, such as a server in a data center or a compute node in a high-performance computing environment.

### Prerequisites

- Access to a remote server (e.g., Noctua 1)
- SSH access to the remote machine
- Local machine with internet connection

### Step 1: Download the VS Code CLI

#### 1.1 Visit the Download Page

- Navigate to the [VS Code Download Page](https://code.visualstudio.com/download).

#### 1.2 Download the CLI for Linux

- Download the CLI version appropriate for your system. As of April 2023, use this [direct link for the CLI Alpine Linux x64 version](https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64).

#### 1.3 Save the File

- Save the downloaded file to your local machine.

### Step 2: Install the CLI on the Remote Machine

#### 2.1 Transfer the Downloaded File

- Use `scp` or another secure file transfer method to transfer the downloaded file to the remote machine.

#### 2.2 Extract the Archive

- Extract the binary with the command: `tar -xzf filename.tar.gz`. Replace `filename.tar.gz` with the actual file name of the downloaded archive.

#### 2.3 Place the Binary

- Create the directory if it doesn’t exist: `mkdir -p ~/.local/bin`
- Move the binary: `mv code ~/.local/bin/`

### Step 3: Update Your PATH

#### 3.1 Edit `.bashrc`

- Open your `.bashrc` file in an editor, e.g., `nano ~/.bashrc`.

#### 3.2 Add PATH Export

- Add the following line to the end of the file: `export PATH=$HOME/.local/bin:$PATH`

#### 3.3 Source `.bashrc`

- Apply the changes: `source ~/.bashrc`

### Step 4: Create a Remote Tunnel (Server Side)

#### 4.1 Run the VS Code CLI

- On the server or compute node, enter: `code tunnel --verbose`

#### 4.2 Follow On-Screen Instructions

- Follow the steps in the terminal, possibly including authenticating with GitHub.

### Step 5: Connect From Your Local Machine (Client Side)

#### 5.1 Open VS Code on Your Local Machine

#### 5.2 Install the “Remote - Tunnels” Extension

- Go to the Extensions view by clicking on the square icon on the sidebar or pressing `Ctrl+Shift+X`.
- Search for “Remote - Tunnels” and install it.

#### 5.3 Connect to the Tunnel

- Execute the command `Remote Tunnels: Connect to Tunnel...` from the Command Palette (`Ctrl+Shift+P`).
- Select the tunnel you wish to use.

### Step 6: Authenticate with GitHub (First Time Only)

- If it's your first time, you will need to authenticate through GitHub to verify your identity.

### Note on VS Code CLI Location

To improve performance and manage disk usage efficiently, create a symbolic link for `.vscode-cli` pointing to a folder on a parallel file system:

```bash
mkdir -p /scratch/hpc-prf-mypr/username/.vscode-cli
ln -s /scratch/hpc-prf-mypr/username/.vscode-cli ~/.vscode-cli
```
## 5. Software and Tools
There are several ways to get the software you need:

- Using preinstalled Software
- Via package managers like pip or conda for Python  or Pkg for Julia
- Via software containers with Singularity 
- Manual installation in your project directory

Please contact them if the software you need is not available via email. For example, in the Noctua-1 cluster, several software and packages were missing so  I contacted them several times and fixed them. (Support E-mail address: pc2-support@uni-paderborn.de). 

## 6. Access in Cloud and Visual Studio  
### - Running Cloud
- Go to CMD or Anaconda Prompt, enter: `ssh noctua-ln1`
- For VStudio, enter: `code tunnel --verbose`
- For web, enter: `https://vscode.dev/tunnel/noctua1`

### - For Visual Files 
- I use [FileZilla](https://filezilla-project.org/download.php?platform=win64).

### - Compute node: Code-server
- Go to CMD or Anaconda Prompt, enter: `ssh noctua-ln1` or `noctua-ln2`, depending on which node you want to use
- `module load tools code-server`
- `PASSWORD=[YOUR PASSWORD] code-server --bind-addr 0.0.0.0:8081 --auth password`
- Then open another cmd
- `ssh -L 8081:ln-0001:8081 -J ltsbo2@noctua-jumphost noctua-ln1`
- Then in browser: `http://127.0.0.1:8081/`

### - Running Visual Studio
- Press `F1` in Visual Studio
- `Remote SSH Connect`
- Select `Noctua-ln1`
- If you need further information, then please visit: [PC2-Documentation](https://upb-pc2.atlassian.net/wiki/spaces/PC2DOK/overview?mode=global). 
## IMPORTANT: Run Python Script in Noctua Cluster - 1

If you need to install any particular library or something, you need to contact the GPU authorities, and their contact details are already given in the previous section. For example, I needed the Tensorflow GPU version, but that library was only available in the Noctua-2 Cluster. So, I contacted them and gave them details of what I needed to do, and they installed it and informed me when it was done.  


If you want to check which module are available in this cluser then use the following command: 

- `module avail or ml avail`


If you need any particular library and want to check whether is it already available or not, then simply use the following command in your CMD:

- `module spider or ml spider`

Display description of a selected module (e.g. Tensorflow): 

- `module spider tensorflow or ml spider tensorflow`

Display help, usage information for modules: 

- `ml help`

Running a Python script is a bit tricky in this Noctua-1 cluster cloud GPU. I am presenting an example, which I did, and scripts are available in the current repository. So, first of all, we need to write a shell script that gives details on which library we need to load and how much GPU memory we need to execute this program. 

**SLURM Script:** [Shell Script](https://github.com/jishan900/HPC-PC2-Documentation/blob/master/Test_TF/job.sh).

```bash
#!/bin/bash: Specifies the script interpreter to be the Bash shell.
#SBATCH -n1: Requests 1 task (core) for the job.
#SBATCH -t 5: Sets a time limit of 5 minutes for the job.
#SBATCH -p gpu: Requests the job to run in the GPU partition.
#SBATCH --gres=gpu:a40:1: Requests 1 A40 GPU for the job.
#SBATCH --mem=45G: Requests 45GB of memory.
#SBATCH -q express: Specifies the Quality of Service (QoS) for the job, which can be adjusted as per the requirements.
```

##### Use the parallel file system for working directory
- `cd $PC2PFS`


Resets the module environment and loads the necessary modules for the job.

```bash
module reset
module load lib/TensorFlow/2.9.1-foss-2022a-CUDA-11.7.0
module load vis
module load matplotlib/3.7.0-gfbf-2022b
python /pc2/users/l/ltsbo2/Test_TF/test.py
```

- Module reset: Resets the module environment to the default state.
- Module load lib/TensorFlow/2.9.1-foss-2022a-CUDA-11.7.0: Loads TensorFlow version 2.9.1 with the specified compiler and CUDA version.
- Module load vis: Loads visualization tools (details depend on the specific system configuration).
- Module load matplotlib/3.7.0-gfbf-2022b: Loads Matplotlib version 3.7.0.
- Python /pc2/users/l/ltsbo2/Test_TF/test.py: Runs the test.py script located in the specified directory using Python.

**Python Script:** Then I write a simple Python test script to check is it working well or not. [Python Script](https://github.com/jishan900/HPC-PC2-Documentation/blob/master/Test_TF/test.py).

Now, it is time to check my script is execute properly or not. So, for execute a script, first go to the terminal, activate cloud along with VPN and then write the following command:

- Job submission and you will get a job ID from here: `sbatch job.sh` 
- Check job status (Job ID: 3077515): `sacct -j 3077515`
- SLURM typically writes the output and error text: `ls -l slurm-3077515.out `
- View the contents of the output file: `cat slurm-3077515.out`


So, we can see that our job is completed.
![image](https://github.com/jishan900/HPC-PC2-Documentation/assets/32738421/7703e601-34ae-4dbb-87d4-2dd3522ec986)



And, this is the output. We can see that task is complete and save plots in the cloud directory. 
![image (1)](https://github.com/jishan900/HPC-PC2-Documentation/assets/32738421/8faf667b-d5e1-46bb-853f-3e1e91e83f14)


## Python Version and Module
**Check here:** [Python Version & Module](https://upb-pc2.atlassian.net/wiki/spaces/PC2DOK/pages/1902497/Python).
