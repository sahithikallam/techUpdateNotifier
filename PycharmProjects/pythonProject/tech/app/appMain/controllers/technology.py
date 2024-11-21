import uuid
from flask import request
from flask_restx import Resource
from tech.app.appMain import db
from tech.app.appMain.models.technology import Technology
from tech.app.appMain.dto.technology import TechnologyDto

technology_api = TechnologyDto.technology_api



# Get All Technologies
@technology_api.route('/technologies', methods=['GET'])
class TechnologyList(Resource):
    def get(self):
        """Get all technologies"""
        technologies = Technology.query.all()
        return [{
            'tech_id': str(tech.tech_id),
            'tech_name': tech.tech_name,
            'tech_desc': tech.tech_desc,
            'version': tech.version,
            'info': tech.info,
            'tech_pic': tech.tech_pic  # Include tech_pic in the response
        } for tech in technologies], 200

    def post(self):
        """Create a new technology"""
        data = request.get_json()
        tech_name = data.get('tech_name')
        tech_desc = data.get('tech_desc')
        tech_pic = data.get('tech_pic')  # Get tech_pic from request

        if not tech_name:
            return {'message': 'Technology name is required'}, 400

        new_technology = Technology(
            tech_id=str(uuid.uuid4()),
            tech_name=tech_name,
            tech_desc=tech_desc,
            # info=info,
            version='1.0.0',  # Set initial version
            tech_pic=tech_pic  # Set tech_pic if provided
        )
        db.session.add(new_technology)
        db.session.commit()

        return {
            'tech_id': str(new_technology.tech_id),
            'tech_name': new_technology.tech_name,
            'tech_desc': new_technology.tech_desc,
            'version': new_technology.version,
            'tech_pic': new_technology.tech_pic  # Include tech_pic in the response
        }, 201

# Get, Update, and Delete Technology by ID or Name
@technology_api.route('/technologies/<string:identifier>', methods=['GET', 'PUT', 'DELETE'])
class TechnologyResource(Resource):
    def get(self, identifier):
        """Get a technology by ID or name"""
        technology = self.get_technology(identifier)
        if not technology:
            return {'message': 'Technology not found'}, 404

        return {
            'tech_id': str(technology.tech_id),
            'tech_name': technology.tech_name,
            'tech_desc': technology.tech_desc,
            'version': technology.version,
            'info': technology.info,
            'tech_pic': technology.tech_pic  # Include tech_pic in the response
        }, 200

    def put(self, identifier):
        """Update a technology by ID or name"""
        data = request.get_json()
        tech_name = data.get('tech_name')
        tech_desc = data.get('tech_desc')
        tech_pic = data.get('tech_pic')  # Update tech_pic if provided

        technology = self.get_technology(identifier)
        if not technology:
            return {'message': 'Technology not found'}, 404

        # Update fields without changing version
        if tech_name:
            technology.tech_name = tech_name
        if tech_desc is not None:
            technology.tech_desc = tech_desc
        if tech_pic is not None:
            technology.tech_pic = tech_pic  # Update tech_pic

        db.session.commit()
        return {
            'tech_id': str(technology.tech_id),
            'tech_name': technology.tech_name,
            'tech_desc': technology.tech_desc,
            'version': technology.version,
            'info': technology.info,
            'tech_pic': technology.tech_pic  # Include tech_pic in the response
        }, 200

    def delete(self, identifier):
        """Delete a technology by ID or name"""
        technology = self.get_technology(identifier)
        if not technology:
            return {'message': 'Technology not found'}, 404

        db.session.delete(technology)
        db.session.commit()

        return {'message': 'Technology deleted successfully'}, 200

    def get_technology(self, identifier):
        """Utility method to fetch a technology by ID or name."""
        return Technology.query.filter(
            (Technology.tech_id == identifier) |
            (Technology.tech_name == identifier)
        ).first()

# Get Technology Details
@technology_api.route('/details', methods=['GET'])
class TechnologyDetails(Resource):
    def get(self):
        """Get technology details by tech_id or tech_name"""
        args = request.args
        tech_id = args.get('tech_id')
        tech_name = args.get('tech_name')

        if tech_id:
            technology = Technology.query.filter_by(tech_id=tech_id).first()
        elif tech_name:
            technology = Technology.query.filter_by(tech_name=tech_name).first()
        else:
            return {'message': 'Either tech_id or tech_name must be provided'}, 400

        if not technology:
            return {'message': 'Technology not found'}, 404

        return {
            'tech_id': str(technology.tech_id),
            'tech_name': technology.tech_name,
            'tech_desc': technology.tech_desc,
            'version': technology.version,
            'info' : technology.info,
            'tech_pic': technology.tech_pic  # Include tech_pic in the response
        }, 200
