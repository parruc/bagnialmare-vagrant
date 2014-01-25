git_reqs:
    pkg:
        - installed
        - names:
            - git

{% for repo_name, repo in pillar['git'].repos.iteritems() %}
{% set user = pillar['users'][repo_name] %}


git_ssh_folder_{{ repo_name }}:
    file.directory:
        - name: {{ user.home_path }}/.ssh
        - user: {{ user.name }}
        - group: {{ user.group }}
        - dir_mode: 700
        - makedirs: True
        - require:
            - file: user_with_home_{{ repo_name }}

git_key_{{ repo_name }}:
    file.managed:
        - name: {{ user.home_path }}/.ssh/id_rsa
        - source: salt://git/id_rsa
        - user: {{ user.name }}
        - group: {{ user.group }}
        - mode: 600
        - makedirs: True
        - replace: True
        - require:
            - file: user_with_home_{{ repo_name }}
            - file: git_ssh_folder_{{ repo_name }}

git_pub_key_{{ repo_name }}:
    file.managed:
        - name: {{ user.home_path }}/.ssh/id_rsa.pub
        - source: salt://git/id_rsa.pub
        - user: {{ user.name }}
        - group: {{ user.group }}
        - mode: 600
        - makedirs: True
        - replace: True
        - require:
            - file: user_with_home_{{ repo_name }}
            - file: git_ssh_folder_{{ repo_name }}

known_hosts_{{ repo_name }}:
    file.managed:
        - name: {{ user.home_path }}/.ssh/known_hosts
        - user: {{ user.name }}
        - group: {{ user.group }}
        - mode: 700
        - makedirs: True
        - replace: True
        - require:
            - file: user_with_home_{{ repo_name }}
            - file: git_ssh_folder_{{ repo_name }}

known_bitbucket_{{ repo_name }}:
    ssh_known_hosts.present:
        - name: bitbucket.org
        - config: {{ user.home_path }}/.ssh/known_hosts
        - user: {{ user.name }}
        - fingerprint: 97:8c:1b:f2:6f:14:6b:5c:3b:ec:aa:46:46:74:7c:40
        - require:
            - file: user_with_home_{{ repo_name }}
            - file: known_hosts_{{ repo_name }}

known_github_{{ repo_name }}:
    ssh_known_hosts.present:
        - name: github.com
        - config: {{ user.home_path }}/.ssh/known_hosts
        - user: {{ user.name }}
        - fingerprint: 16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48
        - require:
            - file: user_with_home_{{ repo_name }}
            - file: known_hosts_{{ repo_name }}

git_checkout_{{ repo_name }}:
    git.latest:
        - name: {{ repo.url }}
        - target: {{ repo.path }}
        - user: {{ user.name }}
        - force: True
        - identity: {{ user.home_path }}/.ssh/id_rsa
        - require:
            - pkg: git_reqs
            - file: git_key_{{ repo_name }}
            - file: git_pub_key_{{ repo_name }}
            - ssh_known_hosts: known_bitbucket_{{ repo_name }}
            - ssh_known_hosts: known_github_{{ repo_name }}


git_upstream_{{repo_name}}:
    cmd.run:
        - name: git branch --set-upstream master origin/{{ repo.rev }}
        - user: {{ user.name }}
        - cwd: {{ repo.path }}


git_{{ repo_name }}:
    git.latest:
        - name: {{ repo.url }}
        - target: {{ repo.path }}
        - user: {{ user.name }}
        - identity: {{ user.home_path }}/.ssh/id_rsa
        - require:
            - cmd: git_upstream_{{repo_name}}

{% endfor %}
