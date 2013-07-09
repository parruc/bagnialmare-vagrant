user_reqs:
    pkg:
        - installed
        - names:
            - vim
            - less
            - screen
            - locate

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
        - system: True
        - require:
            - group: group_{{ user_name }}

    {% if 'home_path' in user %}
user_home_{{ user_name }}:
    file.directory:
        - name: {{ user.home_path }}
        - makedirs: True
        - user: {{ user.name }}
        - group: {{ user.group }}
        - require:
            - user: user_{{ user_name }}

user_with_home_{{ user_name }}:
    user.present:
        - name: {{ user.name }}
        - home: {{ user.home_path }}
        - require:
            - user: user_{{ user_name }}
            - file: user_home_{{ user_name }}

bashrc_{{ user_name }}:
    file.managed:
        - name: {{ user.home_path }}/.bashrc
        - source: salt://users/.bashrc
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 640
        - replace: True
        - makedirs: True
        - require:
            - user: user_{{ user_name }}

vimrc_{{ user_name }}:
    file.managed:
        - name: {{ user.home_path }}/.vimrc
        - source: salt://users/.vimrc
        - makedirs: True
        - replace: True
        - require:
            - pkg: user_reqs
            - user: user_{{ user_name }}
    {% endif %}
{% endfor %}
