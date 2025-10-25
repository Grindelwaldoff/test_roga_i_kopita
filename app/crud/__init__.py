from .corporations import CRUDCorporation  # noqa

from app import models  # noqa

corporation_crud = CRUDCorporation(models.Corporation)
