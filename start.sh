data_path="./app/temp"
out_path="./app/out"
flask_app="app/app.py"

mkdir -p $data_path
mkdir -p $out_path

export FLASK_APP=$flask_app
exec flask run