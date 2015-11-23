from mock import Mock, patch
from django.test import TestCase
from django.core.urlresolvers import reverse
import views
from .client import get_products


class ClientTest(TestCase):
    @patch('requests.get')
    def test_client_results_ok(self, requests_get):
        mocked_response = Mock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = {u'search': {
            u'results': []}}

        with self.settings(
                API_ROOT_URL='https://dev.api.io/search?=',
                API_TOKEN='abc123'):

            requests_get.return_value = mocked_response
            products = get_products(['red', 'boots'])
            requests_get.assert_called_with(
                'https://dev.api.io/search?=red+boots',
                headers={'Authorization': 'MSAuth apikey=abc123'})

    @patch('requests.get')
    def test_client_results_error(self, requests_get):
        mocked_response = Mock()
        mocked_response.status_code = 403

        with self.settings(
                API_ROOT_URL='https://dev.api.io/search?=',
                API_TOKEN='abc123'):

            requests_get.return_value = mocked_response
            products = get_products(['red', 'boots'])
            requests_get.assert_called_with(
                'https://dev.api.io/search?=red+boots',
                headers={'Authorization': 'MSAuth apikey=abc123'})
            self.assertIsNone(products)


class SearchViewTest(TestCase):
    @patch('requests.get')
    def test_search_view_ok(self, requests_get):
        mocked_response = Mock()
        mocked_response.status_code = 200
        mocked_response.json.return_value = {u'search': {
            u'results': [
                {
                    u'averageRating': 5,
                    u'averageRatingPercentage': 100,
                    u'averageRatingText': u'5.00',
                    u'brand': u'',
                    u'callout': {u'collectInXDays': u'7', u'flag': None},
                    u'categoryId': u'301001',
                    u'defaultProductImage': u'xxx',
                    u'fullImageUrl': u'xxx',
                    u'hasSwatches': False,
                    u'isNew': False,
                    u'isOnlineOnly': False,
                    u'listViewImage': u'xxx',
                    u'price': {
                        u'desc': u'',
                        u'isSalePrice': False,
                        u'listPriceText': u'&pound; 42.00',
                        u'productPerUnitPrice': None,
                        u'wasPriceText': None},
                    u'productId': u'P60058441',
                    u'productMainImage': u'xxx',
                    u'title': u'Football Boots Cake - Red'},
                {
                    u'averageRating': 4.5,
                    u'averageRatingPercentage': 90,
                    u'averageRatingText': u'4.50',
                    u'brand': u'Footglove&trade;',
                    u'callout': {u'flag': None},
                    u'categoryId': u'1031502',
                    u'defaultProductImage': u'xxx',
                    u'fullImageUrl': u'xxx',
                    u'hasSwatches': False,
                    u'isNew': False,
                    u'isOnlineOnly': False,
                    u'listViewImage': u'xxx',
                    u'price': {
                        u'desc': u'',
                        u'isSalePrice': False,
                        u'listPriceText': u'&pound; 55.00',
                        u'productPerUnitPrice': None,
                        u'wasPriceText': None},
                    u'productId': u'P22309986',
                    u'productMainImage': u'xxx',
                    u'title': u'Leather Platform Ankle Boots'},
                {
                    u'averageRating': 4.4,
                    u'averageRatingPercentage': 88.00000000000001,
                    u'averageRatingText': u'4.40',
                    u'brand': u'Limited Edition',
                    u'callout': {u'flag': None},
                    u'categoryId': u'1031502',
                    u'defaultProductImage': u'',
                    u'fullImageUrl': u'',
                    u'hasSwatches': False,
                    u'isNew': False,
                    u'isOnlineOnly': False,
                    u'listViewImage': u'',
                    u'price': {
                        u'desc': u'',
                        u'isSalePrice': False,
                        u'listPriceText': u'&pound; 45.00',
                        u'productPerUnitPrice': None,
                        u'wasPriceText': None},
                    u'productId': u'P22321434',
                    u'productMainImage': u'xxx',
                    u'title': u'Chain Trim Ankle Boots with Insolia Flex'}]
            }}

        with self.settings(
                API_ROOT_URL='https://dev.api.io/search?=',
                API_TOKEN='abc123'):

            requests_get.return_value = mocked_response
            products = get_products(['red', 'boots'])
            response = self.client.get(
                reverse('search-index-view'), {'keywords': 'red boots'})

            self.assertTemplateUsed(response, 'results.html')
            self.assertContains(
                response,
                "Chain Trim Ankle Boots with Insolia Flex")
            self.assertContains(
                response,
                "Leather Platform Ankle Boots")
            self.assertContains(
                response,
                "Football Boots Cake - Red")

    @patch.object(views, 'get_products')
    def test_search_view_return_none_products(self, get_products):
        get_products.return_value = None

        with self.settings(
                API_ROOT_URL='https://dev.api.io/search?=',
                API_TOKEN='abc123'):

            response = self.client.get(
                reverse('search-index-view'), {'keywords': 'red boots'})

            self.assertTemplateUsed(response, 'results.html')
            self.assertContains(
                response,
                "Sorry, the product you are looking for is not available.")

    @patch.object(views, 'get_products')
    def test_search_view_return_error(self, get_products):
        e = Exception('An error occurred')
        get_products.side_effect = e

        with self.settings(
                API_ROOT_URL='https://dev.api.io/search?=',
                API_TOKEN='abc123'):

            response = self.client.get(
                reverse('search-index-view'), {'keywords': 'red boots'})
            self.assertTemplateUsed(response, 'error.html')
