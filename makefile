setup:
	pip install -r requirements.txt
	npm install
	cd frontend
	bower install

run:
	cd backend
	nodemon server.js
