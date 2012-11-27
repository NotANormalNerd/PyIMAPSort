'''
Created on 27.11.2012

@author: dschmala
'''
import imaplib
import datetime

subj_rules = {'SubjectContains':'Folder', '[News]':'NewsFolder'}

def print_inbox(imap):
        typ, data = mail.search(None, 'ALL')
        for num in data[0].split():
                typ, data = mail.fetch(num, '(UID BODY[HEADER.FIELDS (FROM)])')
                print data[0]

def sort_by_subject(imap):
        typ, data = mail.search(None, 'ALL')
        for num in data[0].split():
                try:
                        typ, data = mail.fetch(num, '(UID BODY[HEADER.FIELDS (SUBJECT)])')
                except imaplib.IMAP4.error:
                        continue;
                subj = data[0][1]
                for key in subj_rules:
                        if key in subj:
                                mail.copy(num, subj_rules[key])
                                mail.store(num, '+FLAGS', '\\Deleted')
                                print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+' - IMAPSort: Moved '+subj+'with UID '+num+' to '+subj_rules[key]

                mail.expunge()


if __name__ == '__main__':
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+' - IMAPSort: Starting sorting your IMAP_Mails'
    mail = imaplib.IMAP4_SSL('imap.server')
    mail.login('email','password')
    mail.select('INBOX')
    sort_by_subject(mail)
    mail.close()
    mail.logout()
