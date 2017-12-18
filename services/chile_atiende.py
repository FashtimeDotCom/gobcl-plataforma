from .models import Service as ServiceModel
from .models import File as FileModel

from .chile_atiende_client import Service
from .chile_atiende_client import File


def create_services():

    '''
    Call API Chile Atiende and create Service in database
    '''

    service = Service()

    json_service = service.list().json()

    services = json_service['servicios']['items']

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

    '''
    Call API Chile Atiende and create File in database
    '''

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

    '''
    Call "Ficha" from Chile Atiende API by services in DB
    '''

    file_obj = File()

    services = ServiceModel.objects.all()

    file_list = []
    for service in services:

        json_file = file_obj.by_service(service.code).json()

        files = json_file['fichas']['items']

        for file in files:

            data = {
                'service': service,
                'service_name': file.get('servicio'),
                'title': file.get('titulo'),
                'code': file.get('id'),
                'date': file.get('fecha'),
                'objective': file.get('objetivo'),
                'beneficiaries': file.get('beneficiarios'),
                'cost': file.get('costo'),
                'period': file.get('vigencia', ''),
                'duration': file.get('plazo', ''),
            }

            file_list.append(
                FileModel(**data)
            )

    FileModel.objects.bulk_create(file_list)


def charge_data():
    create_services()
    create_files_by_services()
