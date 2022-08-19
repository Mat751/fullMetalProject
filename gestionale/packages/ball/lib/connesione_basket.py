
import ftplib

pasw='5H%5rsz6&mr97Yh1'

with ftplib.FTP('erp.pallacanestrocuoricinocardano.com', 'palcancarerp21', pasw) as ftp:
    ip=ftp.getwelcome().split(" ")[4]
    print(ip)
ftp.close()