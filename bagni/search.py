import os
import shutil
import operator
import re

from django.db.models import signals
from django.conf import settings

from whoosh import fields, index, qparser, sorting, query

from bagni.models import Bagno

WHOOSH_SCHEMA = fields.Schema(id=fields.ID(stored=True, unique=True),
                              name=fields.TEXT(stored=True),
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

signals.post_syncdb.connect(recreate_index)

def update_index(sender, **kwargs):
    ix = index.open_dir(settings.WHOOSH_INDEX)
    writer = ix.writer()
    obj = kwargs['instance']
    if kwargs['created']:
        writer.add_document(id=unicode(obj.slug), name=unicode(obj.name),
                            text=obj.index_text(), city=unicode(obj.city),
                            services=unicode(obj.index_services(sep="#")),
        )
    else:
        writer.update_document(id=unicode(obj.slug), name=unicode(obj.name),
                            text=obj.index_text(), city=unicode(obj.city),
                            services=unicode(obj.index_services(sep="#")),
        )
    writer.commit()

signals.post_save.connect(update_index, sender=Bagno)

def recreate_data(sender=None, **kwargs):
    ix = index.open_dir(settings.WHOOSH_INDEX)
    writer = ix.writer()
    for obj in Bagno.objects.all():
        writer.add_document(id=unicode(obj.slug), name=unicode(obj.name),
                            text=obj.index_text(), city=unicode(obj.city),
                            services=unicode(obj.index_services(sep="#")),
        )
    writer.commit()

def rebuild_index(sender=None, **kwargs):
    recreate_index(sender=sender, **kwargs)
    recreate_data(sender=sender, **kwargs)

def search(q, filters, groups, query_string, max_facets=10):
    ix = index.open_dir(settings.WHOOSH_INDEX)
    hits = []
    facets = [sorting.FieldFacet(g, allow_overlap=True, maptype=sorting.Count) for g in groups]
    og = qparser.OrGroup.factory(0.9)
    parser = qparser.QueryParser("text", schema=ix.schema, group=og)
    parser.remove_plugin_class(qparser.WildcardPlugin)
    parser.add_plugin(qparser.FuzzyTermPlugin())
    fuzzy = "~1/2 "
    q = fuzzy.join(q.split(" ")) + fuzzy
    print q
    try:
        q = parser.parse(q)
    except:
        q = None
    if q is not None:
        searcher = ix.searcher()
        for filter in filters:
            filter_name, filter_value = filter.split(":", 1)
            q = q & query.Term(filter_name, filter_value)
        hits = searcher.search(q.normalize(), groupedby=facets)
        facets = {}
        for group in groups:
            facets[group] = []
            sorted_facets = sorted(hits.groups(group).items(),
                   key=operator.itemgetter(1, 0),
                   reverse=True)[:max_facets]
            for facet_name, facet_value in sorted_facets:
                qs = query_string.copy()
                filter = group + ":" + facet_name
                if filter in filters:
                    qs.setlist('f', [f for f in filters if f != filter])
                    active = "active"
                else:
                    qs.appendlist('f', filter)
                    active = ""
                url = qs.urlencode(safe=":")
                facets[group].append({
                    'name': facet_name,
                    'count': facet_value,
                    'url': url,
                    'class': active,
                    }
                )
    return hits, facets

