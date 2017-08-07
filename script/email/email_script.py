# coding: utf-8

import smtplib
import argparse
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText

def parse_args():
    """
    Parse script input arguments.
    Returns the parsed args, having validated that the input
    file can be read, and that there is a valid Username.
    """
    parser = get_parser()
    args = parser.parse_args()

    # artificially adding this to args, so that
    # it can be passed around easily
    # args.html = open(args.html_filename).read()

    # we have to have a valid Gmail account in order to access the SMTP service
    if args.username is None:
        args.username = "baladavidinha@gmail.com"
    print_args(args)
    return args


def get_parser():
    """ Return the parser used to interpret the script arguments."""
    usage = (
        "Script to send an HTML file as an HTML email, using Google's SMTP server."
        "\nExamples:"
        "\n1. Send the contents of test_file.html to fred"
        "\n$ send_html_email.py fred@example.com test_file.html"
        "\n"
        "\n2. Send the mail to both fred and bob"
        "\n$ send_html_email.py fred@example.com bob@example.com test_file.html"
        "\n"
        "\n3. Use fred123@gmail.com as the Gmail authenticating account"
        "\n$ send_html_email.py fred@example.com test_file.html -u fred123@gmail.com"
        "\n"
        "\n4. Override the default test mail subject line"
        "\n$ send_html_email.py fred@example.com test_file.html -t 'Test email'"
        "\n"
        "\n5. Turn on SMTP debugging"
        "\n$ send_html_email.py fred@example.com test_file.html -d"
    )
    epilog = "NB This script requires a Gmail account."

    parser = argparse.ArgumentParser(description=usage, epilog=epilog,
        # maintains raw formatting, instead of wrapping lines automatically
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # parser.add_argument('recipients', help='The recipient email addresses (space delimited)', nargs='+')
    # parser.add_argument('html_filename', help='The HTML file to use as the email body content')
    parser.add_argument('-s', '--sender',
        help='The sender email address (defaults to <do-not-reply@example.com>)',
        default='do-not-reply@example.com'
    )
    parser.add_argument('-u', '--username',
        help=('A valid Gmail user account (used to authenticate against Google\'s SMTP service). '
            'If this argument is not supplied, the user will be prompted to type it in.')
    )
    parser.add_argument('-t', '--title',
        help='The test email subject line (defaults to "Test email")',
        default="Vidinha de Balada - Relatório Mensal"
    )
    parser.add_argument('-p', '--plain',
        help=('The test email plain text content. This script is designed primarily for the '
            'testing of HTML emails, so this text is really just a placeholder, for completeness. '
            'The default is "This is a test email (plain text)."'),
        default="This is a test email (plain text)"
    )
    parser.add_argument('-d', '--debug', action='store_true',
        help=('Use this option to turn on DEBUG for the SMTP server interaction.')
    )
    return parser


def print_args(args):
    """Print out the input arguments."""
    # print 'Sending test email to: %s' % args.recipients
    print 'Sending test email from: %s' % args.sender
    print 'Using Gmail account: %s' % args.username


def create_message(args, data, nome, recipients):
    """ Create the email message container from the input args."""
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = args.title
    msg['From'] = args.sender

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(args.plain, 'plain')
    id_deputado = data.keys()[0]
    deputado = data[id_deputado]['deputado']
    total_gasto = data[id_deputado]['total_gasto']
    categoria = data[id_deputado]['categoria']
    gasto_categoria = data[id_deputado]['gasto_categoria']
    empresa = data[id_deputado]['empresa']
    maior_gasto = data[id_deputado]['maior_gasto']
    empresa_mais_gastos = data[id_deputado]['empresa_mais_gastos']
    sessoes= data[id_deputado]['sessoes']
    total_sessoes= data[id_deputado]['total_sessoes']


    # Create the body of the message.
    html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
 
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>A Simple Responsive HTML Email</title>
  <style type="text/css">
  body {{margin: 0; padding: 0; min-width: 100%!important;}}
  img {{height: auto;}}
  .content {{width: 100%; max-width: 600px;}}
  .header {{padding: 40px 30px 20px 30px;}}
  .innerpadding {{padding: 30px 30px 30px 30px;}}
  .borderbottom {{border-bottom: 1px solid #f2eeed;}}
  .subhead {{font-size: 15px; color: #61397B; font-family: sans-serif; letter-spacing: 10px;}}
  .h1, .h2, .bodycopy {{color: #61397B; font-family: sans-serif;}}
  .h1 {{font-size: 33px; line-height: 38px; font-weight: bold;}}
  .h2 {{padding: 0 0 15px 0; font-size: 24px; line-height: 28px; font-weight: bold;}}
  .bodycopy {{font-size: 16px; line-height: 22px;}}
  .button {{text-align: center; font-size: 18px; font-family: sans-serif; font-weight: bold; padding: 0 30px 0 30px;}}
  .button a {{color: #ffffff; text-decoration: none;}}
  .footer {{padding: 20px 30px 15px 30px;}}
  .footercopy {{font-family: sans-serif; font-size: 14px; color: #ffffff;}}
  .footercopy a {{color: #ffffff; text-decoration: underline;}}

  @media only screen and (max-width: 550px), screen and (max-device-width: 550px) {{
  body[yahoo] .hide {{display: none!important;}}
  body[yahoo] .buttonwrapper {{background-color: transparent!important;}}
  body[yahoo] .button {{padding: 0px!important;}}
  body[yahoo] .button a {{background-color: #e05443; padding: 15px 15px 13px!important;}}
  body[yahoo] .unsubscribe {{display: block; margin-top: 20px; padding: 10px 50px; background: #2f3942; border-radius: 5px; text-decoration: none!important; font-weight: bold;}}
  }}

  /*@media only screen and (min-device-width: 601px) {{
    .content {{width: 600px !important;}}
    .col425 {{width: 425px!important;}}
    .col380 {{width: 380px!important;}}
    }}*/

  </style>
</head>

<body yahoo bgcolor="#f6f8f1">
<table width="100%" bgcolor="#f6f8f1" border="0" cellpadding="0" cellspacing="0">
<tr>
  <td>
    <!--[if (gte mso 9)|(IE)]>
      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
    <![endif]-->     
    <table bgcolor="#ffffff" class="content" align="center" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td bgcolor="#ffffff" class="header">
          <table width="70" align="left" border="0" cellpadding="0" cellspacing="0">  
            <tr>
             
            </tr>
          </table>
          <!--[if (gte mso 9)|(IE)]>
            <table width="425" align="left" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td>
          <![endif]-->
          <table class="col425" align="left" border="0" cellpadding="0" cellspacing="0" style="width: 100%; max-width: 425px;">  
            <tr>
              <td height="50">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                  
                  </tr>
                  <tr>
                    <td class="h1" style="padding: 20px 0 0 0;">
                     Olá, {0}!
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td class="innerpadding borderbottom">
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td class="h2">
                Este é o relatório mensal do Deputado {1} 
              </td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td class="innerpadding borderbottom">
          <table width="115" align="left" border="0" cellpadding="0" cellspacing="0">  
            <tr>
              <td height="115" style="padding: 50px 20px 20px 0;">
                <img class="fix" src="cid:image3" width="115" height="115" border="0" alt="" />
              </td>
            </tr>
          </table>
     
          <table class="col380" align="center" border="0" cellpadding="0" cellspacing="0" style="width: 100%; max-width: 380px;">  
            <tr>
              <td>
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="bodycopy">
                      <br> Total de gastos no mês foi de: R${2} <br/></br>
                      <br>A categoria de maior gasto foi: {3}  <br/></br>
                      <br>Maior gasto foi R${4} na empresa: {5}  <br/></br>
                      <br>A empresa que mais gastou foi: {6} <br/></br>
                      <br>Compareceu a {8} sessões num total de {9} </br>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding: 20px 0 0 0;">
                      <table class="buttonwrapper" bgcolor="#463066" border="0" cellspacing="0" cellpadding="0">
                        <tr>
                          <td class="button" height="45">
                            <a href="http://vidinhadebalada.com/#!/perfil/{7}">Acesse o perfil do deputado!</a>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
          <!--[if (gte mso 9)|(IE)]>
                </td>
              </tr>
          </table>
          <![endif]-->
        </td>
      </tr>
      
        <td class="footer" bgcolor="#61397B">

          <table width="100%" border="0" cellspacing="0" cellpadding="0">
          <td width="37" style="text-align: center; padding: 0 10px 10px 10px;">
              <a ui-sref="home"><img src="cid:image2" height="60" width="95" class="footer-logo"></img></a>
           </td>
            <tr>

              <td align="center" class="footercopy">
                <span class="hide">Você está recebendo este email pois está inscrito no Vidinha de Balada. Para cancelar sua inscrição clique</span>                
                <a href="#" class="unsubscribe"><font color="#ffffff">aqui</font></a> 
              </td>
            </tr>
            <tr>

              <td align="center" style="padding: 20px 10px 0 0;">
                <table border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td width="37" style="text-align: center; padding: 0 10px 0 10px;">
                    
                    </td>
              
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
    </td>
  </tr>
</table>
</body>
</html>
  """.format(nome, deputado, total_gasto,
    categoria,
    gasto_categoria,
    empresa,
    empresa_mais_gastos, id_deputado, sessoes, total_sessoes)
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.

    fp = open('images/branca.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image2>')
    msg.attach(msgImage)

    fp = open('images/article1.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image3>')
    msg.attach(msgImage)

    msg.attach(part1)
    msg.attach(part2)
    return msg


def main():

    args = parse_args()

    data = {"74040" :
            {'deputado' : 'BENJAMIN MARANHÃO',
            "total_gasto" : "1.129.819,75",
            "categoria" : "Divulgação",
            "gasto_categoria" : "486.868,33",
            "empresa" : "GRÁFICA E EDITORA MANGUEIRA LTDA",
            "maior_gasto" : "193.930,00",
            "empresa_mais_gastos" : "GRÁFICA E EDITORA MANGUEIRA LTDA",
            "sessoes" : 3,
            "total_sessoes": 3
            }
    }

    emails = {"74040":
             [
             ["Helder Ronyer", "helderronyer@gmail.com"],
             ["Helder 2", "helder.alves@ccc.ufcg.edu.br"],
             ["Talita Lobo", "talitabac@gmail.com"]
             ]}
    # getpass() prompts the user for their password (so it never appears in plain text)
    password = getpass()
    for inscrito in emails["74040"]:
        recipients = inscrito[1]
        msg = create_message(args, data, inscrito[0], recipients)

        try:
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.set_debuglevel(args.debug)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(args.username, password)
            # sendmail function takes 3 arguments: sender's address, recipient's address
            # and message to send - here it is sent as one string.
            smtpserver.sendmail(args.sender, recipients, msg.as_string())
            print "Message sent to '%s'." % recipients
            smtpserver.quit()
        except smtplib.SMTPAuthenticationError as e:
            print "Unable to send message: %s" % e



if __name__ == "__main__":
    main()