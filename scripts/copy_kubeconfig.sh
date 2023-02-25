#!/bin/bash

# exit on errors
set -e

config_path=${1:-"${HOME}/.kube/config"}

[[ -z "${SSH_USER}" ]] && SSH_USER="vagrant"
[[ -z "${SSH_USER_PASS}" ]] && SSH_USER_PASS="vagrant"
[[ -z "${SSH_PORT}" ]] && SSH_PORT="2000"
[[ -z "${SSH_HOST}" ]] && SSH_HOST="127.0.0.1"

echo connecting to "${SSH_USER}@${SSH_HOST}:${SSH_PORT}"..
vagrant ssh -c "sudo install -C -m 600 -o vagrant -g vagrant /etc/rancher/k3s/k3s.yaml ./config" >/dev/null 2>&1

echo connection success..

echo copying k3s kubeconfig to "${config_path}"
sshpass -p "${SSH_USER_PASS}" scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -P "${SSH_PORT}" "${SSH_USER}@${SSH_HOST}":~/config "${config_path}" >/dev/null 2>&1

# remove config file from guest machine vagrant home directory
vagrant ssh -c "rm -rf ~/config" >/dev/null 2>&1
