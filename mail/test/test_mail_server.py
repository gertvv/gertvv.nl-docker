import pytest
import socket
import ssl
import smtplib
import imaplib
import os

# NOTE: these tests expect to run against a dummy container without any previously received email

hostname = os.environ.get('MAIL_SERVER_HOSTNAME') 
container_ip = os.environ.get('MAIL_SERVER_CONTAINER_IP')
email_user = os.environ.get('MAIL_SERVER_USERNAME')
email_pass = os.environ.get('MAIL_SERVER_PASSWORD')
context = ssl.create_default_context()
context.check_hostname = True

# Context with host check disabled for when we're not in control of the hostname
# TODO: way around this? https://unix.stackexchange.com/a/56288/107679
context_no_host_check = ssl.create_default_context()
context_no_host_check.check_hostname = False 


def test_imap_ssl_certificate():
    with socket.create_connection((container_ip, 993)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            assert ('DNS', hostname) in ssock.getpeercert()['subjectAltName']

def test_smtp_ssl_certificate():
    with socket.create_connection((container_ip, 465)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            assert ('DNS', hostname) in ssock.getpeercert()['subjectAltName']

def test_imap_starttls_certificate():
    with imaplib.IMAP4(container_ip) as imap:
        imap.starttls(ssl_context=context_no_host_check) # TODO: host check

def test_smtp_starttls_certificate():
    with smtplib.SMTP(container_ip) as smtp:
        smtp.starttls(context=context_no_host_check) # TODO: host check

@pytest.mark.skip(reason="Port 587 (Mail Submissio Agent) SMTP currently disabled")
def test_smtp_msa_starttls_certificate():
    with smtplib.SMTP(container_ip, port=587) as smtp:
        smtp.starttls(context=context_no_host_check) # TODO: host check

def test_smtp_local_delivery_allowed():
    with smtplib.SMTP(container_ip, local_hostname='example.com') as smtp:
        smtp.sendmail('test@example.com', 'gert@gertvv.nl',
            'From: test@example.com\nTo: gert@gertvv.nl\nSubject: testing 123\n\nTesting!')

def test_smtp_relay_forbidden():
    with smtplib.SMTP(container_ip, local_hostname='gertvv.nl') as smtp:
        with pytest.raises(smtplib.SMTPRecipientsRefused):
            smtp.sendmail('gert@gertvv.nl', 'test@example.com',
                'From: gert@gertvv.nl\nTo: test@example.com\nSubject: testing 123\n\nTesting!')

def test_smtp_auth_requires_ssl():
    with smtplib.SMTP(container_ip) as smtp:
        with pytest.raises(smtplib.SMTPNotSupportedError):
            smtp.login('test', 'test1234')

def test_smtp_auth_invalid_credentials():
    with smtplib.SMTP_SSL(container_ip, port=465, context=context_no_host_check) as smtp:
        with pytest.raises(smtplib.SMTPAuthenticationError):
            smtp.login('test', 'test1234')

def test_smtp_authenticated_relay():
    with smtplib.SMTP_SSL(container_ip, port=465, context=context_no_host_check) as smtp:
        smtp.login(email_user, email_pass)
        smtp.sendmail('gert@gertvv.nl', 'test@example.com',
            'From: gert@gertvv.nl\nTo: test@example.com\nSubject: testing 123\n\nTesting!')

def test_imaps_list_messages():
    with imaplib.IMAP4_SSL(container_ip, port=993, ssl_context=context_no_host_check) as imap:
        res, msg = imap.login(email_user, email_pass)
        assert res == 'OK'
        res, msg = imap.list()
        assert res == 'OK'
        res, msg = imap.select('INBOX')
        assert res == 'OK'
        res, msg = imap.fetch('1', '(BODY[HEADER.FIELDS (Subject)])')
        subject = msg[0][1].decode('utf-8')
        assert subject.startswith('Subject: testing 123')

def test_spamassassin_active():
    with imaplib.IMAP4_SSL(container_ip, port=993, ssl_context=context_no_host_check) as imap:
        res, msg = imap.login(email_user, email_pass)
        assert res == 'OK'
        res, msg = imap.select('INBOX')
        assert res == 'OK'
        res, msg = imap.fetch('1', '(BODY[HEADER.FIELDS (X-Spam-Checker-Version)])')
        checker = msg[0][1].decode('utf-8')
        assert checker.startswith('X-Spam-Checker-Version: SpamAssassin')
