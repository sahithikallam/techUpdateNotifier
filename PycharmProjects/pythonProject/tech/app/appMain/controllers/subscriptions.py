import requests
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from tech.app.appMain import db
from tech.app.appMain.dto.subscriptions import SubscriptionDto
from tech.app.appMain.models.subscriptions import Subscription
from tech.app.appMain.models.technology import Technology

subscription_api = SubscriptionDto.subscription_api

@subscription_api.route('/subscribe', methods=['POST'])
class SubscribeResource(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        tech_id = data.get('tech_id')

        if not user_id or not tech_id:
            # print(1)
            return {'message': 'User ID and Technology ID are required'}, 400

        # Check if the user is already subscribed to the technology
        existing_subscription = Subscription.query.filter_by(user_id=user_id, tech_id=tech_id).first()
        if existing_subscription:
            return {'message': 'You are already subscribed to this technology'}, 400

        new_subscription = Subscription(
            user_id=user_id,
            tech_id=tech_id
        )
        db.session.add(new_subscription)
        db.session.commit()

        return {
            'message': 'Subscribed successfully',
            'subscription_id': str(new_subscription.subscription_id)
        }, 201

@subscription_api.route('/subscriptions', methods=['GET'])
class GetSubscriptionsResource(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        # print(user_id)
        if not user_id:
            return {'message': 'User ID is required'}, 400

        # Fetch subscriptions along with technology details
        subscriptions = (
            db.session.query(Subscription, Technology)
            .join(Technology)
            .filter(Subscription.user_id == user_id)
            .all()
        )

        if not subscriptions:
            return {'message': 'No subscriptions found'}, 404

        return jsonify([{
            'subscription_id': str(sub.subscription_id),
            'tech_id': str(tech.tech_id),
            'tech_name': tech.tech_name,
            'tech_desc': tech.tech_desc,
            'version': tech.version,
            'tech_pic':tech.tech_pic
        } for sub, tech in subscriptions])


@subscription_api.route('/unsubscribe', methods=['POST'])
class UnsubscribeResource(Resource):
    def post(self):
        data = request.get_json()
        print(f"Received unsubscribe request: {data}")  # Add this line for debugging
        user_id = data.get('user_id')
        tech_id = data.get('tech_id')

        if not user_id or not tech_id:
            return {'message': 'User ID and Technology ID are required'}, 400

        subscription = Subscription.query.filter_by(user_id=user_id, tech_id=tech_id).first()
        if subscription:
            db.session.delete(subscription)
            db.session.commit()
            return {'message': 'Unsubscribed successfully'}, 200
        else:
            return {'message': 'Subscription not found'}, 404



@subscription_api.route('/technologies', methods=['GET'])
class GetTechnologiesResource(Resource):
    def get(self):
        technologies = Technology.query.all()
        return jsonify([{
            'tech_id': str(tech.tech_id),
            'tech_name': tech.tech_name,
            'tech_desc': tech.tech_desc,
            'version': tech.version,
            'tech_pic':tech.tech_pic

        } for tech in technologies])

class UpdateFetcher:
    @staticmethod
    def fetch_all_updates(api_url):
        updates = []
        page = 1

        while True:
            try:
                response = requests.get(api_url)
                if response.status_code != 200:
                    raise Exception('Failed to fetch update data')

                update_data = response.json()
                # print(update_data)
                if not update_data:  # No more data to fetch
                    break

                for update in update_data:
                    if 'tag_name' in update:
                        updates.append({
                            'tag_name': update['tag_name'],
                            'description': update.get('body', 'No description available'),
                            'published_at': update['published_at']
                        })
                # print(12345678)
                page += 1  # Increment to fetch the next page

            except:
                break

        return updates


@subscription_api.route('/previous-updates/<string:tech_id>', methods=['GET'])
class PreviousUpdatesResource(Resource):
    @jwt_required()

    def get(self, tech_id):
        # Fetch the technology record by tech_id
        technology = Technology.query.filter_by(tech_id=tech_id).first()
        if not technology:
            return {'message': 'Technology not found'}, 404
        # Get the releases URL from the technology record
        api_url = technology.releases
        print(api_url)
        if api_url:
            try:
                all_updates = UpdateFetcher.fetch_all_updates(api_url)
                if all_updates:
                    return make_response({
                        'tech_id': tech_id,
                        'tech_name': technology.tech_name,
                        'updates': all_updates

                    }, 200)

                else:
                    return {'message': 'No updates found for this technology'}, 404

            except Exception as e:
                return {'message': 'Failed to fetch updates'}, 500

        else:
            return {'message': 'No releases URL found for this technology'}, 404