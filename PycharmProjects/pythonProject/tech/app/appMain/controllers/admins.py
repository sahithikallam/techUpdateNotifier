import os
import uuid
from flask_restx import Resource
from flask import request, jsonify, make_response
from werkzeug.utils import secure_filename
from tech.app.appMain import db
from tech.app.appMain.models.admins import Admins
from tech.app.appMain.models.subscriptions import Subscription
from tech.app.appMain.models.user import User
from tech.app.appMain.models.technology import Technology
from tech.app.appMain.dto.admins import AdminDto



admin_api = AdminDto.adminapi


# Admin Signup
@admin_api.route('/signupadmin', methods=['POST'])
class AdminSignup(Resource):
    def post(self):
        return {'message': 'Admin creation is currently disabled.'}, 403

#update admin details
@admin_api.route('/update', methods=['PUT'])
class AdminUpdate(Resource):
    def put(self):
        data = request.get_json()
        admin_email = data.get('admin_email')
        new_username = data.get('username')
        new_admin_email = data.get('admin_email')

        admin = Admins.query.filter_by(admin_email=admin_email).first()
        if admin:
            # Update fields
            admin.username = new_username
            admin.admin_email = new_admin_email
            db.session.commit()  # Save changes
            return {'message': 'Profile updated successfully!'}, 200
        else:
            return {'message': 'Admin not found!'}, 404


# Admin Delete
@admin_api.route('/delete', methods=['DELETE'])
class AdminDelete(Resource):
    def delete(self):
        data = request.get_json()
        admin_email = data.get('admin_email')

        if not admin_email:
            return {'message': 'Admin email is required'}, 400

        admin = Admins.query.filter_by(admin_email=admin_email).first()
        if admin:
            db.session.delete(admin)
            db.session.commit()
            return {'message': 'Admin deleted successfully'}, 200
        else:
            return {'message': 'Admin not found'}, 404


# Get Admin/User Details
@admin_api.route('/details', methods=['GET'])
class AdminUserDetails(Resource):
    def get(self):
        args = request.args
        admin_email = args.get('admin_email')
        username = args.get('username')

        if admin_email:
            admin = Admins.query.filter_by(admin_email=admin_email).first()
            if not admin:
                return {'message': 'Admin not found'}, 404

            admin_data = {
                'admin_id': str(admin.admin_id),
                'username': admin.username,
                'admin_email': admin.admin_email,
                'created_at': admin.created_at,
                'last_login': admin.last_login
            }
            return jsonify(admin_data)

        elif username:
            admin = Admins.query.filter_by(username=username).first()
            if not admin:
                return {'message': 'Admin not found'}, 404

            admin_data = {
                'admin_id': str(admin.admin_id),
                'username': admin.username,
                'admin_email': admin.admin_email,
                'created_at': admin.created_at,
                'last_login': admin.last_login
            }
            return jsonify(admin_data)

        # User details retrieval
        user_email = args.get('user_email')
        user_username = args.get('user_username')

        if user_email:
            user = User.query.filter_by(user_email=user_email).first()
        elif user_username:
            user = User.query.filter_by(user_name=user_username).first()
        else:
            users = User.query.all()
            return make_response([user.to_dict() for user in users], 200)

        if not user:
            return {'message': 'User not found'}, 404

        user_data = {
            'user_id': str(user.user_id),
            'user_name': user.user_name,
            'user_email': user.user_email,
            'created_at': user.created_at,
            'last_login': user.last_login
        }
        return jsonify(user_data)


@admin_api.route('/user/delete/<user_id>', methods=['DELETE'])
class UserDelete(Resource):
    def delete(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            # Delete associated subscriptions
            Subscription.query.filter_by(user_id=user_id).delete()

            # Delete the user
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User and associated subscriptions deleted successfully'}, 200
        else:
            return {'message': 'User not found'}, 404


# Get Technologies
@admin_api.route('/technologies', methods=['GET'])
class AdminTechnologies(Resource):
    def get(self):
        technologies = Technology.query.all()  # Fetch all technologies
        return make_response([{
            'tech_id': str(tech.tech_id),
            'tech_name': tech.tech_name,
            'tech_desc': tech.tech_desc,
        } for tech in technologies], 200)

@admin_api.route('/technology/delete/<tech_id>', methods=['DELETE'])
class TechnologyDelete(Resource):
    def delete(self, tech_id):
        technology = Technology.query.filter_by(tech_id=tech_id).first()
        if technology:
            db.session.delete(technology)
            db.session.commit()
            return {'message': 'Technology deleted successfully'}, 200
        else:
            return {'message': 'Technology not found'}, 404


@admin_api.route('/total-users', methods=['GET'])
class TotalUsers(Resource):
    def get(self):
        count = User.query.count()
        return {'count': count}, 200

@admin_api.route('/total-technologies', methods=['GET'])
class TotalTechnologies(Resource):
    def get(self):
        count = Technology.query.count()
        return {'count': count}, 200


# Admin Add Technology
@admin_api.route('/addTechnologies', methods=['POST'])
class AdminAddTechnology(Resource):
    def post(self):
        """Add a new technology"""

        # Get the form data
        tech_name = request.form.get('tech_name')
        tech_desc = request.form.get('tech_desc')
        version = request.form.get('version')
        releases = request.form.get('releases')
        info = request.form.get('info')

        # Check if all required fields are provided
        if not tech_name:
            return {'message': 'Technology name is required'}, 400
        if not tech_desc:
            return {'message': 'Technology description is required'}, 400
        if not version:
            return {'message': 'Technology version is required'}, 400
        if not releases:
            return {'message': 'Technology releases are required'}, 400
        if not info:
            return {'message': 'Technology information is required'}, 400

        # Handle file upload
        tech_pic = request.files.get('tech_pic')
        if not tech_pic:
            return {'message': 'Technology picture is required'}, 400

        # Validate file extension
        filename = secure_filename(tech_pic.filename)
        file_ext = filename.split('.')[-1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            return {'message': 'Invalid file type. Allowed types: png, jpg, jpeg'}, 400

        # Save the file to the upload folder
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Add a unique identifier to the filename to avoid overwriting
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Save the file
        tech_pic.save(filepath)

        # Create the new technology record
        new_technology = Technology(
            tech_id=uuid.uuid4(),
            tech_name=tech_name,
            tech_desc=tech_desc,
            version=version,
            releases=releases,
            tech_pic=filepath,  # Save the path to the image file
            info=info
        )

        # Add the new technology to the database
        db.session.add(new_technology)
        db.session.commit()

        return {
            'tech_id': str(new_technology.tech_id),
            'tech_name': new_technology.tech_name,
            'tech_desc': new_technology.tech_desc
        }, 201