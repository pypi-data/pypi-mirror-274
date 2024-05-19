rmdir /S /Q dist

pip install .
pip install pyinstaller

pyinstaller --name "euc2mqtt" --console --onefile entry_point.py