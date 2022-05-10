# This should run on the server and deploy the ansible playbook on demand
cd ${HOME}/encyclo-flower/server
git fetch origin main
git reset --hard origin/main

ansible-galaxy role install -r requirements.yml --force
ansible-galaxy collection install -r requirements.yml --force
ansible-playbook -i hosts playbook.yml
