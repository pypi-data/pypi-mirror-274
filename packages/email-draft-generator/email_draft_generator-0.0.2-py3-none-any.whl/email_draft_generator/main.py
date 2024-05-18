import os
import json
import concurrent.futures
import fileinput

import email_draft_generator.gmail
import email_draft_generator.mail_util
import email_draft_generator.email_creator

def main():
	# File paths
	# TODO: Move these to global paths
	google_token_path = ".credentials/token.json"
	google_oauth_credentials_path = ".credentials/credentials.json"

	# Load the companies from the JSON file
	print("Processing input data")
	json_data = ""
	for line in fileinput.input():
		json_data += line
	companies = json.loads(json_data)

	# Load the template, or use the default if none is provided
	# TODO: Create a command line argument for the template path
	template_path = "data/template.json"
	if os.path.exists(template_path):
		with open(template_path) as f:
			template = json.load(f)
			print("Template loaded from file")
	else:
		template = {
			'subject': "Test E-mail",
			'body': """This is a template E-mail used to test an E-mail generation program. Please disregard.

company.name: {name}
company.email: {email}""",
		}
		print("No template provided! Sample template was used")

	# Authenticate with Google
	print("Authenticating")
	creds = email_draft_generator.gmail.get_creds(google_token_path, google_oauth_credentials_path)

	# Build all of the attachments
	attachments = []
	if 'attachments' in template:
		print("Processing attachments")
		with concurrent.futures.ProcessPoolExecutor() as executor:
			for attachment_path in template['attachments']:
				attachments.append(email_draft_generator.mail_util.build_attachment(attachment_path))

	print("Generating and uploading E-mails")
	with concurrent.futures.ProcessPoolExecutor() as executor:
		for company in companies:
			email_draft_generator.gmail.create_draft(creds, email_draft_generator.email_creator.create_email_body(template, company, attachments))