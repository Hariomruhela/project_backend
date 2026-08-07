from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime
import smtplib
import os

load_dotenv()

router = APIRouter()


class ContactForm(BaseModel):
    name: str
    agency: str
    email: EmailStr
    interest: str
    details: str


def admin_email_template(data: ContactForm):
    current_datetime = datetime.now().strftime("%d %B %Y ")

    return f"""
    <html>
    <body style="margin:0;padding:0;background:#f4f7fb;font-family:Arial,sans-serif;">

    <table width="100%" cellpadding="20" cellspacing="0" style="background:#f4f7fb;">
      <tr>
        <td align="center">

          <table width="650" cellpadding="0" cellspacing="0"
            style="
              background:white;
              border-radius:12px;
              overflow:hidden;
              border:1px solid #e5e7eb;
            ">

            <!-- Header -->
            <tr>
              <td
                style="
                  padding:35px;
                  background:#9333ea;
                  text-align:center;
                  color:white;
                "
              >
                <h1 style="margin:0;">New Partnership Inquiry</h1>
                <p style="margin-top:10px;">
                  Techquitoes Partnership Portal
                </p>
              </td>
            </tr>

            <!-- Body -->
            <tr>
              <td style="padding:30px;">

                <p style="color:#475569;">
                  A new partnership request has been submitted through the Techquitoes website.
                </p>

                <table width="100%" cellpadding="12" cellspacing="0"
                    style="
                      border:1px solid #e5e7eb;
                      border-radius:8px;
                    ">

                  <tr>
                    <td width="35%" style="font-weight:bold;">Full Name</td>
                    <td>{data.name}</td>
                  </tr>

                  <tr>
                    <td style="font-weight:bold;">Agency Name</td>
                    <td>{data.agency}</td>
                  </tr>

                  <tr>
                    <td style="font-weight:bold;">Business Email</td>
                    <td style="color:#9333ea;">
                      {data.email}
                    </td>
                  </tr>

                  <tr>
                    <td style="font-weight:bold;">Partnership Scope</td>
                    <td>{data.interest}</td>
                  </tr>

                  <tr>
                    <td style="font-weight:bold;vertical-align:top;">
                      Technical Requirements
                    </td>

                    <td>{data.details}</td>
                  </tr>

                  <tr>
                    <td style="font-weight:bold;">Submitted On</td>
                    <td>{current_datetime}</td>
                  </tr>

                </table>

              </td>
            </tr>

            <!-- Footer -->
            <tr>
              <td
                style="
                  background:#f8fafc;
                  padding:20px;
                  text-align:center;
                  color:#64748b;
                  font-size:12px;
                "
              >
                This email was automatically generated from the
                Techquitoes website.

                <br><br>

                 <a
      href="https://techquitoes.com"
      style="color:#9333ea;text-decoration:none;"
    >
      https://techquitoes.com
    </a>

    &nbsp;|&nbsp;

    <a
      href="mailto:hello@techquitoes.com"
      style="color:#9333ea;text-decoration:none;"
    >
      hello@techquitoes.com
    </a>
              </td>
            </tr>

          </table>

        </td>
      </tr>
    </table>

    </body>
    </html>
    """


def customer_email_template(name):
    return f"""
    <html>
    <body style="margin:0;padding:0;background:#f4f7fb;font-family:Arial,sans-serif;">

    <table width="100%" cellpadding="20" cellspacing="0" style="background:#f4f7fb;">
      <tr>
        <td align="center">

          <table width="650" cellpadding="0" cellspacing="0"
            style="
              background:white;
              border-radius:12px;
              overflow:hidden;
              border:1px solid #e5e7eb;
            ">

            <tr>
              <td
                style="
                  background:#9333ea;
                  padding:35px;
                  color:white;
                  text-align:center;
                "
              >
                <h1>Thank You For Contacting Techquitoes</h1>
              </td>
            </tr>

            <tr>
              <td style="padding:35px;color:#334155;line-height:1.8;">

                <p>Hi {name},</p>

                <p>
                  Thank you for reaching out to Techquitoes.
                  We have successfully received your inquiry.
                </p>

                <p>
                  Our team will review your request and get back
                  to you within <strong>24 business hours</strong>.
                </p>

                <div style="
                    margin-top:25px;
                    padding:20px;
                    background:#f8fafc;
                    border:1px solid #e5e7eb;
                    border-radius:10px;
                ">
                    <strong>What happens next?</strong>

                    <p>✔ Requirement review</p>
                    <p>✔ Technical feasibility analysis</p>
                    <p>✔ Partnership discussion call</p>
                    <p>✔ Proposal planning</p>
                </div>

                <p style="margin-top:30px;">
                  Best Regards,<br>
                  <strong>Techquitoes Team</strong>
                </p>

              </td>
            </tr>

            <tr>
              <td
                style="
                  background:#f8fafc;
                  padding:20px;
                  text-align:center;
                  color:#64748b;
                  font-size:12px;
                "
              >
                © 2026 Techquitoes Solutions
              </td>
            </tr>

          </table>

        </td>
      </tr>
    </table>

    </body>
    </html>
    """


@router.post("/contact")
async def send_contact_email(data: ContactForm):

    sender_email = os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")
    receiver_email = os.getenv("MAIL_TO")

    try:
        # -----------------------------
        # Send Email To Admin
        # -----------------------------
        admin_message = MIMEMultipart("alternative")
        admin_message["Subject"] = "New Partnership Inquiry"
        admin_message["From"] = sender_email
        admin_message["To"] = receiver_email

        admin_message.attach(
            MIMEText(
                admin_email_template(data),
                "html"
            )
        )

        # -----------------------------
        # Auto Reply To Customer
        # -----------------------------
        customer_message = MIMEMultipart("alternative")
        customer_message["Subject"] = "Thank You For Contacting Techquitoes"
        customer_message["From"] = sender_email
        customer_message["To"] = data.email

        customer_message.attach(
            MIMEText(
                customer_email_template(data.name),
                "html"
            )
        )

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()

            server.login(
                sender_email,
                sender_password
            )

            server.sendmail(
                sender_email,
                receiver_email,
                admin_message.as_string()
            )

            server.sendmail(
                sender_email,
                data.email,
                customer_message.as_string()
            )

        return {
            "success": True,
            "message": "Email sent successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )