# 이메일 보내기 앱
import smtplib # Simple Mail Transfer Protocol메일전송프로토콜
from email.mime.text import MIMEText # Multipurpose Interner Mail Extenstions

send_email = 'tn7969@anver.com'
send_pass = 'daspiobfy8554!' # 임시 비밀번호

recv_email = 'tn7969@naver.com'

smtp_name = 'smtp.naver.com'
smtp_port = 465 # 포트번호

text = '''메일 내용입니다. 긴급입니다. 조심하세요~ 빨리 연락주세요'''

msg = MIMEText(text)
msg['Subject'] = '메일 제목입니다'
msg['From'] = send_email # 보내는 메일
msg['To'] = recv_email # 받는 메일
print(msg.as_string())

mail = smtplib.SMTP_SSL(smtp_name, smtp_port) # SMTP 객체생성
mail.starttls() # 전송계층 보안시작dd
mail.login(send_email, send_pass)
mail.sendmail(send_email, recv_email, msg=msg.as_string())
mail.quit()
print('전송완료')