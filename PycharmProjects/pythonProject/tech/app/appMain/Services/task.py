import uuid
from importlib.resources import Resource

import requests
from datetime import datetime
from tech.app.appMain.models.updates import Update
from tech.app.appMain.models.technology import Technology
from tech.app.appMain.models.subscriptions import Subscription
from tech.app.appMain.models.user_notifications import UserNotification
from tech.app.appMain import db

#
# class TaskService:
#     @staticmethod
#     def fetch_and_create_updates():
#         try:
#             # Access the current app's database session
#             db_session = db.session
#             # print("qwertyuio")
#             technologies = Technology.query.all()
#             # print(technologies)
#
#             if not technologies:
#                 return "No technologies found in the database."
#
#             for tech in technologies:
#                 tech_name = tech.tech_name
#                 tech_id = str(tech.tech_id)
#                 print(tech_id)
#                 print(tech_name)
#
#                 # Define the API URL for fetching updates based on technology
#                 api_url = {
#                     "Next.js": "https://api.github.com/repos/vercel/next.js/releases",
#                     "Node.js": "https://api.github.com/repos/nodejs/node/releases",
#                     "Spring Boot": "https://api.github.com/repos/spring-projects/spring-boot/releases",
#                     "ReactJS": "https://api.github.com/repos/facebook/react/releases"
#                 }.get(tech_name)
#
#                 # For remaining technologies, use the randomuser.me API
#                 if not api_url:
#                     api_url = "https://randomuser.me/api/"
#
#                 try:
#                     # Fetch the update data from the API
#                     response = requests.get(api_url)
#                     response.raise_for_status()
#                     update_data = response.json()
#
#                     # Extract the release information
#                     if 'tag_name' in update_data[0]:
#                         update_description = f"Latest release: {update_data[0]['tag_name']}"
#                     else:
#                         return f"Unexpected data format for {tech_name} from API."
#
#                 except Exception as e:
#                     return f"Error fetching update data for {tech_name}: {str(e)}"
#
#                 # Check if the update already exists
#                 latest_update = Update.query.filter_by(tech_id=tech_id).order_by(Update.update_date.desc()).first()
#                 if latest_update and latest_update.update_description == update_description:
#                     continue  # Skip if no new update
#
#                 # Create a new update record
#                 new_update = Update(
#                     tech_id=tech_id,
#                     update_type="New Release",
#                     update_description=update_description,
#                     update_date=datetime.utcnow(),
#                     created_at=datetime.utcnow()
#                 )
#                 db_session.add(new_update)
#
#                 # Create notifications for all users subscribed to this technology
#                 subscriptions = Subscription.query.filter_by(tech_id=tech_id).all()
#                 notifications_list = [
#                     UserNotification(
#                         notification_id=str(uuid.uuid4()),
#                         user_id=sub.user_id,
#                         read=False,
#                         title=tech_name,
#                         message=new_update.update_description,
#                         url=tech.releases,
#                         created_at=datetime.utcnow(),
#                         isactive=True
#                     )
#                     for sub in subscriptions
#                 ]
#                 db_session.add_all(notifications_list)
#
#             # Commit changes to the database
#             db_session.commit()
#
#             # Trigger the /auto endpoint if needed
#             try:
#                 post_url = f"{current_app.config['BASE_URL']}/auto"
#                 post_response = requests.post(post_url, json={})
#                 if post_response.status_code == 200:
#                     return "Successfully triggered the /auto endpoint."
#                 else:
#                     return f"Failed to trigger /auto. Status Code: {post_response.status_code}"
#             except Exception as e:
#                 return f"Error triggering /auto: {str(e)}"
#
#         except Exception as e:
#             return f"Error in fetch_and_create_updates: {str(e)}"
# class TaskService:
#
#     # Helper function to get tech IDs and names
#     def get_tech_id_map(self):
#         tech_map = {}
#         technologies = Technology.query.all()
#         for tech in technologies:
#             tech_id = str(tech.tech_id)
#             tech_map[tech_id] = tech.tech_name
#         return tech_map
#
#     # Helper function to fetch updates from API
#
#     def fetch_update_from_api(self, api_url):
#         try:
#             # Fetch data from the provided API URL
#             response = requests.get(api_url)
#             if response.status_code != 200:
#                 return f"Error: Failed to fetch update data, status code: {response.status_code}"
#
#             update_data = response.json()
#
#             # Log the fetched data for debugging purposes
#             # logging.info(f"Fetched data: {update_data}")
#
#             # Handle public API (search by 'tag_name')
#             if isinstance(update_data, list) and len(update_data) > 0:
#                 # Check for 'tag_name' in public APIs (e.g., GitHub)
#                 if 'tag_name' in update_data[0]:
#                     return f"Latest release found: {update_data[0]['tag_name']}"
#
#                 # If 'tag_name' is not found, check for 'name' in random APIs (e.g., randomuser.me)
#                 if 'results' in update_data and len(update_data['results']) > 0:
#                     first_entry = update_data['results'][0]
#                     first_name = first_entry.get('name', {}).get('first', 'N/A')
#                     last_name = first_entry.get('name', {}).get('last', 'N/A')
#                     email = first_entry.get('email', 'N/A')
#                     return f"First Name: {first_name}, Last Name: {last_name}, Email: {email}"
#
#             # If the format doesn't match the expected structure, return an error
#             return "Error: Update data format is unexpected or unsupported."
#
#         except Exception as e:
#             return f"Error: {str(e)}"
#
#     # Helper function to get API URL based on technology name
#     def get_api_url(self, tech_name):
#         api_map = {
#             "Next.js": "https://api.github.com/repos/vercel/next.js/releases",
#             "Node.js": "https://api.github.com/repos/nodejs/node/releases",
#             "Spring Boot": "https://api.github.com/repos/spring-projects/spring-boot/releases",
#             "ReactJS": "https://api.github.com/repos/facebook/react/releases",
#         }
#         return api_map.get(tech_name, "https://randomuser.me/api/")
#
#     # Task service function to fetch updates for all technologies and store them in the database
#     def fetch_and_store_tech_updates(self):
#         technologies = Technology.query.all()
#         notifications_list = []
#
#         for tech in technologies:
#             tech_id = tech.tech_id
#             tech_name = tech.tech_name
#             api_url = self.get_api_url(tech_name)
#
#             # Fetch the update from the API
#             update_description = self.fetch_update_from_api(api_url)
#             if update_description.startswith("Error"):
#                 return update_description  # Return error message if there was an issue fetching the update
#
#             # Check if there's an existing update
#             latest_update = Update.query.filter_by(tech_id=tech_id).order_by(Update.update_date.desc()).first()
#
#             # Only store new updates
#             if latest_update and latest_update.update_description == update_description:
#                 continue  # No new update
#
#             # Create a new update entry
#             new_update = Update(
#                 tech_id=tech_id,
#                 update_type="New Release",  # Or other appropriate type
#                 update_description=update_description,
#                 update_date=datetime.utcnow(),
#                 created_at=datetime.utcnow()
#             )
#
#             # Save the new update
#             db.session.add(new_update)
#
#             # Fetch subscriptions and prepare notifications
#             subscriptions = Subscription.query.filter_by(tech_id=tech_id).all()
#             for subscription in subscriptions:
#                 notification = UserNotification(
#                     notification_id=str(uuid.uuid4()),
#                     user_id=subscription.user_id,
#                     read=False,
#                     title=tech_name,
#                     message=update_description,
#                     url=tech.releases,  # Assuming 'releases' is the URL or API link
#                     created_at=datetime.utcnow(),
#                     isactive=True
#                 )
#                 notifications_list.append(notification)
#
#             db.session.add_all(notifications_list)
#
#         # Commit the transaction to save updates and notifications
#         try:
#             db.session.commit()
#             return {'message': 'Technology updates fetched and notifications sent successfully.'}
#         except Exception as e:
#             db.session.rollback()
#             return {'message': f"Error saving updates or notifications: {str(e)}"}
#
#     # Example Task Service function call (you can use this to invoke the task)
#     def trigger_fetch_tech_updates(self):
#         result = self.fetch_and_store_tech_updates()
#         return result

