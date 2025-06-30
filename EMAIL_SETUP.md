# Email Setup Instructions

## Quick Setup for Mohit Maurya (msm606248@gmail.com)

To enable email functionality for your contact form, follow these steps:

### 1. Gmail App Password Setup

1. **Enable 2-Factor Authentication** on your Gmail account (msm606248@gmail.com)
2. **Generate an App Password**:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Click on "2-Step Verification"
   - Scroll down to "App passwords"
   - Select "Mail" and generate a password
   - Copy the 16-character password (something like: `abcd efgh ijkl mnop`)

3. **Add your App Password**:
   - Open `portfolio_site/local_settings.py`
   - Replace the empty string in `EMAIL_HOST_PASSWORD = ''` with your App Password
   - Example: `EMAIL_HOST_PASSWORD = 'abcd efgh ijkl mnop'`

### 2. What Happens When Someone Contacts You

✅ **Admin Notification Email (to msm606248@gmail.com):**
- Beautiful HTML email with contact details
- Subject: "🔔 New Contact: [Their Subject]"
- Contains: Name, Email, Subject, Message, Timestamp
- Clear formatting for easy reading

✅ **User Confirmation Email (from msm606248@gmail.com):**
- Professional HTML confirmation email
- Subject: "✨ Thank you for contacting me - Mohit Maurya"
- Beautiful design with your branding
- Includes response time expectations (24-48 hours)
- Your contact information and social links

### 3. Test Your Setup

```bash
# Test email configuration
python manage.py test_email --to msm606248@gmail.com
```

### 4. Development Mode

If you just want to test without sending real emails:

1. No setup needed - emails will be printed to the console
2. Submit the contact form and check the terminal output

### Features

Once configured, the contact form will:
- ✅ Save messages to the database (viewable in admin panel)
- ✅ Send you an email notification with the message details
- ✅ Send a confirmation email to the person who contacted you
- ✅ Show success/error messages to the user

### Admin Panel

- View all contact messages at: http://127.0.0.1:8080/admin/
- Mark messages as read/unread
- Filter by date and read status
- Search through messages

### Troubleshooting

1. **Gmail Issues**: Make sure you're using an App Password, not your regular password
2. **Connection Issues**: Check if your firewall allows SMTP connections
3. **Authentication Issues**: Verify your email and password are correct
4. **Testing**: Use console backend for development: `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
