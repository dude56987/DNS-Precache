show:
	echo 'Run sudo make install to install the program'
run:
	sudo python dns-precache.py
install:
	apt-get install firefox --assume-yes
	apt-get install python --assume-yes
	cp dns-precache /usr/bin/dns-precache
	chmod +x /usr/bin/dns-precache
	mkdir /etc/dns-precache
	cp -v addons.conf /etc/dns-precache
	cp -v customSettings.conf /etc/dns-precache
uninstall:
	rm -v /usr/bin/dns-precache
	rm -rv /etc/dns-precache
installed-size:
	du -sx --exclude DEBIAN ./debian/
build: 
	sudo make build-deb;
build-deb:
	mkdir -p debian;
	mkdir -p debian/DEBIAN;
	mkdir -p debian/usr;
	mkdir -p debian/usr/bin;
	mkdir -p debian/etc/dns-precache;
	# make post and pre install scripts have the correct permissions
	chmod 775 debdata/*
	# copy over the binary
	cp -vf dns-precache.py ./debian/usr/bin/dns-precache
	# copy over the config files
	cp -vf default.list ./debian/etc/dns-precache
	cp -vf top500.list ./debian/etc/dns-precache
	# make the program executable
	chmod +x ./debian/usr/bin/dns-precache;
	# start the md5sums file
	md5sum ./debian/usr/bin/dns-precache > ./debian/DEBIAN/md5sums
	# create md5 sums for all the config files transfered over
	md5sum ./debian/etc/dns-precache/* >> ./debian/DEBIAN/md5sums
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	cp -rv debdata/. debian/DEBIAN/
	dpkg-deb --build debian
	cp -v debian.deb dns-precache_UNSTABLE.deb
	rm -v debian.deb
	rm -rv debian
