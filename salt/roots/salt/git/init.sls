git_reqs:
    pkg:
        - installed
        - names:
            - git
{% for repo_name, repo in pillar['pg'].repos.iteritems() %}
git_{{ repo_name }}:
    git.latest:
        - name: {{ repo.url }}
        - rev: {{ repo.branch }}
        - target: {{ repo.path }}
        - force: True
    require:
        - pkg: git_reqs
{% endfor %}
