.PHONEY: all dist run_dev

dist: src/version.py exe
	poetry install && pyinstaller orbit.spec --noconfirm 
	poetry export -f requirements.txt --without-hashes > requirements.txt
	python -m third_party_license_file_generator \
		-g \
		-r requirements.txt \
		-o dist/server-third-party-licenses.txt \
		-p ~/.pyenv/shims/python3
	rm requirements.txt

exe:
	@mkdir -p nltk_data
	@python3 -m nltk.downloader -d ./nltk_data stopwords
	@python3 -m nltk.downloader -d ./nltk_data punkt
	pyinstaller orbit.spec --noconfirm

run_dev:
	python -m src --dev --run

