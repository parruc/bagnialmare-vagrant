import os
import operator
import re

from django.db.models import signals
from django.conf import settings

from whoosh import fields, index, qparser, sorting, query
from whoosh.filedb.filestore import FileStorage

from bagni.models import Bagno

WHOOSH_SCHEMA = fields.Schema(id=fields.ID(stored=True, unique=True),
                              name=fields.TEXT(stored=True),
                              text=fields.TEXT,
                              city=fields.ID(stored=True, ),
                              services=fields.IDLIST(stored=True, expression=re.compile("#")),
                            )

def create_index(sender=None, **kwargs):
    if not os.path.exists(settings.WHOOSH_INDEX):
        os.mkdir(settings.WHOOSH_INDEX)
        storage = FileStorage(settings.WHOOSH_INDEX)
        return index.Index(storage, schema=WHOOSH_SCHEMA, create=True)

signals.post_syncdb.connect(create_index)

def update_index(sender, obj, created, **kwargs):
    ix = index.open_dir(settings.WHOOSH_INDEX)
    writer = ix.writer()
    if created:
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

def search(q, filters, groups, query_string, max_facets=10):
    ix = index.open_dir(settings.WHOOSH_INDEX)
    hits = []
    facets = [sorting.FieldFacet(g, allow_overlap=True, maptype=sorting.Count) for g in groups]
    og = qparser.OrGroup.factory(0.9)
    parser = qparser.QueryParser("text", schema=ix.schema, group=og)
    parser.remove_plugin_class(qparser.WildcardPlugin)

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

