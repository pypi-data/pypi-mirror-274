.PHONEY: all build_deb

all:
	@echo "make targets:"
	@echo " * build_deb - make an x86 debian installable package"

build_deb:
	@echo "Build Package"
	@./scripts/roll_version.py
	@rm -rf apt/usr/local/bin
	@rm -rf apt/opt/{{ project }}
	@umask 0022
	@mkdir -p apt/usr/local/bin
	@mkdir -p apt/opt/{{ project }}/scripts
	@mkdir -p apt/opt/{{ project }}/web
	@mkdir -p dist
	@cd server; make dist
	@cd client; make dist
	@cp server/scripts/make_keys.sh apt/opt/{{ project }}/scripts/
	@cp -r server/dist/{{ project }} apt/opt/{{ project }}
	@cp -r server/dist/server-third-party-licenses.txt apt/opt/{{ project }}
	@cp -r client/dist/client-third-party-licenses.txt apt/opt/{{ project }}
	@cp -r client/dist/* apt/opt/{{ project }}/web
	@cd apt/usr/local/bin && ln -sf /opt/{{ project }}/{{ project }} .
	@dpkg-deb --build --root-owner-group apt dist