shell_reqs:
    pkg:
        - installed
        - names:
            - vim
            - less
            - screen
            - locate

/home/vagrant/.vimrc:
    file:
        - managed
        - source: salt://shell/vimrc
    require:
        - pkg: shell_reqs
