from .models import ChileAtiendeService
from .models import ChileAtiendeFile

from .chile_atiende_client import Service
from .chile_atiende_client import File


def create_services():

    '''
    Call API Chile Atiende and create Service in database
    '''

    service = Service()

    json_service = service.list().json()

    services = json_service['servicios']['items']

    for service in services:

        code = service.get('id')

        data = {
            'initial': service.get('sigla'),
            'name': service.get('nombre'),
            'url': service.get('url'),
            'mision': service.get('mision'),
        }

        ChileAtiendeService.objects.update_or_create(
            code=code,
            defaults=data,
        )


def create_files():

    '''
    Call API Chile Atiende and create File in database
    '''

    file_obj = File()

    json_file = file_obj.list().json()

    files = json_file['fichas']['items']['ficha']

    for file in files:

        service_name = file.get('servicio')

        service = ChileAtiendeService.objects.get_or_none(
            name=service_name
        )

        code = file.get('id')

        data = {
            'service': service,
            'service_name': service_name,
            'title': file.get('titulo'),
            'date': file.get('fecha'),
            'objective': file.get('objetivo'),
            'beneficiaries': file.get('beneficiarios'),
            'cost': file.get('costo'),
            'period': file.get('vigencia'),
            'duration': file.get('plazo'),
        }

        ChileAtiendeFile.objects.update_or_create(
            code=code,
            defaults=data,
        )


def create_files_by_services():

    '''
    Call "Ficha" from Chile Atiende API by services in DB
    '''

    file_obj = File()

    services = ChileAtiendeService.objects.all()

    for service in services:

        json_file = file_obj.by_service(service.code).json()

        files = json_file['fichas'].get('items')

        for file in files:

            code = file.get('id'),

            data = {
                'service': service,
                'service_name': file.get('servicio'),
                'title': file.get('titulo'),
                'date': file.get('fecha'),
                'objective': file.get('objetivo'),
                'beneficiaries': file.get('beneficiarios'),
                'cost': file.get('costo'),
                'period': file.get('vigencia', ''),
                'duration': file.get('plazo', ''),
            }

            ChileAtiendeFile.objects.update_or_create(
                code=code,
                defaults=data,
            )


def charge_data():
    create_services()
    create_files_by_services()
