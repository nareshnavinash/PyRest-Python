import os
import json
import glob
import datetime
from shovel import task
from gmail import GMail
from gmail import Message

@task
def email(to_email="nareshnavinash@gmail.com", jenkins_url="Not set from cli", git_branch="Not set from cli", git_commit="Not set from cli", git_commiter_email="Not set from cli"):
    """Emails the consolidated report to the recipients"""
    failed = 0
    passed = 0
    broken = 0
    failed_cases = []
    broken_cases = []
    attachments = []
    for file in glob.glob("reports/allure/*result.json"):
        f = open(os.getcwd() + "/" + file, 'r')
        file_data_as_string = f.readlines()
        json_values = json.loads(file_data_as_string[0])
        try:
            if json_values['status'] == "passed":
                passed = passed + 1
            elif json_values['status'] == "failed":
                failed = failed + 1
                failed_cases.append(json_values['name'])
            else:
                broken = broken + 1
                broken_cases.append(json_values['name'])
        except Exception as e:
            broken = broken + 1
            broken_cases.append(json_values['name'])
            print(e)
    print("Passed - " + str(passed))
    print("Failed - " + str(failed))
    print("Broken - " + str(broken))

    # Email parameters
    email = "nareshapitest@gmail.com"  # to send the email from this account
    password = "Test@123"
    gmail = GMail(email, password)
    current_time = str(datetime.datetime.now())
    if failed == 0 and broken == 0:
        email_subject = "Automation - Report " + current_time
    else:
        email_subject = "Automation - Report " + current_time + " - Alert failure(s) found !!!"

    if len(failed_cases) != 0:
        final_string = ""
        for cases in failed_cases:
            final_string = final_string + "<li>" + cases + "</li>"
        failed_testcases_string = "Failed Test Cases, \n<ul>\n" + final_string + "\n</ul>"
    else:
        failed_testcases_string = ""
    if len(broken_cases) != 0:
        final_string = ""
        for cases in broken_cases:
            final_string = final_string + "<li>" + cases + "</li>"
        broken_testcases_string = "Broken Test Cases, \n<ul>\n" + final_string + "\n</ul>"
    else:
        broken_testcases_string = ""
    for file in glob.glob("reports/*.html"):
        attachments.append(file)
    html_body = "" \
        "<body style=\"margin: 0; padding: 0;\">" \
        "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\" style=\"background: #f3f3f3; min-width: 350px; font-size: 1px; line-height: normal;\">" \
           "<tr>" \
             "<td align=\"center\" valign=\"top\">" \
               "<!--[if (gte mso 9)|(IE)]>" \
                 "<table border=\"0\" cellspacing=\"0\" cellpadding=\"0\">" \
                 "<tr><td align=\"center\" valign=\"top\" width=\"750\"><![endif]-->" \
               "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"750\" class=\"table750\" style=\"width: 100%; max-width: 750px; min-width: 350px; background: #f3f3f3;\">" \
                 "<tr>" \
                       "<td class=\"mob_pad\" width=\"25\" style=\"width: 25px; max-width: 25px; min-width: 25px;\">&nbsp;</td>" \
                   "<td align=\"center\" valign=\"top\" style=\"background: #ffffff;\">" \
                          "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\" style=\"width: 100% !important; min-width: 100%; max-width: 100%; background: #f3f3f3;\">" \
                             "<tr>" \
                                "<td align=\"right\" valign=\"top\">" \
                                   "<div class=\"top_pad\" style=\"height: 25px; line-height: 25px; font-size: 23px;\">&nbsp;</div>" \
                                "</td>" \
                             "</tr>" \
                          "</table>" \
                          "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\" style=\"width: 100% !important; min-width: 100%; max-width: 100%; background: #f3f3f3;\">" \
                             "<tr>" \
                                "<td align=\"right\" valign=\"top\">" \
                                   "<div class=\"top_pad\" style=\"height: 25px; line-height: 25px; font-size: 23px;\">&nbsp;</div>" \
                                "</td>" \
                             "</tr>" \
                          "</table>" \
                          "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"88%\" style=\"width: 88% !important; min-width: 88%; max-width: 88%;\">" \
                             "<tr>" \
                                "<td align=\"left\" valign=\"top\">" \
                                   "<div style=\"height: 10px; line-height: 33px; font-size: 31px;\">&nbsp;</div>" \
                                   "<div class=\"header\" align=\"center\">" \
                                     "<h2 style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #3375AA; font-size: 32px; line-height: 32px;\">Automation Report</h2>" \
                                   "</div>" \
                                   "<div style=\"height: 10px; line-height: 33px; font-size: 31px;\">&nbsp;</div>" \
                                   "<font face=\"'Source Sans Pro', sans-serif\" color=\"#1a1a1a\" style=\"font-size: 24px; line-height: 32px;\">" \
                                      "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 20px; line-height: 32px;\">Hi Team,</span>" \
                                   "</font>" \
                                   "<div style=\"height: 33px; line-height: 33px; font-size: 31px;\">&nbsp;</div>" \
                                   "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                      "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 20px; line-height: 32px;\">Automation Regression Status,</span>" \
                                   "</font>" \
                                   "<div style=\"height: 20px; line-height: 20px; font-size: 20px;\">&nbsp;</div>" \
                                   "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"88%\" style=\"width: 88% !important; min-width: 88%; max-width: 88%;\">" \
                                      "<tr>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 18px; line-height: 32px;\">Passed Test Case count :</span>" \
                                            "</font>" \
                                         "</td>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #0E9C4A; font-size: 18px; line-height: 32px;\">" + str(passed) + "</span>" \
                                            "</font>" \
                                         "</td>" \
                                      "</tr>" \
                                      "<tr>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 18px; line-height: 32px;\">Failed Test Case count :</span>" \
                                            "</font>" \
                                         "</td>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #B2230F; font-size: 18px; line-height: 32px;\">" + str(failed) + "</span>" \
                                            "</font>" \
                                         "</td>" \
                                      "</tr>" \
                                      "<tr>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 18px; line-height: 32px;\">Broken Test Case count :</span>" \
                                            "</font>" \
                                         "</td>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #E6C404; font-size: 18px; line-height: 32px;\">" + str(broken) + "</span>" \
                                            "</font>" \
                                         "</td>" \
                                      "</tr>" \
                                      "<tr>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 18px; line-height: 32px;\">Run Completed at :</span>" \
                                            "</font>" \
                                         "</td>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #130145; font-size: 18px; line-height: 32px;\">" + str(current_time) + "</span>" \
                                            "</font>" \
                                         "</td>" \
                                      "</tr>" \
                                   "</table>" \
                                   "<div style=\"height: 33px; line-height: 33px; font-size: 31px;\">&nbsp;</div>" \
                                   "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                      "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 18px; line-height: 32px;\">HTML Reports are attached for reference. Below are the few parameters that are responsible for this job trigger. If any failures or broken cases found in the result kindly trace back from the last commit ID with the last commited user.</span>" \
                                   "</font>" \
                                   "<div style=\"height: 20px; line-height: 20px; font-size: 31px;\">&nbsp;</div>" \
                                   "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"88%\" style=\"width: 88% !important; min-width: 88%; max-width: 88%;\">" \
                                      "<tr>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 17px; line-height: 32px;\">Jenkins URL:</span>" \
                                            "</font>" \
                                         "</td>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<a href=\"" + jenkins_url +"\" style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #130145; font-size: 17px; line-height: 32px;\">navigate_to_jenkins</a>" \
                                            "</font>" \
                                         "</td>" \
                                      "</tr>" \
                                      "<tr>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 17px; line-height: 32px;\">Git Branch:</span>" \
                                            "</font>" \
                                         "</td>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #130145; font-size: 17px; line-height: 32px;\">" + git_branch + "</span>" \
                                            "</font>" \
                                         "</td>" \
                                      "</tr>" \
                                      "<tr>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 17px; line-height: 32px;\">Last Commit ID:</span>" \
                                            "</font>" \
                                         "</td>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #130145; font-size: 17px; line-height: 32px;\">" + git_commit + "</span>" \
                                            "</font>" \
                                         "</td>" \
                                      "</tr>" \
                                      "<tr>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 17px; line-height: 32px;\">Last Commit by:</span>" \
                                            "</font>" \
                                         "</td>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #130145; font-size: 17px; line-height: 32px;\">" + git_commiter_email + "</span>" \
                                            "</font>" \
                                         "</td>" \
                                      "</tr>" \
                                   "</table>" \
                                   "<div style=\"height: 33px; line-height: 33px; font-size: 31px;\">&nbsp;</div>" \
                                   "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                      "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 18px; line-height: 32px;\">Follow the following Link for detailed analysis in allure,</span>" \
                                   "</font>" \
                                   "<div style=\"height: 10px; line-height: 10px; font-size: 10px;\">&nbsp;</div>" \
                                   "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"88%\" style=\"width: 88% !important; min-width: 88%; max-width: 88%;\">" \
                                      "<tr>" \
                                         "<td align=\"left\" valign=\"top\">" \
                                            "<table class=\"mob_btn\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"background: #27cbcc; border-radius: 4px;\">" \
                                               "<tr>" \
                                                  "<td align=\"center\" valign=\"top\">" \
                                                     "<a href=\"" + jenkins_url + "/allure/\" target=\"_blank\" style=\"display: block; border: 1px solid #27cbcc; border-radius: 4px; padding: 4px 8px; font-family: 'Source Sans Pro', Arial, Verdana, Tahoma, Geneva, sans-serif; color: #ffffff; font-size: 20px; line-height: 30px; text-decoration: none; white-space: nowrap; font-weight: 600;\">" \
                                                        "<font face=\"'Source Sans Pro', sans-serif\" color=\"#ffffff\" style=\"font-size: 20px; line-height: 30px; text-decoration: none; white-space: nowrap; font-weight: 600;\">" \
                                                           "<span style=\"font-family: 'Source Sans Pro', Arial, Verdana, Tahoma, Geneva, sans-serif; color: #ffffff; font-size: 20px; line-height: 30px; text-decoration: none; white-space: nowrap; font-weight: 600;\">Allure&nbsp;Report</span>" \
                                                        "</font>" \
                                                     "</a>" \
                                                  "</td>" \
                                               "</tr>" \
                                            "</table>" \
                                         "</td>" \
                                      "</tr>" \
                                   "</table>" \
                                   "<div style=\"height: 45px; line-height: 10px; font-size: 10px;\">&nbsp;</div>" \
                                   "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                      "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 16px; line-height: 32px;\">This email is auto-triggered from Jenkins Automation Job, for any queries please contact </span>" \
                                      "<a href=\"mailto:nareshnavinash@gmail.com\" style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 16px; line-height: 32px;\"> nareshnavinash@gmail.com</a>" \
                                      "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 16px; line-height: 32px;\"> or </span>" \
                                      "<a href=\"mailto:nareshsekar@zoho.com\" style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 16px; line-height: 32px;\">nareshsekar@zoho.com.</a>" \
                                   "</font>" \
                                   "<div style=\"height: 33px; line-height: 33px; font-size: 31px;\">&nbsp;</div>" \
                                   "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                      "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 16px; line-height: 32px;\">" + failed_testcases_string +"</span>" \
                                   "</font>" \
                                   "<div style=\"height: 1px; line-height: 1px; font-size: 31px;\">&nbsp;</div>" \
                                   "<font face=\"'Source Sans Pro', sans-serif\" color=\"#585858\" style=\"font-size: 24px; line-height: 32px;\">" \
                                      "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #585858; font-size: 16px; line-height: 32px;\">" + broken_testcases_string + "</span>" \
                                   "</font>" \
                                   "<div style=\"height: 33px; line-height: 33px; font-size: 31px;\">&nbsp;</div>" \
                                "</td>" \
                             "</tr>" \
                          "</table>" \
                          "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"90%\" style=\"width: 90% !important; min-width: 90%; max-width: 90%; border-width: 1px; border-style: solid; border-color: #e8e8e8; border-bottom: none; border-left: none; border-right: none;\">" \
                             "<tr>" \
                                "<td align=\"left\" valign=\"top\">" \
                                   "<div style=\"height: 15px; line-height: 15px; font-size: 13px;\">&nbsp;</div>" \
                                "</td>" \
                             "</tr>" \
                          "</table>" \
                          "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"88%\" style=\"width: 88% !important; min-width: 88%; max-width: 88%;\">" \
                             "<tr>" \
                                "<td class=\"mob_center\" align=\"left\" valign=\"top\">" \
                                   "<div style=\"height: 10px; line-height: 10px; font-size: 11px;\">&nbsp;</div>" \
                                   "<font face=\"'Source Sans Pro', sans-serif\" color=\"#000000\" style=\"font-size: 19px; line-height: 23px; font-weight: 600;\">" \
                                      "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #7f7f7f; font-size: 19px; line-height: 23px;\">Thanks,</span>" \
                                   "</font>" \
                                   "<div style=\"height: 1px; line-height: 1px; font-size: 1px;\">&nbsp;</div>" \
                                   "<font face=\"'Source Sans Pro', sans-serif\" color=\"#7f7f7f\" style=\"font-size: 19px; line-height: 23px;\">" \
                                      "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #000000; font-size: 19px; line-height: 23px; font-weight: 600;\">SDET Team.</span>" \
                                   "</font>" \
                                   "<div style=\"height: 25px; line-height: 20px; font-size: 15px;\">&nbsp;</div>" \
                                "</td>" \
                             "</tr>" \
                          "</table>" \
                          "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\" style=\"width: 100% !important; min-width: 100%; max-width: 100%; background: #f3f3f3;\">" \
                             "<tr>" \
                                "<td align=\"center\" valign=\"top\">" \
                                   "<div style=\"height: 34px; line-height: 34px; font-size: 32px;\">&nbsp;</div>" \
                                   "<table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"88%\" style=\"width: 88% !important; min-width: 88%; max-width: 88%;\">" \
                                      "<tr>" \
                                         "<td align=\"center\" valign=\"top\">" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#868686\" style=\"font-size: 17px; line-height: 20px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #868686; font-size: 17px; line-height: 20px;\">Copyright &copy; 2020 Naresh Sekar. All&nbsp;Rights&nbsp;Reserved. Confidential&nbsp;attachments!</span>" \
                                            "</font>" \
                                            "<div style=\"height: 2px; line-height: 2px; font-size: 32px;\">&nbsp;</div>" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#868686\" style=\"font-size: 17px; line-height: 20px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #868686; font-size: 17px; line-height: 20px;\">Beware Before Forwarding this e-mail!</span>" \
                                            "</font>" \
                                            "<div style=\"height: 3px; line-height: 3px; font-size: 1px;\">&nbsp;</div>" \
                                            "<font face=\"'Source Sans Pro', sans-serif\" color=\"#1a1a1a\" style=\"font-size: 17px; line-height: 20px;\">" \
                                               "<span style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #1a1a1a; font-size: 17px; line-height: 20px;\"><a href=\"mailto:nareshnavinash@gmail.com\" target=\"_blank\" style=\"font-family: 'Source Sans Pro', Arial, Tahoma, Geneva, sans-serif; color: #1a1a1a; font-size: 17px; line-height: 20px; text-decoration: none;\">nareshnavinash@gmail.com</a>" \
                                            "</font>" \
                                            "<div style=\"height: 35px; line-height: 35px; font-size: 33px;\">&nbsp;</div>" \
                                         "</td>" \
                                      "</tr>" \
                                   "</table>" \
                                "</td>" \
                             "</tr>" \
                          "</table>" \
                       "</td>" \
                       "<td class=\"mob_pad\" width=\"25\" style=\"width: 25px; max-width: 25px; min-width: 25px;\">&nbsp;</td>" \
                    "</tr>" \
                 "</table>" \
                 "<!--[if (gte mso 9)|(IE)]>" \
                 "</td></tr>" \
                 "</table><![endif]-->" \
              "</td>" \
           "</tr>" \
        "</table>" \
        "</body>" \
""
    message = Message(email_subject, to=to_email, html=html_body, attachments=attachments)
    gmail.send(message)
