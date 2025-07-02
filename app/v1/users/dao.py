from models.city import City
from models.country import Country
from models.file import File
from models.fund import Fund
from models.payment import Payment
from models.project import Project, Stage
from models.region import Region
from models.user import User
from v1.dao.base import BaseDAO


class UserDAO(BaseDAO):
    model = User


class CountryDAO(BaseDAO):
    model = Country


class CityDAO(BaseDAO):
    model = City


class RegionDAO(BaseDAO):
    model = Region


class FundDAO(BaseDAO):
    model = Fund


class ProjectDAO(BaseDAO):
    model = Project


class StageDAO(BaseDAO):
    model = Stage


class FileDAO(BaseDAO):
    model = File


class PaymentDAO(BaseDAO):
    model = Payment
