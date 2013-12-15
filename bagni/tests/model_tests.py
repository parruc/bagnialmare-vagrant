from django.test import TestCase
from django.contrib.gis.geos import Point

from bagni.models import Bagno

def create_dummy_bagno(name="bagno test"):
    b = Bagno.objects.create(
        name = name,
        number = "18",
        address = "via test n. 0",
        city = "TestCity",
        mail = "mail@example.com",
        point = Point([40.0, 50.0]),
        )
    b.save()
    return b




        # article = Articles()
        # article.title = "This is title"
        # article.body = "This is body"
        # article.save()

        # articles_in_database = Articles.objects.all()
        # self.assertEquals(len(articles_in_database), 1)
        # only_article_in_database = articles_in_database[0]
        # self.assertEquals(only_article_in_database, article)

        # self.assertEquals(only_article_in_database.title, "This is title")
        # self.assertEquals(only_article_in_database.body, "This is body")


class BagnoModelTest(TestCase):
    """
    What should we test in the models?
    """
    def setUp(self):
        """
        This already tests wether we can create a new object or not
        """
        self.added = create_dummy_bagno()

    def test_basic_retrival(self):
        """
        Does this test make any sense?
        """
        self.assertTrue(self.added in Bagno.objects.all())

    def test_index_features(self):
        """
        this test should definitely exist as it tests a method we added
        extending the basic django features.
        What should we test though?! If this test is a bare replication of the
        method defined in the model it makes no sense at all ...
        """
        b = Bagno.objects.all()[0]
        self.assertTrue(hasattr(b, 'index_features'))
        features = b.index_features()
        self.assertEqual(features['id'], unicode(b.id))
        self.assertTrue(features.has_key('city'))
        self.assertTrue(features.has_key('text'))
        self.assertTrue(features.has_key('services'))


class HomePage(TestCase):
    """
    Very very simple test case. Just shows how to use the client.get method
    """
    def test_home_page_template(self):
        self.assertTrue(len(Bagno.objects.all()) == 0) #true if no fixture
        response = self.client.get("/it/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "bagni/homepage.html")


class BagniPage(TestCase):
    """
    Let's begin to create stuff and test the database functionalities and view
    argument passing
    """

    fixtures = ['bagni.json']

    def test_view_params(self):
        self.assertTrue(len(Bagno.objects.all()) > 10) #false if fixtures
        response = self.client.get('/it/bagni/')
        self.assertIn('object_list', response.context)

