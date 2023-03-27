import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        self.server.starttls()
        self.server.login(self.email, self.password)
        self.body_html=""

    def send_email(self, to_email, subject):
        msg = MIMEMultipart()
        msg["From"] = self.email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(self.body_html, "html"))
        self.server.sendmail(self.email, to_email, msg.as_string())

    def close(self):
        self.server.quit()

    def create_html(self, list,list_names):
        self.body_html = "<html>\n<body>\n<ul>\n"
        for j in range(len(list)):
            self.body_html += f"<li><a href={list[j]}>{list_names[j]}<a/></li>\n"
            self.body_html += "</ul>\n</body>\n</html>"