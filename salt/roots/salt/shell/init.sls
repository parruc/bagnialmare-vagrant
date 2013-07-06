shell_reqs:
    pkg:
        - installed
        - names:
            - vim
            - less
            - screen
            - locate

/home/vagrant/.vimrc:
    file.managed:
        - source: salt://shell/vimrc
        - makedirs: True
        - replace: True
        - require:
            - pkg: shell_reqs
