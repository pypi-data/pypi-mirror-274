from .clone import clone
from .build import build
from .deploy import deploy, deploy_data
from .assess import assess

all = [assess, clone, build, deploy, deploy_data]
