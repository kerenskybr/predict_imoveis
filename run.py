import os

from predictimoveis import app

if __name__ == "__main__":
	#app.run(debug=True)

	#For heroku
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)