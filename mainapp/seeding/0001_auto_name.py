from seeding.seeding import BaseSeeding

from mainapp.models import News


class Seeding(BaseSeeding):

    def seeding(self):
        return None

    def rollback(self):
        """ Remove seeded data from project  """
        pass
