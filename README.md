## Setup
python -m venv venvtest
source venvtest/bin/activate  # Linux/macOS
venvtest\Scripts\activate     # Windows
pip install -r requirements.txt
pip freeze > requirements.txt
#run
 python test.py


## git with azure devops

git init
git remote add origin https://sujeetkumar2010@dev.azure.com/sujeetkumar2010/DsaWebApp/_git/pythonlangchaindemo
git add .
git commit -m "initial commit"
git push -u origin --all

---below all may be not needed
 git remote -v 
 git remote remove origin

---
 git pull origin main
git checkout main
git pull origin main
git push -u origin main

## git best way
 # code register from local vs code to azure devops repose
go to root folder or project 
#Git Commands
git init
git remote add origin https://dev.azure.com/sujeetkumar2010/DsaWebApp/_git/McpServerAndClient
git pull origin main
git checkout main
git add .
git commit -m "initial commit"
git push -u origin --all