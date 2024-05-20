.PHONEY: all

publish:
        @echo "publish - publish client and server"
        @./scripts/roll_version.py
        @cd client && npm run build && npm publish
        @cd server && poetry build && poetry publish
