[![Build Status](https://travis-ci.org/CSCfi/ansible-role-rally.svg?branch=master)](https://travis-ci.org/CSCfi/ansible-role-rally)

# ansible-role-rally

This role does a basic installation of openstack-rally for the "rally" user. Currenly it has minor configuration capabilities for the rally tempest options.

This role doesn't do much itself. The "ansible-role-rally-scenarios" role can configure rally deployments and tempest verifiers. 

## Configuration options

Plese see defaults/main.yml for configuration options.

## Usage
```
---
- name: Configure rally
  hosts: rally_server
  become: true
  roles:
    - ansible-role-rally
    - ansible-role-rally-scenarios
  environment: "{{ proxy_env }}"
```
