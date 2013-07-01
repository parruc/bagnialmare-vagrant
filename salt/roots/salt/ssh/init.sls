/root/.ssh/known_hosts:
    file.managed:
        - user: root
        - group: root
        - mode: 700
        - makedirs: True

bitbucket.org:
    ssh_known_hosts:
        - present
        - user: root
        - fingerprint: 97:8c:1b:f2:6f:14:6b:5c:3b:ec:aa:46:46:74:7c:40
    require:
        - file: /root/.ssh/known_hosts
