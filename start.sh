data_path="./app/temp"
out_path="./app/out"
app_dir="app/"

mkdir -p $data_path
mkdir -p $out_path

pip3 install -r "./requirements.txt"
export FLASK_APP=$app_dir"app.py"
exec flask run