from haystack import indexes
from bagni.models import Bagno


class BagnoIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name')
    text = indexes.EdgeNgramField(document=True, use_template=True)

    services = indexes.FacetMultiValueField()
    city = indexes.FacetCharField(model_attr='city')
    # Other field definitions

    def prepare_services(self, obj):
        values = list()
        for service in obj.services.all():
            values.append(service.name)
        return values

    def get_model(self):
        return Bagno

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
