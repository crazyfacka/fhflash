import smtplib
import ssl

def send_success_mail(mail_confs, class_to_book):
  message = """\
From: FH Flash <%s>
To: %s <%s>
Subject: %s marcada

This message is sent from FH Flash booker.""" % (mail_confs["user"], mail_confs["to"]["name"], mail_confs["to"]["mail"], class_to_book)

  context = ssl.create_default_context()
  
  try:
    server = smtplib.SMTP(mail_confs["host"], mail_confs["port"])
    server.starttls(context=context)
    server.login(mail_confs["user"], mail_confs["password"])
    server.sendmail(mail_confs["user"], mail_confs["to"]["mail"], message)
  except Exception as e:
    print(e)
  finally:
    server.quit()