# Common Commands

Generate Patches
```
git format-patch -1 --pretty=fuller 3a38e874d70b
```

`checkpatch.pl` to check format style of patch.

```
git format-patch -1 <commit ID> --to=maintainer1 --to=maintainer2 --cc=maillist1 --cc=maillist2
```

```
git send-email <patch_file>
```

The right place for the version history is after the "---" below the Signed-off-by tag and the start of the changed file list, as shown in the screenshot below. Everything between the Signed-off-by and the diff is just for the reviewers and will not be included in the commit. Please don’t include version history in the commit log.

```
git apply --index file.patch
```

# Setup Env

```
sudo apt-get install build-essential vim git cscope libncurses-dev libssl-dev bison flex
sudo apt-get install git-email
sudo apt-get install bindgen pahole jfsutils xfsprogs btrfs-progs pcmciautils quota ppp
sudo apt-get install nfs-common grub2-common u-boot-tools global
sudo apt install libelf-dev libdw-dev zlib1g-dev pkg-config clang llvm
sudo apt install cpio
```

```
sudo apt-get install codespell
```

If you already have a .git/hooks/post-commit file, move it to .git/hooks/post-commit.sample. git will not execute files with the .sample extension. Then, edit the .git/hooks/post-commit file to contain only the following lines:

#!/bin/bash
exec git show --format=email HEAD | ./scripts/checkpatch.pl --strict --codespell
# Make sure the file is executable:
chmod a+x .git/hooks/post-commit

# Compilation

```
make x86_64_defconfig
make kvm_guest.config
```

Compile a module
`make M=drivers/media/test-drivers/vimc`

Check 
`drivers/media/test-drivers/vimc/Kconfig`
for dependency and config option

# Busybox settings

```
make defconfig
make menuconfig
```

- Enabled static binary
- Disable tc

```
cd initramfs
mkdir -p {bin,sbin,proc,sys,dev}
cp busybox bin/
```

Init
```
#!/bin/sh

mount -t proc none /proc
mount -t sysfs none /sys
mount -t devtmpfs none /dev

echo -e "\nBoot took $(cut -d' ' -f1 /proc/uptime) seconds\n"

exec /bin/sh
```

```
cd initramfs
find . | cpio -o -H newc | gzip > ../initramfs.gz
```

# QEMU notes

| Keys       | What it does               |
| ---------- | -------------------------- |
| `Ctrl+A H` | Help (shows all shortcuts) |
| `Ctrl+A X` | Exit QEMU                  |
| `Ctrl+A C` | Open QEMU monitor          |
| `Ctrl+A R` | Reset VM                   |
| `Ctrl+A P` | Pause                      |
| `Ctrl+A S` | Resume                     |


```
qemu-system-x86_64 \
  -kernel stable/arch/x86_64/boot/bzImage \
  -initrd initramfs.gz \
  -append "console=ttyS0" \
  -nographic \
  -machine type=pc,accel=kvm \
  -cpu host \
  -m 2048 \
  -smp cores=2
```

```
sudo apt install qemu-system qemu-utils
```

```
qemu-img create \
-f qcow2 \
/mnt/d/mintVM/mintVM.qcow2 20G
```

```
qemu-system-x86_64 \
-m 16384 \
-smp cores=8 \
-cpu host \
-machine type=pc,accel=kvm \
-hda /mnt/d/mintVM/mintVM.qcow2 \
-cdrom /mnt/d/isos/linuxmint.iso \
-boot d \
-vga virtio \
-usb -device usb-mouse -device usb-kbd

qemu-system-x86_64 \
-m 16384 \
-smp cores=8 \
-cpu host \
-machine type=pc,accel=kvm \
-hda /mnt/d/mintVM/mintVM.qcow2 \
-boot c \
-vga virtio \
-usb -device usb-mouse -device usb-kbd
```


# Grub

`/etc/default/grub`

Enable printing early boot messages to vga using the earlyprink=vga kernel boot option
Increase the GRUB_TIMEOUT value to 30 seconds, so grub pauses in menu allowing time to choose the kernel to boot from the grub menu, and comment out GRUB_TIMEOUT_STYLE=hidden

GRUB_CMDLINE_LINUX="earlyprink=vga"
#GRUB_TIMEOUT_STYLE=hidden
GRUB_TIMEOUT=30

`sudo update-grub`

# Modules

Configure as a module:

    Configure CONFIG_USB_VIDEO_CLASS=m
    Recompile your kernel and install. Please note that you don't have to reboot your system. You can load your newly installed module.

Load module:

    sudo modprobe uvcvideo
    Once you load the module, let's check if you see your message.
    Run dmesg | less and search for "I changed". Do you see the message?
    Run lsmod | grep uvcvideo. Do you see the module?

Unload module:

    sudo rmmod uvcvideo
    Check dmesg for any messages about the uvcvideo module removal.
    Run lsmod | grep uvcvideo. Do you see the module?

