from flask_restx import Namespace

class TechnologyDto:
    technology_api = Namespace('technology', description='API for technology operations (CRUD for technologies)')

