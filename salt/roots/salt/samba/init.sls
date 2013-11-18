samba_reqs:
    pkg:
        - installed
        - names:
            - samba
            - expect

samba_expect:
    file.managed:
        - name: /tmp/samba.expect
        - source: salt://lib/samba.expect
        - user: root
        - mode: 700

samba_user:
    cmd.run:
        - name: /tmp/samba.expect
        - user: root
        - require:
            - file: samba_expect
            - pkg: samba_reqs

samba_process:
    service.running:
        - name: samba
        - user: root
        - reload: true
        - enable: true
        - require:
            - cmd: samba_user