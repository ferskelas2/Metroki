import cv2
import numpy as np
import serpent.cv


class SpriteHelper:

    def __init__(self, game_agent):
        self.game_agent = game_agent

    # Findet alle Vorkommnisse eines Bildes innerhalb eines GameFrames
    # path = Der absolute Pfad zu dem zu suchenden Bild
    # game_frame = Der GameFrame, in dem gesucht werden soll
    # screen_region = Eine eingrenzung der zu suchenden Region
    # use_global_location = Ob die Coordinaten relativ zu der ScreenRegion oder zu dem GameFrame angegeben werden sollen
    def find(self, path, game_frame=None, screen_region=None, use_global_location=True, ignore_regions=[]):
        regions = []

        # Den Frame zum suchen vorbereiten
        frame = game_frame.grayscale_frame
        if screen_region is not None:
            frame = serpent.cv.extract_region_from_image(frame, screen_region)

        # Das zu suchende Bild vorbereiten
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(frame, image, cv2.TM_CCOEFF_NORMED)
        # Alle Punkte über einem gewissen threshold auf Gültigkeit überprüfen
        threshold = .9
        loc = np.where(res >= threshold)
        #print('ignore')
        #print(ignore_regions)
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            valid = True
            region = [pt[0], pt[1], pt[0] + image.shape[0], pt[1] + image.shape[1]]
            #print(region)
            # Überprügt, ob die gefundene Region mit einer der zu ignorierenden Regionen überschneidet

            for ignore in ignore_regions:
                if not self.game_agent.game.api.regions_intersect(region, ignore):
                    valid = False
                    break
            # Wenn die Region gültig ist zu den gültigen Regionen hinzufügen
            if valid:
                if region is not None and screen_region is not None and use_global_location:
                    region = (
                        region[0] + screen_region[0],
                        region[1] + screen_region[1],
                        region[2] + screen_region[0],
                        region[3] + screen_region[1]
                    )
                ignore_regions.append(region)
                regions.append(region)
        return regions
