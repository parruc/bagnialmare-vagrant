from modeltranslation.translator import translator, TranslationOptions
from bagni.models import Bagno, Service, Image, Municipality, District


class BagnoTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',  'address',)

translator.register(Bagno, BagnoTranslationOptions)


class ServiceTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

translator.register(Service, ServiceTranslationOptions)


class DistrictTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

translator.register(District, DistrictTranslationOptions)


class MunicipalityTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

translator.register(Municipality, MunicipalityTranslationOptions)


class ImageTranslationOptions(TranslationOptions):
    fields = ('name', 'slug',)

translator.register(Image, ImageTranslationOptions)
