# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions
from bagni import models


class BagnoTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',  'address',)

translator.register(models.Bagno, BagnoTranslationOptions)


class ServiceTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(models.Service, ServiceTranslationOptions)


class DistrictTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(models.District, DistrictTranslationOptions)


class MunicipalityTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(models.Municipality, MunicipalityTranslationOptions)


class ServiceCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(models.ServiceCategory, ServiceCategoryTranslationOptions)


class LanguageTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(models.Language, LanguageTranslationOptions)


class ImageTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(models.Image, ImageTranslationOptions)
