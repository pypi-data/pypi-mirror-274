import base64
from email.message import EmailMessage

def create_email_body(company, attachments):
	"""Generates an E-mail with the provided company name and attachments"""
	mime_message = EmailMessage()

	# headers
	# TODO: Pull these from a configuration file
	mime_message["To"] = company['email']
	# Doesn't seem to be required for Gmail
	# mime_message["From"] = ""
	mime_message["Subject"] = "sample with attachment"

	# text
	mime_message.set_content(f"""Dear {company['name']},

We are pleased to inform you that your company has been selected for a special offer.
Please find attached the details of the offer.

Best regards,
Your Company""")

	# Add attachments
	for attachment in attachments:
		mime_message.add_attachment(attachment['data'], maintype=attachment['maintype'], subtype=attachment['subtype'], filename=attachment['name'])

	encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

	return {"message": {"raw": encoded_message}}