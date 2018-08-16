DESTDIR=
PREFIX=/usr
SYSCONFDIR=/etc

NPM:=$(shell which npm)
SYSTEMCTL:=$(shell which systemctl)

install:
	if test -x "$(SYSTEMCTL)" && test -d "$(DESTDIR)$(SYSCONFDIR)/systemd/system"; then install -m0644 rpi-ac-controller.service $(DESTDIR)$(SYSCONFDIR)/systemd/system/rpi-ac-controller.service && $(SYSTEMCTL) daemon-reload; else echo "could not find systemd"; fi
	if test -e "$(DESTDIR)$(SYSCONFDIR)/systemd/system/rpi-ac-controller.service" && test ! -e "$(DESTDIR)$(SYSCONFDIR)/systemd/system/multi-user.target.wants/rpi-ac-controller.service"; then $(SYSTEMCTL) enable rpi-ac-controller.service && $(SYSTEMCTL) start rpi-ac-controller.service; else echo "rpi-ac-controller daemon is already enabled"; fi
