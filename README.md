# sanbox POC

## Which kind of isolation does it provide

- Linux namespaces: UTS (hostname), MOUNT (chroot), PID (separate PID tree), IPC, NET (separate networking context), USER, CGROUPS
- FS constraints: chroot(), pivot_root(), RO-remounting, custom /proc and tmpfs mount points
- Resource limits (wall-time/CPU time limits, VM/mem address space limits, etc.)
- Programmable seccomp-bpf syscall filters (through the kafel language)
- Cloned and isolated Ethernet interfaces
- Cgroups for memory and PID utilization control.


Examples:
- Run echo command once only, as a sub-process: `nsjail -Mo --chroot / -- /bin/echo "ABC"`
- Execute echo command directly, without a supervising process: `nsjail -Me --chroot / --disable_proc -- /bin/echo "ABC"`

## Building the docker

Base image for nsjail
`docker build . -t nsjail`

Playground image
`docker build -f Dockerfile.playground . -t playground`

how to run stuff inside testing docker:

`./run_interactive.sh`

Then you can run examples:

- `nsjail --chroot / --config  /sandbox.cfg -- python3 --version`
- `nsjail --chroot / --config  /sandbox.cfg -- python3 /examples/hello.py`
- `nsjail --chroot / --config  /sandbox.cfg -- /usr/bin/python3 -Su /examples/hello.py `

## Sandbox permissions

### System

**keep_caps: false** = Strip all capabilities from the sandboxed process
This means the sandboxed Python code runs with minimal privileges

### User

- 👤 Username: nobody
- 📝 Real Name: Unknown
- 🆔 User ID: 65534
- 👥 Group ID: 65534

### Folders

- R/W permissions on `/data` dir mount, which is actually isolated for each sandbox run. This directory is the default pwd and user's HOME dir.
- /tmp dir with rw permissions, it's mounted to 'tmpfs', lives in RAM. So basically it goes off after sandbox execution end and each sandbox has own isolated temp dir

### Network

- Egress to internet is allowed
- No local IP

### Environment variables

list of inherited env vars from host:

- "WANDB_API_KEY"
- "HF_DATASETS_CACHE"
- "HF_HOME"
- "HF_TOKEN"


## Limits

- 1GB RAM
- 8GB maximum file size
- 8GB max size of data segment.

## TBD

- handle lib64
- harden network access policy:
    - Only traffic to External Net
    - And traffic to harmony ws endpoint.