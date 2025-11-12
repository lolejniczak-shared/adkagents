sudo apt update
sudo apt install python3-venv

python -m venv myenv
source myenv/bin/activate

cd adkagents
pip install -r requirements.txt

Important:
1/ For every agent go to agent definition and rename .env.template to .env
2/ cd Make sure to use your owne project etc.
