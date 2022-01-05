#!/bin/bash

echo "Usage: Triple tap with mouse on any line then Copy/Paste on target shell"
echo
echo '>>>-----------------------------------------------------<<<'
echo "[*] Upgrade shell"
echo "[*] which python / script ??? "
echo
echo "which python || which python3 || which script"
echo "Using python/python3"
echo "\`which python\` -c 'import pty;pty.spawn(\"/bin/bash\")' || \`which python3\` -c 'import pty;pty.spawn(\"/bin/bash\")' || \`which script\` -qc /bin/bash /dev/null"
echo
echo "Press <CTRL> + Z"
echo
echo ">>>=====================================================<<<"
echo
echo "echo $TERM; stty -a # Not compulsory"
echo "stty raw -echo; fg # Press <ENTER> Twice or use the reset command"
echo 
echo "export TERM=xterm-256color"
echo "export SHELL=/bin/bash"
echo "stty rows 56 columns 238 # Change values according to your terminal size"
echo "alias ls='ls -la --color=auto'"
echo
echo '>>>-----------------------------------------------------<<<'
echo "[*] Colors??? Yes pls [Experimental] "
echo "May cause issues with some shells such as zsh"
echo
echo "PS1='\[\e[0;36m\]|\t| \${debian_chroot:+(\$debian_chroot)}\[\033[01;35m\]\u\[\033[01;36m\]@\[\033[01;32m\]\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '"
echo
echo ">>>=====================================================<<<"