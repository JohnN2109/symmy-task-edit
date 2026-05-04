from celery import shared_task

from integrator.services.sync_service import run_sync


@shared_task
def sync_products():
    run_sync()