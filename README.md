# Bin (Python edition)

## Installation guide:
1. Clone the repository to your local storage:
```bash
git clone https://github.com/notdankenough/bin.git -b "flask-py"
cd bin
```
2. Set up and activate a virtualenv (You must have installed virtualenv before):
```bash
python3 -m venv venv
. venv/bin/activate
```
3. Download all from `requirements.txt`:
```bash
pip install -r requirements.txt
```
4. Done!

## Start bin as a development server:
```bash
flask --app main --debug run
```

## Start bin as a production server:
According to [Flask documentation (Deploy to Production)](https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/), you need to make these steps:
1. Build a distribution file with wheel:
```bash
pip install wheel
python setup.py bdist_wheel
```
2. Set up a new virtualenv, then install the file with pip:
```bash
pip install flaskr-1.0.0-py3-none-any.whl
```
3. Run `init-db` to create the database in the instance folder:
```bash
flask --app flaskr init-db
```
4. Generate the secret key:
```bash
python -c 'import secrets; print("SECRET_KEY = \"{}\".format(secrets.token_hex()))' >> "venv/var/flaskr-instance/config.py"
```
5. Install WSGI server:
```bash
pip install waitress
```
6. Call the application factory to get an app object:
```bash
waitress-serve --call 'flaskr:create_app'
```
7. Tip: Waitress should not be run as root because it's not secure. Instead, use the nginx/Apache httpd reverse proxy for Waitress.
