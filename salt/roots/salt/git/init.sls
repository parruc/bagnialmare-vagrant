git_reqs:
    pkg:
        - installed
        - names:
            - git

git_ombrelloni:
    git.latest:
        - name: https://parruc@bitbucket.org/flyingfrog/4hm.git
        - rev: {{ pillar["git_branch"] }}
        - target: {{ pillar["django_path"] }}
        - force: True
    require:
        - pkg: git_reqs
