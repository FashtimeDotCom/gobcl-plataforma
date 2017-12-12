import requests

from django.conf import settings

from .models import Service as ServiceModel
from .models import File as FileModel


class ChileAtiende(object):

    def __init__(self):
        self._url = 'http://www.chileatiende.cl/api'
        self._access_token = settings.CHILEATIENDE_ACCESS_TOKEN

    def _connect(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        request = requests.get(
            url,
            headers=headers
        )

        return request

    def _get_url(self, path, id=None, is_file=False):

        url = '{}{}'.format(
            self._url,
            path,
        )
        if id:
            url = '{}/{}/'.format(
                url,
                id,
            )

        if is_file:
            url = '{}{}'.format(
                url,
                'fichas/'
            )

        url = '{}?access_token={}&type=json'.format(
                url,
                self._access_token,
            )

        return url


class Service(ChileAtiende):

    def list(self):

        return self._connect(
            self._get_url('/servicios')
        )

    def get(self, service_id):

        return self._connect(
            self._get_url('/servicios', service_id)
        )


class File(ChileAtiende):

    def list(self):

        return self._connect(
            self._get_url('/fichas')
        )

    def get(self, file_id):

        return self._connect(
            self._get_url('/fichas', file_id)
        )

    def by_service(self, service_id):

        return self._connect(
            self._get_url('/servicios', service_id, is_file=True)
        )


def create_services():
    service = Service()

    json_service = service.list().json()

    services = json_service['servicios']['items']['servicio']

    service_list = []
    for service in services:

        data = {
            'code': service.get('id'),
            'initial': service.get('sigla'),
            'name': service.get('nombre'),
            'url': service.get('url'),
            'mision': service.get('mision'),
        }

        service_list.append(
            ServiceModel(**data)
        )

    ServiceModel.objects.bulk_create(service_list)


def create_files():
    file_obj = File()

    json_file = file_obj.list().json()

    files = json_file['fichas']['items']['ficha']

    file_list = []
    for file in files:

        service_name = file.get('servicio')

        service = ServiceModel.objects.get_or_none(
            name=service_name
        )

        data = {
            'service': service,
            'service_name': service_name,
            'title': file.get('titulo'),
            'code': file.get('id'),
            'date': file.get('fecha'),
            'objective': file.get('objetivo'),
            'beneficiaries': file.get('beneficiarios'),
            'cost': file.get('costo'),
            'period': file.get('vigencia'),
            'duration': file.get('plazo'),
        }

        file_list.append(
            FileModel(**data)
        )

    FileModel.objects.bulk_create(file_list)


def create_files_by_services():
    file_obj = File()

    services = ServiceModel.objects.all()

    for service in services:

        json_file = file_obj.by_service(service.code).json()

        files = json_file['fichas']['items']

        file_list = []
        for file in files:

            service_name = file.get('servicio')

            service = ServiceModel.objects.get_or_none(
                name=service_name
            )

            data = {
                'service': service,
                'service_name': service_name,
                'title': file.get('titulo'),
                'code': file.get('id'),
                'date': file.get('fecha'),
                'objective': file.get('objetivo'),
                'beneficiaries': file.get('beneficiarios'),
                'cost': file.get('costo'),
                'period': file.get('vigencia'),
                'duration': file.get('plazo'),
            }

            file_list.append(
                FileModel(**data)
            )

        FileModel.objects.bulk_create(file_list)


def charge_data():
    create_services()
    create_files_by_services()
