class CoachPathern:
    def __init__(self, name: str, specialite: str):
        self._name = name
        self._specialite = specialite

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def specialite(self):
        return self._specialite

    @specialite.setter
    def specialite(self, new_specialite):
        self._specialite = new_specialite

    def __str__(self):
        return f"Coach: {self.name}, Specialité: {self.specialite}"
