source venv/bin/activate

rm -r dist

python3 setup.py bdist_wheel

pip3 install -U dist/*
