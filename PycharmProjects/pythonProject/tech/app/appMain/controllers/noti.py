# from flask import make_response
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from flask_restx import Resource
#
# from tech.app.appMain.controllers.user import users_api
# from tech.app.appMain.dto.noti import NotiDto
# from tech.app.appMain.models.noti import AdminNotification
#
#
#
# noti_api = NotiDto.noti_api
#
#
#
# @users_api.route('/admin/notifications', methods=['GET'])
# class GetAdminNotifications(Resource):
#     @jwt_required()  # Ensure the request has a valid JWT token (to verify admin identity)
#     def get(self):
#         admin_id = get_jwt_identity()  # Extract admin_id from JWT token
#         notifications = AdminNotification.query.filter_by(admin_id=admin_id).order_by(
#             AdminNotification.created_at.desc()).all()
#
#         # Convert notifications to dictionary format
#         noti_list = [notification.to_dict() for notification in notifications]
#
#         return make_response(noti_list, 200)
