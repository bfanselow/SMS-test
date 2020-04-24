#!/usr/bin/env python
"""
  File: sms_test.py
  Description:
    Simple API for exposing several Strava API-access methods including
    processing the Strava OAuth steps to get a "scoped" access_token
  Usage: 
   1) Populate "twilio.auth.json" file with JSON format 
        { "account_sid": "<sid>", "auth_token": "<token>", "source_number": "<number>" } 
      These come from your Twillio account registration.
   2) Execute: $ ./sms_test.py <dest-phone-number> [-m <message>]
       where dest-phone-number must be a Twillio verified number

"""

import os
import sys 
import json
import logging
import argparse

from twilio.rest import Client

## local Twillio auth file in json format 
AUTH_FILE = './twilio.auth.json'

myname = os.path.basename(__file__)

DEBUG = 0

##-----------------------------------------------------------------------------------
class AuthError(Exception):
  pass

##-----------------------------------------------------------------------------------
def load_auth_credentials(auth_file_path):
  """
   Read the auth-credential file and load the required auth parameters.
   File should have json format:
     { "account_sid": "<sid>", "auth_token": "<token>", "source_number": "<number>" } 
   Required args: path to auth_file
   Return (tuple): ( account_sid, auth_token, source_number ) 
  """
  print("Loading auth file data: %s..." % (auth_file_path))

  if not os.path.exists(auth_file_path):
    raise AuthError("Auth file not found: [%s]" % (auth_file_path))
  if not os.access(auth_file_path, os.R_OK):
    raise AuthError("Auth file cound not be read: [%s]" % (auth_file_path))

  with open(auth_file_path) as f:
    auth_data = json.load(f) 

    account_sid = auth_data.get('account_sid', None)
    auth_token = auth_data.get('auth_token', None)
    source_number = auth_data.get('source_number', None)
    if not account_sid:
      raise AuthError("%s: Failed to retrieve auth value: [account_sid]")
    if not auth_token:
      raise AuthError("%s: Failed to retrieve auth value: [auth_token]")
    if not source_number:
      raise AuthError("%s: Failed to retrieve auth value: [source_number]")

  return( account_sid, auth_token, source_number )

##-----------------------------------------------------------------------------------
def clean_dest_number(dest_number):
  """
    Take our intput source phone-number and verify/reformat it into proper syntax
    303-111-2222 => '+13031112222'
  """


  return(dest_number)

##-----------------------------------------------------------------------------------
def sms_send(message, sid, token, sms_source, sms_dest ):

  client = Client(sid, token)

  sms_message = client.messages.create(
       body=message,
       from_=sms_source,
       to=sms_dest
  )

  return(sms_message)

##-----------------------------------------------------------------------------------
if __name__ == "__main__":

  default_message = "%s: Testing! Are you there?" % (myname)

  my_parser = argparse.ArgumentParser( prog=myname, 
                                       usage='%(prog)s [options] <dest-phone-number>',
                                       description='Send SMS message to dest-phone-number'
                                      )

  my_parser.add_argument(
                         'DestNumber',           
                          metavar='dest',
                          type=str,
                          help='destination phone number'
                        )
  my_parser.add_argument(
                          '-d', '--debug',                 
                          required=False,
                          type=int,
                          #metavar='debug',
                          help='set debug level'
                        )
  my_parser.add_argument(
                          '-m', '--msg',                 
                          required=False,
                          metavar='message',
                          type=str,
                          help='Optional message to send'
                        )


  # Execute the parse_args() method
  args = my_parser.parse_args()
  print("%s: INPUT-ARGS: %s" % (myname, vars(args)))

  dest_number = args.DestNumber
  if args.debug:
    DEBUG = args.debug

  message = default_message
  if args.msg:
    message = args.msg

  (account_sid, auth_token, source_number) = load_auth_credentials(AUTH_FILE)

  ## TODO
  ## dest_number = clean_dest_number(dest_number)

  resp = sms_send(message, account_sid, auth_token, source_number, dest_number )

  print(resp.__dict__)
