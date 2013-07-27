import os
import shutil
import operator
import re

from django.db.models import signals
from django.conf import settings

from whoosh import fields, index, qparser, sorting, query

from bagni.models import Bagno

WHOOSH_SCHEMA = fields.Schema(id=fields.ID(stored=True, unique=True),
                              text=fields.TEXT,
                              city=fields.ID(stored=True, ),
                              services=fields.IDLIST(stored=True, expression=re.compile(r"[^#]+")),
                              )


def create_index(sender=None, **kwargs):
    if not os.path.exists(settings.WHOOSH_INDEX):
        os.mkdir(settings.WHOOSH_INDEX)
        return index.create_in(settings.WHOOSH_INDEX, schema=WHOOSH_SCHEMA)


def delete_index(sender=None, **kwargs):
    if os.path.exists(settings.WHOOSH_INDEX):
        shutil.rmtree(settings.WHOOSH_INDEX)


def recreate_index(sender=None, **kwargs):
    delete_index(sender=sender, **kwargs)
    create_index(sender=sender, **kwargs)


def update_index(sender, **kwargs):
    ix = index.open_dir(settings.WHOOSH_INDEX)
    writer = ix.writer()
    obj = kwargs['instance']
    if kwargs['created']:
        writer.add_document(**obj.index_features())
    else:
        writer.update_document(**obj.index_features())
    writer.commit()

signals.post_save.connect(update_index, sender=Bagno)


def recreate_data(sender=None, **kwargs):
    ix = index.open_dir(settings.WHOOSH_INDEX)
    writer = ix.writer()
    for obj in Bagno.objects.all():
        writer.add_document(**obj.index_features())
    writer.commit()


def recreate_all(sender=None, **kwargs):
    recreate_index(sender=sender, **kwargs)
    recreate_data(sender=sender, **kwargs)

signals.post_syncdb.connect(recreate_all)


def search(q, filters, groups, query_string, max_facets=10):
    """Search for a query term and a set o filters
    Returns a list of hits and the representation of the facets
    """
    ix = index.open_dir(settings.WHOOSH_INDEX)
    hits = []
    facets = [sorting.FieldFacet(g, allow_overlap=True, maptype=sorting.Count) for g in groups]
    # Commented due to a boost error
    # og = qparser.OrGroup.factory(0.5)
    parser = qparser.QueryParser("text", schema=ix.schema, )  # group=og)
    parser.remove_plugin_class(qparser.WildcardPlugin)
    # Temporary removed fuzzy search: more pain than benefit
    #parser.add_plugin(qparser.FuzzyTermPlugin())
    #fuzzy = "~1/2 "
    #q = fuzzy.join(q.split(" ")) + fuzzy
    try:
        q = parser.parse(q)
    except:
        q = None
    if q or filters:
        searcher = ix.searcher()
        for filter in filters:
            filter_name, filter_value = filter.split(":", 1)
            q = q & query.Term(filter_name, filter_value)
        hits = searcher.search(q.normalize(), groupedby=facets)
        facets = {}
        for group in groups:
            facets[group] = {'active': [], 'available': []}
            sorted_facets = sorted(hits.groups(group).items(),
                                   key=operator.itemgetter(1, 0),
                                   reverse=True)
            for facet_name, facet_value in sorted_facets:
                if not facet_name:
                    continue
                qs = query_string.copy()
                filter = group + ":" + facet_name
                if filter in filters:
                    qs.setlist('f', [f for f in filters if f != filter])
                    state = "active"
                else:
                    qs.appendlist('f', filter)
                    state = "available"
                url = qs.urlencode(safe=":")

                facets[group][state].append({
                    'name': facet_name,
                    'count': facet_value,
                    'url': url,
                })
                if len(facets[group]['available']) >= max_facets:
                    break
    return hits, facets
