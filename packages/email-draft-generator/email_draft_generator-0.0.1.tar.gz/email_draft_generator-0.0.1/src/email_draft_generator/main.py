import json
import concurrent.futures
import fileinput

import email_generator.gmail
import email_generator.mail_util
import email_generator.email_creator

def main():
	# File paths
	# TODO: Move these to global paths
	google_token_path = ".credentials/token.json"
	google_oauth_credentials_path = ".credentials/credentials.json"
	# TODO: Pull attachments from a directory
	attachment_paths = []

	# Load the companies from the JSON file
	print("Processing input data")
	json_data = ""
	for line in fileinput.input():
		json_data += line
	companies = json.loads(json_data)

	# Authenticate with Google
	print("Authenticating")
	creds = email_generator.gmail.get_creds(google_token_path, google_oauth_credentials_path)

	# Build all of the attachments
	print("Processing attachments")
	attachments = []
	with concurrent.futures.ProcessPoolExecutor() as executor:
		for attachment_path in attachment_paths:
			attachments.append(email_generator.mail_util.build_attachment(attachment_path))

	print("Generating and uploading E-mails")
	with concurrent.futures.ProcessPoolExecutor() as executor:
		for company in companies:
			email_generator.gmail.create_draft(creds, email_generator.email_creator.create_email_body(company, attachments))