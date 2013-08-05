pg:
    ssl: 'false'
    dbs:
        ombrelloni:
            name: 'ombrelloni'
            geo: True
            owner: 'ombrelloni'
            pass: 'z?;YQcg-{*aL;ZZHeS"m9gJ}>c;d[m,aGD;e9y3a'
            can_create: False
            custom_psql: 'GRANT SELECT ON geometry_columns TO ombrelloni;GRANT SELECT ON geography_columns TO ombrelloni;GRANT SELECT ON spatial_ref_sys TO ombrelloni;'
        test_ombrelloni:
            name: 'test_ombrelloni'
            geo: True
            owner: 'test_ombrelloni'
            pass: 'z?;YQcg-{*aL;ZZHeS"m9gJ}>c;d[m,aGD;e9y3a'
            can_create: True
