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
```

Update to the mainline kernel

```
pacman -S - < system-packages.txt
```

Reboot server, and log in as `astrogruff` and then install
the useful packages

```
yay -S - < useful-packages.txt
```

# Setup astrogruff user with ZSH

Set default shell to zsh:

```
chsh --shell /bin/zsh astrogruff
```

Copy `.zshrc` to `${HOME}` setup `zsh`. Log out and back in
to have `zsh` being the default shell.

# Setup VNC / noVNC

Install the `vnc` packages using:

```
yay -S - < vnc-packages.txt
```

To enable the `vnc` to come up as part of the X11 startup need to add
an autologin for the sddm (see above and in the SDDM wiki), using a dummy screen ()

Copy the `xorg-conf-headless.conf` to `/etc/X11/xorg.conf.d/05-headless.conf`

As `astrogruff` set the VNC password via

```
x11vnc -storepasswd
```

* copy the `vnc-config` file `~/.vnc/config`
* copy the `x11vnc-service-override.conf` to `/etc/systemd/system/x11vnc.service.d/override.conf`
* enable the `x11vnc.service` using the following commands:

```
sudo systemctl daemon-reload
sudo systemctl enable --now x11vnc.service
```

## TODO - document novnc
* nginx install and config

Copy `novnc.service` to `/etc/systemd/system` and then enable service:

```
sudo systemctl daemon-reload
sudo systemctl enable --now novnc.service
```

# Setting up Astro parts

Install the astro packages with:

```
yay -S - < astro-packages.txt
```

* copy the `udev-custom.rules` to `/etc/udev/rules.d/49-custom.rules`

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

Copy `gpsd` to `/etc/defaults/gpsd`

Enable the `gpsd.socket` with:

```
sudo systemctl enable --now gpsd.socket
```

## Desktop setup

Install `desktop-packages.txt`

```
yay -S - < desktop-packages.txt
```

* set compositor to `XRender`

|Setting|Package|
|-------|-------|
|Global Theme|Infinity-Global|

The addons will allow for a picture of the day (POTD) wallpaper, the **Unsplash Wallpapers** with
the galaxy theme

Install favourite theme, but get the `candy-icons` as they are great with a dark theme

# Setting up WiFi Hotspot

<TODO - use the linux-wifi-hotspot and set up service>
