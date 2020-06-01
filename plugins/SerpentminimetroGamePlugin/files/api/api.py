from serpent.game_api import GameAPI
import math


class minimetroAPI(GameAPI):

    def __init__(self, game=None):
        super().__init__(game=game)

    # Überprüft ob zwei Regionen überlappen
    def regions_intersect(self, region1, region2):
        if region1[0] < region2[2] and region1[2] > region2[0] and region1[1] < region2[3] and region1[3] > region2[1]:
            return True
        return False

    # Gibt die Mitte einer Region aus
    def find_middle_point(self, region):
        x = (region[2] + region[0]) / 2
        y = (region[3] + region[1]) / 2
        return x, y

    def get_distance(self, point1, point2):
        dist = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
        return dist

    class MyAPINamespace:

        @classmethod
        def my_namespaced_api_function(cls):
            api = minimetroAPI.instance