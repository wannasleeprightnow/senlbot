import email
from email.header import decode_header
import imaplib

from config import MailConfig


class Schedule:
    def __init__(self) -> None:
        self.logined_mail = ""

    def _connect_imap_server(self) -> str:
        if not self.logined_mail:
            mail = imaplib.IMAP4_SSL(MailConfig.IMAP_SERVER)
            mail.login(MailConfig.TARGET_MAIL, MailConfig.TARGET_MAIL_PASSWORD)
            mail.select("inbox")
            self.logined_mail = mail
        return self.logined_mail

    def _get_new_mails(self) -> list | None:
        status, data = self.logined_mail.search(None, "UNSEEN")
        if status == "OK":
            return data[0].split()

    def _get_mail_data(self, mail_id):
        status, mail_data = self.logined_mail.fetch(mail_id, "(RFC822)")
        if status == "OK":
            return email.message_from_bytes(mail_data[0][1])

    def _check_sender(self, message) -> bool:
        return MailConfig.SENDER_MAIL in message["From"]

    def _check_multipart(self, message) -> bool:
        return message.get_content_maintype() == "multipart"

    def _get_filename(self, part) -> str | None:
        if not (part in ("multipart", "text")):
            return part.get_filename()

    def _check_filename(self, filename) -> str | None:
        filename, charset = decode_header(filename)[0]
        if charset:
            filename = filename.decode(charset)
            if MailConfig.FIND_FILENAME in filename:
                return filename

    def _write_file(self, part) -> None:
        with open(MailConfig.SAVE_FILENAME, "wb") as file:
            file.write(part.get_payload(decode=True))

    def _check_mail(self, mail_id):
        mail = self._get_mail_data(mail_id)
        if self._check_sender(mail):
            if self._check_multipart(mail):
                for part in mail.walk():
                    if filename := self._get_filename(part):
                        if self._check_filename(filename):
                            self._write_file(part)
                            return True

    def is_new_exists(self):
        self._connect_imap_server()
        for mail_id in self._get_new_mails():
            if self._check_mail(mail_id):
                return True
