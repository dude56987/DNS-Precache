show:
	echo 'Run sudo make install to install the program'
run:
	sudo python dns-precache.py
install: build
	sudo gdebi --non-interactive dns-precache_UNSTABLE.deb
uninstall:
	sudo apt-get purge dns-precache
build: 
	sudo make build-deb;
build-deb:
	mkdir -p debian;
	mkdir -p debian/DEBIAN;
	mkdir -p debian/usr;
	mkdir -p debian/usr/bin;
	mkdir -p debian/etc/dns-precache;
	# copy over the binary
	cp -vf dns-precache.py ./debian/usr/bin/dns-precache
	# copy over the config files
	cp -vf default.list ./debian/etc/dns-precache
	cp -vf top500.list ./debian/etc/dns-precache
	# make the program executable
	chmod +x ./debian/usr/bin/dns-precache;
	# Create the md5sums file
	find ./debian/ -type f -print0 | xargs -0 md5sum > ./debian/DEBIAN/md5sums
	# cut filenames of extra junk
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*\\n//g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*//g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	# figure out the package size	
	du -sx --exclude DEBIAN ./debian/ > Installed-Size.txt
	# copy over package data
	cp -rv debdata/. debian/DEBIAN/
	# fix permissions in package
	chmod -Rv 775 debian/DEBIAN/
	chmod -Rv ugo+r debian/
	chmod -Rv go-w debian/
	chmod -Rv u+w debian/
	# build the package
	dpkg-deb --build debian
	cp -v debian.deb dns-precache_UNSTABLE.deb
	rm -v debian.deb
	rm -rv debian
