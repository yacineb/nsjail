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