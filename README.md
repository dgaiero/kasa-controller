# Kasa Light Controller

After cloning the repository, create the virtual environment

Please note, this readme assumes the repository was cloned to `/var/bin/light-controller`

```shell
python3 -m venv lc
source lc/bin/activate
pip install -r requirements.txt
```

This repository was tested on Python 3.9, but an earlier of python *should* work.
Make sure that the virtual environment is named `lc` since that is what the startup
script uses.

To inject this into the system path, edit `/etc/profile` and add the following line
below the existing `PATH` manipulation:

```shell
PATH="$PATH:/var/bin/light-controller";export PATH
```

To make the script run after the last uesr logs out, you need to edit
`/etc/pam.d/sshd`. Add the following line:

```shell
# Execute the login/logoff scripts
session    optional     pam_exec.so quiet /etc/pam_session.sh
```

Then, symlink the `pam_session.sh` file in this repository to `/etc/pam_session.sh`:

```shell
ln -s /var/bin/light-controller/pam_session.sh /etc/pam_session.sh
```

Lastly, make sure that both `light` and `pam_session.sh` are given executable
permissions:

```shell
chmod a+x light pam_session.sh
```

The main Python file, `LightControl.py` takes in one positional argument and one
optional argument. The positional argument tells the program whether to turn the
light `on` or `off`. The optional argument tells the program what level of
debugging to provide. Additionally, an IP address can be provided with the `-ip`
flag. If an IP address is not provided, the program will read the environment
variable `LIGHT_CONTROL_IP_ADDR`. You can optionally make a `.env` file in the
repository directory:

```shell
echo LIGHT_CONTROL_IP_ADDR=XX.XX.XX.XX >> .env # replace XX.XX.XX.XX with your IP address
```

```shell
usage: light [-h] [--verbose] [-ip IP] {on,off}

positional arguments:
  {on,off}

optional arguments:
  -h, --help     show this help message and exit
  --verbose, -v
  -ip IP         IP address of smart plug
```
