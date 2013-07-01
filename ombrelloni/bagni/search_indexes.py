from haystack import indexes
from bagni.models import Bagno


class BagnoIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name')
    city = indexes.CharField(model_attr='city')
    text = indexes.EdgeNgramField(document=True, use_template=True)

    services = indexes.FacetMultiValueField()
    # Other field definitions


    def prepare_services(self, object):
        values = list()
        for service in object.services.all():
            values.append(service.name)
        return values

    def get_model(self):
        return Bagno

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
