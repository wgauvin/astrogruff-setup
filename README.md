Astrogruff (Manjaro RPi4)
=========================

This is the instructions for what I used to set up an ArchLinux RPi used
for my astrophotography

# Install Manjaro RPi4

Download latest Manjaro RPi4 build available from (https://manjaro.org/downloads/arm/raspberry-pi-4/arm8-raspberry-pi-4-kde-plasma/)
Burn this to a microSD card using Etcher.

To do a headless install, make sure it's connected to the network with an ethernet cable and ssh into it via
it's IP address and using the `root` user. Follow the install script to set things up. This will set the locale,
create users, change root passwd.

Update the mirror list and then the system, helps speed things up.

```
pacman-mirrors -aS unstable
pacman-mirrors --geoip
pacman -Syyuu
pacman -S git
```

The git package is needed to this repo can be checked out locally on the
server. With the `astrogruff` user checkout out this repo

```
git clone https://github.com/wgauvin/astrogruff-setup.git
```

Setup up the base system with the base system packages, including
using the `linux-rpi4-mainline` kernel.

```
pacman -S - < packages/system-packages.txt
```

Reboot server, and log in as `astrogruff` and then install
the useful packages.

```
yay -S - < packages/useful-packages.txt
```

# Setup astrogruff user with ZSH

Set default shell to zsh:

```
chsh --shell /bin/zsh astrogruff
```

From this repo, copy `astrogruff/.zshrc` to `${HOME}` setup `zsh`. Log out
and back in to have `zsh` being the default shell.

# Setup VNC / noVNC

Install the `vnc` packages using:

```
yay -S - < packages/vnc-packages.txt
```

To enable the `vnc` to come up as part of the X11 startup need to add
an autologin for the sddm (see above and in the SDDM wiki), using a dummy screen ()

Copy the contents `etc/X11/xorg.conf.d/` to `/etc/X11/xorg.conf.d/`

As `astrogruff` set the VNC password via

```
x11vnc -storepasswd
```

* copy `astrogruff/.vnc/` file `${HOME}/.vnc/`
* copy `etc/systemd/system/x11vnc.service.d/` to `/etc/systemd/system/x11vnc.service.d/`
* enable the `x11vnc.service` using the following commands:

```
sudo systemctl daemon-reload
sudo systemctl enable --now x11vnc.service
```

Copy `/etc/systemd/system/novnc.service` to `/etc/systemd/system` and then enable service:

```
sudo systemctl daemon-reload
sudo systemctl enable --now novnc.service
```

* TODO - document nginx.conf
* TODO - make sure set up SSL

# Setting up Astro parts

Install the astro packages with:

```
yay -S - < packages/astro-packages.txt
```

Copy all the `udev` rules in  `etc/udev/rules.d` to `/etc/udev/rules.d/`

If there is an issue with parsing the udev rule then none of the rules
would be applied. To check use the following commands:

```
lsusb
sudo udevadm control --reload-rules && sudo udevadm trigger
udevam test $(udevadm info --query=path --name=<path>)
```

Add `astrogruff` to the `uucp` group if it already is not:

```
sudo usermod -a -G uucp astrogruff
```

## Setup of GPSD

Copy `etc/defaults/gpsd` to `/etc/defaults/gpsd`

Enable the `gpsd.socket` with:

```
sudo systemctl enable --now gpsd.socket
```

## Desktop setup

Install `desktop-packages.txt`

```
yay -S - < packages/desktop-packages.txt
```

* set compositor to `XRender`

The addons will allow for a picture of the day (POTD) wallpaper, the **Unsplash Wallpapers** with
the galaxy theme

Install favourite theme, but get the `candy-icons` as they are great with a dark theme

# Setting up WiFi Hotspot

<TODO - use the linux-wifi-hotspot and set up service>
