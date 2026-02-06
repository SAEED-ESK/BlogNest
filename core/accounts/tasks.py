from celery import shared_task
from time import sleep

@shared_task
def sendEmail():
    """
    A test task for testing celery
    """
    sleep(3)
    print('done sending email')