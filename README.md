
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

- Access to a remote server (e.g., Noctua 2)
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
