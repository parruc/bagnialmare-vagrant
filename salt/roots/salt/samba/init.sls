samba_reqs:
    pkg:
        - installed
        - names:
            - samba
            - expect

{% for user_name, user in pillar['users'].iteritems() %}
{% if 'home_path' in user %}

samba_expect_{{ user_name }}:
    file.managed:
        - name: /tmp/samba_{{ user_name }}.expect
        - source: salt://samba/samba.expect
        - template: jinja
        - defaults:
            user: {{ user.name }}
            pass: {{ user.pass }}
        - user: root
        - mode: 700

samba_user_{{ user_name }}:
    cmd.run:
        - name: /tmp/samba_{{ user_name }}.expect
        - user: root
        - require:
            - file: samba_expect_{{ user_name }}
            - pkg: samba_reqs
            - user: user_{{ user_name }}
{% endif %}
{% endfor %}

samba_process:
    service.running:
        - name: samba
        - user: root
        - reload: true
        - enable: true
        - require:
            {% for user_name, user in pillar['users'].iteritems() %}
            {% if 'home_path' in user %}
            - cmd: samba_user_{{ user_name }}
            {% endif %}
            {% endfor %}