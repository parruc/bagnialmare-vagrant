user_reqs:
    pkg:
        - installed
        - names:
            - vim
            - less
            - screen
            - locate

user_container:
    file.directory:
        - name: /var/www
        - user: root
        - group: root

{% for user_name, user in pillar['users'].iteritems() %}

    group_{{ user_name }}:
        group.present:
            - name: {{ user.group }}


    {% if 'home_path' in user %}

        user_{{ user_name }}:
            user.present:
                - name: {{ user.name }}
                - password: {{ user.pass }}
                - home: {{ user.home_path }}
                - groups:
                    - {{ user.group }}
                - shell: /bin/bash
                - system: True
                - require:
                    - file: user_container
                    - group: group_{{ user_name }}

        user_with_home_{{ user_name }}:
            file.directory:
                - name: {{ user.home_path }}
                - user: {{ user.name }}
                - group: {{ user.group }}
                - recurse:
                    - user
                    - group
                - require:
                    - user: user_{{ user_name }}


        bash_profile_{{ user_name }}:
            file.managed:
                - name: {{ user.home_path }}/.bash_profile
                - source: salt://users/.bash_profile
                - user: {{ user.name }}
                - group: {{ user.group }}
                - file_mode: 640
                - replace: True
                - makedirs: True
                - require:
                    - file: user_with_home_{{ user_name }}

        vimrc_{{ user_name }}:
            file.managed:
                - name: {{ user.home_path }}/.vimrc
                - source: salt://users/.vimrc
                - makedirs: True
                - replace: True
                - require:
                    - file: user_with_home_{{ user_name }}
    {% else %}
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
    {% endif %}


    {% if grains['configuration'] == 'local' and 'home_path' in user %}
        # Copy vagrant user keys for our user in local so that you can mount
        # development folder as the wanted user
        keys_{{ user_name }}:
            cmd.run:
                - name: "cp /home/vagrant/.ssh/authorized_keys {{ user.home_path }}/.ssh/authorized_keys"
                - user: root
                - require:
                    - file: user_with_home_{{ user_name }}

        keys-permission_{{ user_name }}:
            file.managed:
                - name: {{ user.home_path }}/.ssh/authorized_keys
                - user: {{ user.name }}
                - group: {{ user.group }}
                - file_mode: 700
                - require:
                    - cmd: keys_{{ user_name }}
    {% endif %}

{% endfor %}
