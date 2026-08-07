python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
pytest -n 2 --reruns 1
allure generate ./allure-results/ -o ./allure-report/ --clean
