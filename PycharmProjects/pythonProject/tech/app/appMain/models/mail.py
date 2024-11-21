from random import random

import smtplib
import random
from flask import make_response,request
from flask_restx import Resource
from requests import request
# from  app.appMain.d import Mail
# email_verify = Mail.mail
# my_mail = "techupdate.notifier@gmail.com"
# password = "dgfn ytwn ihev mdxx "
# @email_verify.route('',methods=['GET'])
# class VerifyMail():
#     def get(self,reset_token,email):
        # data = request.args.get('email')
        # random_number = random.randint(0, 999999)
        # print(1)
        # OTP = str(random_number).zfill(6)
        # with smtplib.SMTP("smtp.gmail.com",587) as connection:
            # print(2)
            # connection.starttls()
            # connection.login(user=my_mail, password=password)
            # connection.sendmail(from_addr=my_mail, to_addrs=f"{email}",msg=f"Subject:Password reset request\n\n You requested a password reset. Click here to reset your password:http://localhost:4200/reset-password/{reset_token}If it's not you, please contact us.")
            #
            #
            # print("mail sent")
            # return make_response(OTP,201)

# VerifyMail().get()