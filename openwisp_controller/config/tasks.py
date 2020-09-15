import logging

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from swapper import load_model

logger = logging.getLogger(__name__)
Vpn = load_model('config', 'Vpn')


@shared_task(soft_time_limit=1200)
def create_vpn_dhparam(vpn_pk):
    vpn_obj = Vpn.objects.get(pk=vpn_pk)
    try:
        vpn_obj.dh = Vpn.dhparam(2048)
    except SoftTimeLimitExceeded as e:
        logger.warning(f'A timeout exception occurred when generating the DH: {e}')
    else:
        vpn_obj.full_clean()
        vpn_obj.save()
