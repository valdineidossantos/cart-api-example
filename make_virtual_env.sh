echo "Adding virtual environment"
python -m venv .venv
echo "choice virtual environment to activate"
source .venv/bin/activate
echo "Install python depencencies libs controler"
pip install poetry
echo "Installing requirements in local"
poetry install
