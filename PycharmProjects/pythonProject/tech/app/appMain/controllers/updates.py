# import uuid
# import logging
# from datetime import datetime
# from flask import request, make_response
# from flask_jwt_extended import get_jwt_identity, jwt_required
# from flask_restx import Resource
# from tech.app.appMain import db
# from tech.app.appMain.dto.updates import UpdateDto
# from tech.app.appMain.models.subscriptions import Subscription
# from tech.app.appMain.models.technology import Technology
# from tech.app.appMain.models.updates import Update
# from tech.app.appMain.models.user_notifications import UserNotification
# import requests
#
# update_api = UpdateDto.update_api
#
# # Helper functions for fetching tech updates
# def get_tech_id_map():
#     tech_map = {}
#     technologies = Technology.query.all()
#     for tech in technologies:
#         tech_id = str(tech.tech_id)
#         tech_map[tech_id] = tech.tech_name
#     return tech_map
#
# # def fetch_update_from_api(api_url):
# #     try:
# #         response = requests.get(api_url)
# #         if response.status_code != 200:
# #             raise Exception('Failed to fetch update data')
# #
# #         update_data = response.json()
# #         if 'tag_name' in update_data[0]:
# #             print(update_data)
# #             return f"Latest release found: {update_data[0]['tag_name']}"
# #         else:
# #             raise Exception('Update data format is unexpected')
# #     except Exception as e:
# #         logging.error(f"Error fetching data from {api_url}: {str(e)}")
# #         raise
#
# def fetch_update_from_api(releases, tech_name):
#     try:
#         # Handling technology-specific APIs from the 'releases' column (releases is a list of URLs)
#         if not releases:
#             raise Exception(f"No release URLs found for {tech_name}")
#
#         release_url = releases[0]  # Assuming the releases column stores a list of URLs and using the first one
#
#         response = requests.get(release_url)
#
#         if response.status_code != 200:
#             raise Exception(f"Failed to fetch update data, status code: {response.status_code}")
#
#         update_data = response.json()
#
#         # Ensure the data is in the expected format
#         if not isinstance(update_data, list) or len(update_data) == 0:
#             raise Exception("Update data is not a list or is empty")
#
#         if 'tag_name' in update_data[0]:
#             return f"Latest release for {tech_name}: {update_data[0]['tag_name']}"
#         else:
#             raise Exception("Update data format is unexpected: 'tag_name' not found")
#     except Exception as e:
#         logging.error(f"Error fetching data from {releases}: {str(e)}")
#         # Return a default response if something goes wrong
#         return f"Error fetching update for {tech_name}."
#
#
# def get_api_url(tech_name):
#     api_map = {
#         "Next.js": "https://api.github.com/repos/vercel/next.js/releases",
#         "Node.js": "https://api.github.com/repos/nodejs/node/releases",
#         "Spring Boot": "https://api.github.com/repos/spring-projects/spring-boot/releases",
#         "ReactJS": "https://api.github.com/repos/facebook/react/releases",
#     }
#     return api_map.get(tech_name, "https://randomuser.me/api/")
#
# @update_api.route('/user-updates', methods=['GET'])
# class UserUpdateResource(Resource):
#     # @jwt_required()
#     def get(self):
#         user_id = get_jwt_identity()
#         data =request.get_json()
#         user_id = data.get('user_id')
#
#         subscriptions = Subscription.query.filter_by(user_id=user_id).all()
#         tech_ids = [sub.tech_id for sub in subscriptions]
#
#         if not tech_ids:
#             return {'message': 'No subscriptions found for this user'}, 404
#
#         updates = Update.query.filter(Update.tech_id.in_(tech_ids)).all()
#
#         if not updates:
#             return {'message': 'No updates found for your subscriptions'}, 404
#
#         updates_list = []
#         for update in updates:
#             updates_list.append({
#                 'update_id': str(update.update_id),
#                 'tech_id': str(update.tech_id),
#                 'update_type': update.update_type,
#                 'update_description': update.update_description,
#                 'update_date': str(update.update_date.isoformat()),
#                 'created_at': str(update.created_at.isoformat())
#             })
#
#         latest_updates = self.fetch_latest_updates(tech_ids)
#
#         return make_response({'updates': updates_list, 'latest_updates': latest_updates}, 200)
#
#     def fetch_latest_updates(self, tech_ids):
#         tech_id_map = get_tech_id_map()
#         latest_updates = []
#
#         for tech_id in tech_ids:
#             tech_name = tech_id_map.get(tech_id)
#             if tech_name:
#                 api_url = get_api_url(tech_name)
#                 try:
#                     update_description = fetch_update_from_api(api_url, tech_name)
#                     latest_updates.append({
#                         'tech_id': tech_id,
#                         'tech_name': tech_name,
#                         'update_description': update_description
#                     })
#                 except Exception as e:
#                     logging.error(f"Error fetching latest update for {tech_name}: {str(e)}")
#                     # In case of error, still return a placeholder update
#                     latest_updates.append({
#                         'tech_id': tech_id,
#                         'tech_name': tech_name,
#                         'update_description': f"No new update available for {tech_name}."
#                     })
#
#         return latest_updates
#
# @update_api.route('', methods=['POST'])
# class UpdateResource(Resource):
#     def post(self):
#         data = request.get_json()
#         tech_id = data.get('tech_id')
#         update_type = data.get('update_type')
#
#         if not data or not tech_id or not update_type:
#             return {'message': 'Technology ID and Update Type are required'}, 400
#
#         tech_id_map = get_tech_id_map()
#         tech_name = tech_id_map.get(tech_id)
#
#         if not tech_name:
#             return {'message': 'Invalid Technology ID'}, 400
#
#         api_url = get_api_url(tech_name)
#         try:
#             update_description = fetch_update_from_api(api_url)
#         except Exception as e:
#             logging.error(f"Error fetching update description: {str(e)}")
#             return {'message': str(e)}, 500
#
#         latest_update = Update.query.filter_by(tech_id=tech_id).order_by(Update.update_date.desc()).first()
#
#         if latest_update and latest_update.update_description == update_description:
#             return {'message': 'No new update to notify'}, 200
#
#         new_update = Update(
#             tech_id=tech_id,
#             update_type=update_type,
#             update_description=update_description,
#             update_date=datetime.utcnow(),
#             created_at=datetime.utcnow()
#         )
#
#         try:
#             db.session.add(new_update)
#
#             techRelease = Technology.query.filter_by(tech_id=tech_id).first()
#
#             subscriptions = Subscription.query.filter_by(tech_id=tech_id).all()
#             notifications_list = []
#
#             for subscription in subscriptions:
#                 notification = UserNotification(
#                     notification_id=str(uuid.uuid4()),
#                     user_id=subscription.user_id,
#                     read=False,
#                     title=tech_name,
#                     message=f"Latest update for {tech_name}: {update_description}",
#                     url=techRelease.releases,
#                     created_at=datetime.utcnow(),
#                     isactive=True
#                 )
#                 notifications_list.append(notification)
#
#             db.session.add_all(notifications_list)
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()
#             logging.error(f"Error saving update or notifications: {str(e)}")
#             return {'message': 'Failed to save update or notifications'}, 500
#
#         result = {
#             'message': 'Update created successfully',
#             'update_id': str(new_update.update_id),
#             'notifications': [notification.to_dict() for notification in notifications_list]
#         }
#         return make_response(result, 200)
#
#


