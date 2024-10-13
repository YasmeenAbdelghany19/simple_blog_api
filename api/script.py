import smtplib

smtp_server = "smtp.mailmug.net"
port = 2525
username = "ytb00jijgfnjbzf5"
password = "rzqcq38qzqmbugah"
try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()  # Identify ourselves to the SMTP server
    # server.starttls()  # Secure the connection
    server.login(username, password)  # Try to log in
    print("Logged in successfully!")
except smtplib.SMTPAuthenticationError as e:
    print(f"Authentication failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    server.quit()
