from serpent.game_api import GameAPI
import math


class minimetroAPI(GameAPI):

    def __init__(self, game=None):
        super().__init__(game=game)

    # Überprüft ob zwei Regionen überlappen
    def regions_intersect(self, region1, region2):
        #print(region1)
        #print(region2)
        if region1[0] >= region2[2] or region2[0] >= region1[2]:
         #   print(False)
            return False
        if region1[1] <= region2[3] or region2[1] <= region1[3]:
        #    print(False)
            return False
        #print(True)
        return True

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