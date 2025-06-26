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

`docker build . -t nsjail`

how to run stuff inside testing docker:

`./run_interactive.sh`

Then you can run examples:

- `nsjail --chroot / --config  /sandbox.cfg -- python3 --version`
- `nsjail --chroot / --config  /sandbox.cfg -- python3 /examples/hello.py`
- `nsjail --chroot / --config  /sandbox.cfg -- /usr/bin/python3 -Su /examples/hello.py `

## Sandbox permissoions

### User

- 👤 Username: nobody
- 📝 Real Name: Unknown
- 🆔 User ID: 65534
- 👥 Group ID: 65534

### Folders

- R/W permissions on `/data` dir mount, which is actually isolated for each sandbox run. This directory is the default pwd
- No home directory.

### Network

- Egress to internet is allowed
- No local IP

## known issues

- mount `/lib64` to be fixed