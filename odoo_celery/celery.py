from __future__ import absolute_import
from celery import Celery
from kombu import Queue, Exchange
from odoo.modules.registry import RegistryManager
from odoo.api import Environment
from odoo import modules
import odoo
from odoo_celery.celeryconfig import conf_file


app = Celery('credr-odoo')
CELERY_QUEUES = (
    # Queue('default', Exchange('default'), routing_key='default'),
    Queue('odoo_task', Exchange('odoo_task'), routing_key='odoo_task'),
)
app.conf.task_queues = CELERY_QUEUES
# import pdb; pdb.set_trace()
# app.conf.task_create_missing_queues = False
# app.conf.task_ignore_result = True
# app.conf.task_default_queue = 'odoo_task'
# app.conf.event_queue_expires = 36000
app.conf.timezone = 'Asia/Kolkata'

# Set is and env variable
odoo.tools.config.parse_config(['-c', conf_file])
mods = modules.get_modules()
modules.initialize_sys_path()

install_apps = [
    'c2b_crm'
]

installed_mods = []
for mod in mods:
    if mod in install_apps:
        installed_mods.append('odoo.addons.'+mod)

app.autodiscover_tasks(lambda: installed_mods)