def get_first_five_lines(text):
    lines = text.split('\n')
    return '\n'.join(lines[:6])


def notify_subscribed_users(tech_id, tech_name, new_data):
    """
    Sends notifications to users subscribed to a specific technology update.

    Args:
    - tech_id: ID of the technology
    - tech_name: Name of the technology
    - new_data: The new update data (message, details, etc.)
    """
    try:
        # Get all subscriptions for this technology
        subscriptions = Subscription.query.filter_by(tech_id=tech_id).all()

        if not subscriptions:
            print(f"No users subscribed to {tech_name}.")
            return

        # Create and store notifications for each subscriber
        notifications_list = [
            UserNotification(
                notification_id=str(uuid.uuid4()),  # Generate a unique notification ID
                user_id=sub.user_id,  # User to whom the notification is directed
                read=False,  # Default to unread
                title=f"New update for {tech_name}",
                message=new_data['message'],  # Message to display in the notification
                url=tech_name,  # Can be a link to the technology or the release page
                created_at=datetime.utcnow(),  # Timestamp when the notification was created
                isactive=True  # Notification is active
            )
            for sub in subscriptions
        ]

        # Add all notifications to the session
        db.session.add_all(notifications_list)
        db.session.commit()
        print(f"Notifications sent to {len(notifications_list)} users for {tech_name}.")

    except Exception as e:
        print(f"Error notifying users for {tech_name}: {e}")


