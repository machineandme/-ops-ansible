# -ops-ansible

## Write playbook

About ansible playbooks [here.](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html)

```yaml
---
- name: Hello example
  hosts: all
  tasks:
    - name: Send hello to server
      shell: echo hello server
```

Will execute on **every** server avaliable. Include production. Not recomended to use.

## Write playbook for any project server

```yaml
---
- name: Hello example
  hosts: sampleProject
  tasks:
    - name: Send hello to sampleProject server
      shell: echo hello sampleProject server
```

Will execute on test and production server of sampleProject.

## Write playbook for test server

```yaml
---
- name: Hello example
  hosts: sampleProject:&test
  tasks:
    - name: Send hello to sampleProject test server
      shell: echo hello sampleProject test server
```

Will execute only on test server of sampleProject.

## Write playbook for prod server

```yaml
---
- name: Hello example
  hosts: sampleProject:&prod
  tasks:
    - name: Send hello to sampleProject prod server
      shell: echo hello sampleProject prod server
```

Will execute only on production server of sampleProject.


## Github action

Add to repository secrets:
1. `githubPAT` - github personal access token
2. `sshKey` - allowed ssh key for target machine
3. `sshPubKey` - public key for `sshKey`

```yaml
name: Release
on:
  release:
    types: [released]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          token: "${{ secrets.githubPAT }}"
          submodules: recursive

      - name: Write ssh key
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.sshKey }}" > ~/.ssh/id_rsa
          echo "${{ secrets.sshPubKey }}" > ~/.ssh/id_rsa.pub
          chmod 600 ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa.pub

      - name: Install Taskfile.dev deb
        run: |
          wget https://github.com/go-task/task/releases/download/v3.0.0/task_linux_amd64.deb
          sudo dpkg -i ./task_linux_amd64.deb

      # - name: Ansible some playbook
      #   run: ansible-playbook ../playbooks/example.yaml
      #   working-directory: -ops-ansible
```

## Refresh inventory

Get the digital ocean api key and run with `{{it}}` in env build_inventory python file.

```sh
git pull
```
```sh
env DO_API_KEY={{it}} python3 build_inventory.py
```
```sh
git add inventory.yaml
```
```sh
git commit -m "New inventory file generated from Digital Ocean API."
```
```sh
git push
```