Configure Built-in:

    Configure CONFIG_USB_VIDEO_CLASS=y
    Recompile your kernel, install, and reboot the system into the newly installed kernel.
    Run dmesg | less and search for "I changed". Do you see the message?

# Patch checklist

    Run scripts/checkpatch.pl before sending the patch. Note that checkpatch.pl might suggest unnecessary changes! Use your best judgment when deciding whether it makes sense to make the change checkpatch.pl suggests. The end goal is for the code to be more readable. If checkpatch.pl suggests a change and you think the end result is not more readable, don't make the change. For example, if a line is 81 characters long, but breaking it makes the resulting code look ugly, don't break that line.
    Compile and test your change.
    Document your change and include relevant testing details and results of that testing.
    Signed-off-by should be the last tag.
    As a general rule, don't include change lines in the commit log.
    Remember that good patches get accepted quicker. It is important to understand how to create good patches.
    Copy mailing lists and maintainers/developers suggested by scripts/get_maintainer.pl.
    Be patient and wait at least one week before requesting comments. During busy periods such as the merge windows, it could take longer than a week.
    Always thank the reviewers for their feedback and address them.
    Don’t hesitate to ask a clarifying question if you don’t understand the comment.
    When working on a patch based on a suggested idea, give credit using the Suggested-by tag. Other tags used for giving credit are Tested-by, Reported-by.
    Remember that the reviewers help improve code. Don’t take it personally and handle the feedback gracefully. Please don’t top-post when responding to emails. Responses should be inlined.
    Keep in mind that the community is not obligated to accept your patch. Patches are pulled, not pushed. Always give a reason for the maintainer to take your patch.
    Be patient and be ready to make changes and work with the reviewers. It could take multiple versions before your patch gets accepted. It is okay to disagree with maintainers and reviewers. Please don't ignore a review because you disagree with it. Present your reasons for disagreeing and supporting technical data such as benchmarks and other improvements.
    In general, getting responses and comments is a good sign that the community likes the patch and wants to see it improved. Silence is what you want to be concerned about. If you don't hear back from the maintainer after a week, feel free to either send the patch again, or send a gentle "ping" - something like "Hi, I know you are busy, but have you found time to look at my patch?"
    Expect to receive comments and feedback at any time during the review process.
    Stay engaged and be ready to fix problems, if any, after the patch gets accepted into linux-next for integration into the mainline. Kernel build and Continuous Integration (CI) bots and rings usually find problems.
    When a patch gets accepted, you will either see an email from the maintainer or an automated patch accepted email with information on which tree it has been applied to, and some estimate on when you can expect to see it in the mainline kernel. Not all maintainers might send an email when the patch gets merged. The patch could stay in linux-next for integration until the next merge window, before it gets into Linus's tree. Unless the patch is an actual fix to a bug in Linus's tree, in which case, it may go directly into his tree.
    Sometimes you need to send multiple related patches. This is useful for grouping, say, to group driver clean-up patches for one particular driver into a set, or grouping patches that are part of a new feature into one set. git format-patch -2 -s --cover-letter --thread --subject-prefix="PATCH v3" --to= “name” --cc=” name” will create a threaded patch series that includes the top two commits and generated cover letter template. It is a good practice to send a cover letter for a patch series.
    Including patch series version history in the cover letter will help reviewers get a quick snapshot of changes from version to version.
    When a maintainer accepts a patch, the maintainer assumes maintenance responsibility for that patch. As a result, maintainers have decision-making power on how to manage patch flow into their sub-system(s), and they also have individual preferences. Be prepared for maintainer-to-maintainer differences in commit log content and sub-system specific coding styles.

# Tests

```
dmesg -t -l emerg
dmesg -t -l crit
dmesg -t -l alert
dmesg -t -l err
dmesg -t -l warn
dmesg -t -k
dmesg -t
```

Stress test by compiling the kernel (multiple in parallel)
`time make all`

# Debug

```
git grep -r DEBUG | grep Kconfig

CONFIG_KASAN
CONFIG_KMSAN
CONFIG_UBSAN
CONFIG_LOCKDEP
CONFIG_PROVE_LOCKING
CONFIG_LOCKUP_DETECTOR
```

```
scripts/decode_stacktrace.sh ./vmlinux < panic_trace.txt
```

Available events to trace
```
sudo cat /sys/kernel/debug/tracing/available_events

Enable all events:
      cd /sys/kernel/debug/tracing/events
      echo 1 > enable 

Enable the skb events:
      cd /sys/kernel/debug/tracing/events/skb
      echo 1 > enable 

sudo cat /sys/kernel/debug/tracing/trace
```

# Patching the release