import uuid
import logging
from datetime import datetime
from flask import request, make_response
from flask_jwt_extended import get_jwt_identity
from flask_restx import Resource
from tech.app.appMain import db
from tech.app.appMain.dto.updates import UpdateDto
from tech.app.appMain.models.subscriptions import Subscription
from tech.app.appMain.models.technology import Technology
from tech.app.appMain.models.updates import Update
from tech.app.appMain.models.user_notifications import UserNotification
import requests

update_api = UpdateDto.update_api


# Helper functions for fetching tech updates
def get_tech_id_map():
    tech_map = {}
    technologies = Technology.query.all()
    for tech in technologies:
        tech_id = str(tech.tech_id)
        tech_map[tech_id] = tech.tech_name
    return tech_map

def fetch_update_from_api(releases, tech_name):
    try:
        # Handling technology-specific APIs from the 'releases' column (releases is a list of URLs)
        if not releases:
            raise Exception(f"No release URLs found for {tech_name}")

        release_url = releases[0]  # Assuming the releases column stores a list of URLs and using the first one

        response = requests.get(release_url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch update data, status code: {response.status_code}")

        update_data = response.json()

        # Ensure the data is in the expected format
        if not isinstance(update_data, list) or len(update_data) == 0:
            raise Exception("Update data is not a list or is empty")

        if 'tag_name' in update_data[0]:
            return f"Latest release for {tech_name}: {update_data[0]['tag_name']}"
        else:
            raise Exception("Update data format is unexpected: 'tag_name' not found")
    except Exception as e:
        logging.error(f"Error fetching data from {releases}: {str(e)}")
        # Return a default response if something goes wrong
        return f"Error fetching update for {tech_name}."

def get_api_url(tech_name):
    api_map = {
        "Next.js": "https://api.github.com/repos/vercel/next.js/releases",
        "Node.js": "https://api.github.com/repos/nodejs/node/releases",
        "Spring Boot": "https://api.github.com/repos/spring-projects/spring-boot/releases",
        "ReactJS": "https://api.github.com/repos/facebook/react/releases",
    }
    return api_map.get(tech_name, "https://randomuser.me/api/")

@update_api.route('/user-updates', methods=['GET'])
class UserUpdateResource(Resource):
    def get(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        user_id = data.get('user_id')

        subscriptions = Subscription.query.filter_by(user_id=user_id).all()
        tech_ids = [sub.tech_id for sub in subscriptions]

        if not tech_ids:
            return {'message': 'No subscriptions found for this user'}, 404

        updates = Update.query.filter(Update.tech_id.in_(tech_ids)).all()

        if not updates:
            return {'message': 'No updates found for your subscriptions'}, 404

        updates_list = []
        for update in updates:
            updates_list.append({
                'update_id': str(update.update_id),
                'tech_id': str(update.tech_id),
                'update_type': update.update_type,
                'update_description': update.update_description,
                'update_date': str(update.update_date.isoformat()),
                'created_at': str(update.created_at.isoformat())
            })

        latest_updates = self.fetch_latest_updates(tech_ids)

        return make_response({'updates': updates_list, 'latest_updates': latest_updates}, 200)

    def fetch_latest_updates(self, tech_ids):
        tech_id_map = get_tech_id_map()
        latest_updates = []

        for tech_id in tech_ids:
            tech_name = tech_id_map.get(tech_id)
            if tech_name:
                api_url = get_api_url(tech_name)
                try:
                    update_description = fetch_update_from_api(api_url, tech_name)
                    latest_updates.append({
                        'tech_id': tech_id,
                        'tech_name': tech_name,
                        'update_description': update_description
                    })
                except Exception as e:
                    logging.error(f"Error fetching latest update for {tech_name}: {str(e)}")
                    # In case of error, still return a placeholder update
                    latest_updates.append({
                        'tech_id': tech_id,
                        'tech_name': tech_name,
                        'update_description': f"No new update available for {tech_name}."
                    })

        return latest_updates

@update_api.route('', methods=['POST'])
class UpdateResource(Resource):
    def post(self):
        data = request.get_json()
        tech_id = data.get('tech_id')
        update_type = data.get('update_type')

        if not data or not tech_id or not update_type:
            return {'message': 'Technology ID and Update Type are required'}, 400

        tech_id_map = get_tech_id_map()
        tech_name = tech_id_map.get(tech_id)

        if not tech_name:
            return {'message': 'Invalid Technology ID'}, 400

        # Fetching the release data for the technology
        releases = Technology.query.filter_by(tech_id=tech_id).first().releases
        try:
            update_description = fetch_update_from_api(releases, tech_name)
        except Exception as e:
            logging.error(f"Error fetching update description: {str(e)}")
            return {'message': str(e)}, 500

        latest_update = Update.query.filter_by(tech_id=tech_id).order_by(Update.update_date.desc()).first()

        if latest_update and latest_update.update_description == update_description:
            return {'message': 'No new update to notify'}, 200

        new_update = Update(
            tech_id=tech_id,
            update_type=update_type,
            update_description=update_description,
            update_date=datetime.utcnow(),
            created_at=datetime.utcnow()
        )

        try:
            db.session.add(new_update)

            techRelease = Technology.query.filter_by(tech_id=tech_id).first()

            subscriptions = Subscription.query.filter_by(tech_id=tech_id).all()
            notifications_list = []

            for subscription in subscriptions:
                # Check if a notification already exists for this user and technology
                existing_notification = UserNotification.query.filter_by(
                    user_id=subscription.user_id,
                    tech_id=tech_id,
                    update_id=new_update.update_id
                ).first()

                if existing_notification:
                    continue  # Skip creating a new notification if one already exists

                # Create new notification only if it doesn't exist already
                notification = UserNotification(
                    notification_id=str(uuid.uuid4()),
                    user_id=subscription.user_id,
                    read=False,
                    title=tech_name,
                    message=f"Latest update for {tech_name}: {update_description}",
                    url=techRelease.releases,
                    created_at=datetime.utcnow(),
                    isactive=True
                )
                notifications_list.append(notification)

            db.session.add_all(notifications_list)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving update or notifications: {str(e)}")
            return {'message': 'Failed to save update or notifications'}, 500

        result = {
            'message': 'Update created successfully',
            'update_id': str(new_update.update_id),
            'notifications': [notification.to_dict() for notification in notifications_list]
        }
        return make_response(result, 200)
