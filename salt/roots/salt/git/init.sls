git_reqs:
    pkg:
        - installed
        - names:
            - git

git_key:
    file.managed:
        - name: /root/.ssh/git_key
        - source: salt://git/id_rsa
        - user: root
        - group: root
        - mode: 600
        - replace: True

known_hosts:
    file.managed:
        - name: /root/.ssh/known_hosts
        - user: root
        - group: root
        - mode: 700
        - makedirs: True

known_bitbucket:
    ssh_known_hosts:
        - name: bitbucket.org
        - present
        - user: root
        - fingerprint: 97:8c:1b:f2:6f:14:6b:5c:3b:ec:aa:46:46:74:7c:40
    require:
        - file: known_hosts


{% for repo_name, repo in pillar['git'].repos.iteritems() %}
git_{{ repo_name }}:
    git.latest:
        - name: {{ repo.url }}
        - rev: {{ repo.branch }}
        - target: {{ repo.path }}
        - force: True
        - identity: /root/.ssh/git_key
    require:
        - pkg: git_reqs
        - file: git_key
        - ssh_known_hosts: known_bitboucket
{% endfor %}