```
stable_checkout.sh
     #!/bin/bash
     ## SPDX-License-Identifier: GPL-2.0
     # Copyright(c) Shuah Khan <skhan@linuxfoundation.org>
     #
     # License: GPLv2
     # Example usage: stable_checkout.sh <stable-release-version e.g 5.2>
     mkdir -p stable
     cd stable
     git clone git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git linux_$1_stable
     cd linux_$1_stable
     git checkout linux-$1.y
     #cp /boot/ .config # Replace <currentconfig> Here with the config file you want to use​

pre_compile_setup.sh
     #!/bin/bash
     ## SPDX-License-Identifier: GPL-2.0
     # Copyright(c) Shuah Khan <skhan@linuxfoundation.org>
     #
     # License: GPLv2
     # Example usage: pre_compile_setup.sh 5.2.11 1 5
     # Arg1 is the stable release version which is typically 5.2.x
     # Arg2 is the 1 for rc1 or 2 for rc2
     # Arg3 is 4.x or 5.x used to call wget to get the patch file
     echo Testing patch-$1-rc$2
     wget https://www.kernel.org/pub/linux/kernel/v$3.x/stable-review/patch-$1-rc$2.gz ;
     git reset --hard
     make clean
     git pull
     gunzip patch-$1-rc$2.gz
     git apply --index patch-$1-rc$2
     echo "Patch-$1-rc$2 applied"
     head Makefile
     make -j2 all
     rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
     su -c "make modules_install install"
     echo Ready for reboot test of Linux-$1-$2
```

```
dmesg_checks.sh
     # !/bin/bash
     #
     #SPDX-License-Identifier: GPL-2.0
     # Copyright(c) Shuah Khan <skhan@linuxfoundation.org>
     #
     # License: GPLv2​

          if [ "$1" == "" ]; then
             echo "$0 " <old name -r>
             exit -1
     fi

release=`uname -r`
echo "Start dmesg regression check for $release" > dmesg_checks_results

echo "--------------------------" >> dmesg_checks_results

dmesg -t -l emerg > $release.dmesg_emerg
echo "dmesg emergency regressions" >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results
diff $1.dmesg_emerg $release.dmesg_emerg >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results

dmesg -t -l crit > $release.dmesg_crit
echo "dmesg critical regressions" >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results
diff $1.dmesg_crit $release.dmesg_crit >> dmesg_checks_results 
echo "--------------------------" >> dmesg_checks_results

dmesg -t -l alert > $release.dmesg_alert
echo "dmesg alert regressions" >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results
diff $1.dmesg_alert $release.dmesg_alert >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results

dmesg -t -l err > $release.dmesg_err
echo "dmesg err regressions" >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results
diff $1.dmesg_err $release.dmesg_err >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results

dmesg -t -l warn > $release.dmesg_warn
echo "dmesg warn regressions" >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results
diff $1.dmesg_warn $release.dmesg_warn >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results

dmesg -t > $release.dmesg
echo "dmesg regressions" >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results
diff $1.dmesg $release.dmesg >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results

dmesg -t > $release.dmesg_kern
echo "dmesg_kern regressions" >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results
diff $1.dmesg_kern $release.dmesg_kern >> dmesg_checks_results
echo "--------------------------" >> dmesg_checks_results

echo "--------------------------" >> dmesg_checks_results

echo "End dmesg regression check for $release" >> dmesg_checks_results
```

# docs

make htmldocs

make htmldocs > doc_make.log 2>&1

# Follow up

Join the #kernelnewbies IRC channel on the OFTC IRC network. Several of us developers hang out on that channel. This server is home to #mm, #linux-rt, and several other Linux channels.
Join the #linux-kselftest, #linuxtv, #kernelci, or #v4l IRC channels on freenode.
- This server recommends Nick registration. Server Name: irc.freenode.net/6667. You can register your Nick in the server tab with the command: /msg NickServ identify <password>
- You can configure your chat client to auto-identify using the NickServ(/MSG NickServ+password) option - works on hexchat.
Find spelling errors in kernel messages.
Static code analysis error fixing: Static code analysis is the process of detecting errors and flaws in the source code. The Linux kernel Makefile can be invoked with options to enable the Sparse source code checker to run on all source files, or only on the recompiled files. Compile the kernel with the enabled source code checker, find errors, and fix them as needed.
Fix the Syzbot null pointer dereference and WARN bug reports which include the reproducer to analyze. Run the reproducer to see if you can reproduce the problem. Look ​​​at the crash report and walk through sources for a possible cause. You might be able to fix problems.
Look for opportunities to add/update .gitignore files for tools and Kselftest. Build tools and Kselftest and run git status. If there are binaries, then it is time to add a new .gitignore file and/or an entry to an existing .gitignore file.
Run mainline kernels built with the CONFIG_KASAN, CONFIG_KMSAN, CONFIG_UBSAN, locking debug options mentioned earlier in the debugging section, and report problems if you see any. This gives you an opportunity to debug and fix problems. The community welcomes fixes and bug reports.