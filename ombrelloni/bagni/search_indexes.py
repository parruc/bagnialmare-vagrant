from haystack import indexes
from bagni.models import Bagno


class BagnoIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name')
    city = indexes.CharField(model_attr='city')
    text = indexes.EdgeNgramField(document=True, use_template=True)

    services = indexes.FacetMultiValueField()
    # Other field definitions


    def prepare(self, obj):
        data = super(BagnoIndex, self).prepare(obj)
        data['services'] = list()
        for service in obj.services.all():
            data['services'].append(service.name)
        return data

    def get_model(self):
        return Bagno

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
