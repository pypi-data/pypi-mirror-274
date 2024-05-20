.PHONEY: dist run_dev

dist: package.json
	npm run build
	npx generate-license-file --input package.json --output dist/client-third-party-licenses.txt --overwrite

run_dev:
	npm run dev
