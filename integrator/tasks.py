from celery import shared_task
from integrator.mock_data import PRODUCTS
from integrator.services.sync_services import run_sync


@shared_task(bind=True, max_retries=3)
def sync_products(self):
    run_sync(PRODUCTS)