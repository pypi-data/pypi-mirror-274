import json
import concurrent.futures
import argparse

import email_draft_generator.gmail
import email_draft_generator.mail_util
import email_draft_generator.email_creator

def main():
	# Command-line arguments
	parser = argparse.ArgumentParser(
		prog='email-generator',
		description='Generates E-mail drafts from a list of E-mail addresses and uploads them to Gmail.'
	)

	parser.add_argument('-t', '--template', type=argparse.FileType('r'), help='the template file to use')
	parser.add_argument('infile', type=argparse.FileType('r'), help='the list of e-mail addresses to parse')

	args = parser.parse_args()

	# File paths
	# TODO: Use a keyring for these
	google_token_path = ".credentials/token.json"
	google_oauth_credentials_path = ".credentials/credentials.json"

	# Load the companies from the JSON file
	print("Processing input data")
	companies = json.load(args.infile)

	# Load the template, or use the default if none is provided
	if args.template:
		template = json.load(args.template)
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