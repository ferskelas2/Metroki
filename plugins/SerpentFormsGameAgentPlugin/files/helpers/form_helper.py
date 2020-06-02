from serpent.input_controller import MouseButton

# Eine Verbindung von zwei Formen
class Connection:
    def __init__(self, game_agent, form1, form2, previous_connection=None, parameters=None):
        self.game_agent = game_agent
        form1.connections.append(self)
        form2.connections.append(self)
        self.forms = [form1, form2]
        self.previous_connection = previous_connection
        self.next_connection = None
        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = {}

    def is_line_end(self):
        if self.previous_connection is None or self.next_connection is None:
            return True
        return False


class FormHelper:

    def __init__(self, game_agent):
        self.game_agent = game_agent

    # Wandelt eine Liste an Regionen in eine Liste von Formen um
    def regions_to_forms(self, regions, type_name, parameters=None):
        forms = []
        for region in regions:
            form = Form(self.game_agent, region, type_name, parameters)
            forms.append(form)
        return forms

    # Wandelt eine Liste an Formen in eine Liste von Regionen um
    def forms_to_regions(self, forms):
        regions = []
        for form in forms:
            regions.append(form.region)
        return regions

    # Verbindet alle Formen in der Liste untereinander
    def connect_forms(self, forms):
        previous_connection = None
        previous_form = None
        for i, form in enumerate(forms, start=1):
            point = form.get_middle()
            self.game_agent.input_controller.move(x=point[0], y=point[1])
            if i == 1:
                self.game_agent.input_controller.click_down(MouseButton.LEFT)
                previous_form = form
            else:
                connection = Connection(self.game_agent, previous_form, form, previous_connection)
                previous_connection = connection
            if i == len(forms):
                self.game_agent.input_controller.click_up(MouseButton.LEFT)

    # Gibt alle Formen in der Liste aus, die den Parameter 'repeating' haben
    def get_repeating(self, forms):
        out = []
        for form in forms:
            if 'repeating' in form.parameters and form.parameters['repeating']:
                out.append(form)
        return out


class Form:

    def __init__(self, game_agent, region, type_name, parameters=None):
        self.game_agent = game_agent
        self.region = region
        self.type_name = type_name
        self.connections = []
        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = {}

    # Gibt den Mittelpunkt der Form aus
    def get_middle(self):
        return self.game_agent.game.api.find_middle_point(self.region)

    # Überprüft ob die Form sich mit einer anderen Form schneidet
    def intersects_form(self, form):
        return self.game_agent.game.api.regions_intersect(self.region, form.region)

    # Überprüft ob die Form mit einer anderen Verbunden ist
    def is_connected(self):
        if len(self.connections) != 0:
            return True
        return False