def fetch_updates():
    print("Running cron job to fetch technology updates")

    technologies = Technology.query.all()

    for tech in technologies:
        try:
            # Replace apiUrl with releases
            # Make a GET request to fetch the release data using the releases URL from the tech object
            response = requests.get(tech.releases)  # Use the releases attribute
            response_data = response.json()  # Assuming JSON response

            # Initialize message and update_identifier variables
            message = ""
            update_identifier = ""

            # Handle the response directly based on different API sources
            if "api.github.com" in tech.releases:
                # For GitHub API response, extract the latest release tag (e.g., v3.4.0-M3)
                message = f"Latest release: {response_data[0]['tag_name']}" if response_data else "No releases found"
                update_identifier = response_data[0]['tag_name'] if response_data else 'No tag'

            elif "randomuser.me" in tech.releases:
                # For randomuser.me, extract the user's email and generate the message
                if response_data and 'results' in response_data and response_data['results']:
                    user = response_data['results'][0]
                    first_name = user.get('name', {}).get('first', 'Unknown')
                    last_name = user.get('name', {}).get('last', 'User')
                    email = user.get('email', 'No email')

                    # Create the update message and description
                    message = f"User email: {email}"
                    update_identifier = email  # Email as the identifier for randomuser.me
                    update_description = f"New update from AWS: {first_name} {last_name}"
                else:
                    message = "No data found"
                    update_identifier = 'No email'

            else:
                # Default case for other APIs or no valid releases
                message = "No valid data available"
                update_identifier = "Unknown"

            # Package the parsed data into a dictionary for notification
            new_data = {
                'message': message,
                'details': response_data,
                'updateIdentifier': update_identifier
            }

            # Check if there is a new update to save
            # Query the database for the most recent update for this tech_id
            existing_update = Update.query.filter_by(tech_id=tech.tech_id).order_by(Update.created_at.desc()).first()

            # If an existing update is found, compare the current message with the last saved update
            if existing_update:
                last_message = existing_update.update_description
                last_update_identifier = existing_update.update_type

                # Check if the current message and identifier match the previous update
                is_same_update = (last_message == message) and (last_update_identifier == update_identifier)
                print(f"Is Same Update: {is_same_update}")  # Debug print to check if the update is the same

                # If the update is different, save the new update to the database
                if not is_same_update:
                    update = Update(
                        tech_id=tech.tech_id,
                        update_type=update_identifier,
                        update_description=message
                    )
                    db.session.add(update)  # Add the new update to the session
                    db.session.commit()  # Commit the transaction to the database
                    print(f"Notification updated for technology: {tech.tech_name}")

                    # Notify subscribed users
                    notify_subscribed_users(tech.tech_id, tech.tech_name, new_data)
                else:
                    print(f"No new updates for {tech.tech_name}, skipping notification.")
            else:
                print(f"No existing updates found for technology: {tech.tech_name}")
        except Exception as error:
            print(f"Error fetching data for {tech.tech_name}: {error}")
