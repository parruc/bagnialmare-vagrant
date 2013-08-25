from modeltranslation.translator import translator, TranslationOptions
from bagni.models import Bagno, Service, Image


class BagnoTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',  'address', 'city',)

translator.register(Bagno, BagnoTranslationOptions)


class ServiceTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

translator.register(Service, ServiceTranslationOptions)


class ImageTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

translator.register(Image, ImageTranslationOptions)
