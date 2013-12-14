import os
import shutil
import operator
import re
from collections import OrderedDict
from django.db.models import signals
from django.conf import settings
from django.utils.translation import get_language, activate, deactivate

from whoosh import fields, index, qparser, sorting, query

from bagni.models import Bagno

WHOOSH_SCHEMA = fields.Schema(id=fields.ID(stored=True, unique=True),
                              text=fields.TEXT,
                              services=fields.IDLIST(stored=True, expression=re.compile(r"[^#]+"),),
                              languages=fields.IDLIST(stored=True, expression=re.compile(r"[^#]+"),),
                              )

LANGS = [l[0] for l in settings.LANGUAGES]

def index_path(lang):
    return os.path.join(settings.WHOOSH_INDEX, lang)

def create_index(sender=None, langs=LANGS, **kwargs):
    """ Creates the index schema (no data at this point)
    """
    for lang in langs:
        if not os.path.exists(index_path(lang)):
            os.mkdir(index_path(lang))
            index.create_in(index_path(lang), schema=WHOOSH_SCHEMA)


def delete_index(sender=None, langs=LANGS, **kwargs):
    """ Deletes the index schema and eventually the contained data
    """
    for lang in langs:
        if os.path.exists(index_path(lang)):
            shutil.rmtree(index_path(lang))


def recreate_index(sender=None, langs=LANGS, **kwargs):
    """ Deletes the index schema and eventually the contained data
        and rebuilds the index schema (no data at this point)
    """
    delete_index(sender=sender, langs=langs, **kwargs)
    create_index(sender=sender, langs=langs, **kwargs)


def update_index(sender, langs=LANGS, **kwargs):
    """ Adds/updates an entry in the index. It's connected with
        the post_save signal of the Object objects so will automatically
        index every new or modified Object
    """
    for lang in langs:
        ix = index.open_dir(index_path(lang))
        # TODO: Verificare se poi mi cambia lingua
        activate(lang)
        writer = ix.writer()
        obj = kwargs['instance']
        if kwargs['created']:
            writer.add_document(**obj.index_features())
        else:
            writer.update_document(**obj.index_features())
        deactivate()
        writer.commit()

signals.post_save.connect(update_index, sender=Bagno)


def recreate_data(sender=None, langs=LANGS, **kwargs):
    """ Readds all the Object in the index. If they already exists
        will be duplicated
    """
    for lang in langs:
        ix = index.open_dir(index_path(lang))
        writer = ix.writer()
        activate(lang)
        for obj in Bagno.objects.all():
            writer.add_document(**obj.index_features())
        deactivate()
        writer.commit()


def recreate_all(sender=None, langs=LANGS, **kwargs):
    """ Deletes the schema, creates it back and recreate all the data
        Good to create from scratch or for schema/data modification
    """
    recreate_index(sender=sender, langs=langs, **kwargs)
    recreate_data(sender=sender, langs=langs,**kwargs)

#signals.post_syncdb.connect(recreate_all)


def search(q, filters, groups, query_string, max_facets=5):
    """ Search for a query term and a set o filters
        Returns a list of hits and the representation of the facets
        TODO: Finetune of the fuzzy search
    """
    lang = get_language()
    ix = index.open_dir(index_path(lang))
    hits = []
    facets = [sorting.FieldFacet(g, allow_overlap=True, maptype=sorting.Count) for g in groups]
    # Commented due to a boost error
    # og = qparser.OrGroup.factory(0.5)
    parser = qparser.QueryParser("text", schema=ix.schema) # , group=og)
    #parser.remove_plugin_class(qparser.WildcardPlugin)
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
        facets = OrderedDict()
        active_facets = []
        for group in groups:
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

                out_group = group
                if group == 'services':
                    facet_name, out_group = facet_name.split("@")
                facet_dict = {
                    'name': facet_name,
                    'count': facet_value,
                    'url': url,
                }
                if state == 'active':
                    facet_dict['group'] = out_group
                    active_facets.append(facet_dict)
                if not out_group in facets:
                    facets[out_group] = []
                if len(facets[out_group]) < max_facets:
                    facets[out_group].append(facet_dict)
    return hits, facets, active_facets
