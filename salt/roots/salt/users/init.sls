{% for user_name, user in pillar['users'].iteritems() %}

group_{{ user_name }}:
    group.present:
        - name: {{ user.group }}

user_{{ user_name }}:
    user.present:
        - name: {{ user.name }}
        - password: {{ user.pass }}
        - groups:
            - {{ user.group }}
        - shell: /bin/bash
{% if home_path in user %}
        - home: {{ user.home_path }}
        - create_home: True
{% endif %}
        - system: True
        - require:
            - group: group_{{ user_name }}
{% endfor %}
