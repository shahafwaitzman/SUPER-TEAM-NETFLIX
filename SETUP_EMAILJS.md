# EmailJS Configuration Guide

## Current Setup
- **Public Key:** nhwKyEa3uJ8JjmxXQ  
- **Service ID:** service_etqui87
- **Template ID:** template_6bo4ai9

## Template Parameters
The EmailJS template MUST accept these parameters:
- `to_email` - Recipient email address
- `tab_name` - TAB member name
- `user_name` - New user name
- `user_email` - New user email  
- `approve_url` - Approval link

## Email Template Content
Should contain:
- Greeting with user name
- "Click here to approve" button linking to `approve_url`
- TAB member name (from `tab_name`)

## Setup Steps

### 1. Verify EmailJS Account
- Go to https://www.emailjs.com/
- Log in with your account
- Check Email Services → Verify SMTP is enabled

### 2. Check Email Service
- Go to Email Services
- Verify service_etqui87 exists
- Enable if disabled
- Test send to verify it works

### 3. Check Email Template
- Go to Email Templates
- Find or create template_6bo4ai9
- **CRITICAL:** Ensure template accepts:
  - `to_email` - "Send to" address
  - `tab_name` - For "{{tab_name}}"
  - `user_name` - For "{{user_name}}"
  - `user_email` - For "{{user_email}}"
  - `approve_url` - For clickable link

### 4. Test Email Sending
```javascript
// Open browser console and run:
emailjs.init('nhwKyEa3uJ8JjmxXQ');
emailjs.send('service_etqui87', 'template_6bo4ai9', {
  to_email: 'your-email@gmail.com',
  tab_name: 'Test TAB',
  user_name: 'Test User',
  user_email: 'test@example.com',
  approve_url: 'https://example.com/approve?key=123'
}).then(function(status) {
  console.log('SUCCESS - Email sent!', status);
}, function(error) {
  console.log('FAILED - Check console for details:', error);
});
```

### 5. Verify Email Received
- Check spam/promotions folder
- Check that `to_email` address received the message
- Verify approve link is clickable

## If Email Still Doesn't Work

### Check Browser Console
1. Open DevTools (F12)
2. Click Login with test data
3. Check Console tab for error messages
4. Look for "Email sent successfully" message
5. If error, it will be shown there

### Common Issues
- **"API key not found"** → Public key is wrong
- **"Service not found"** → Service ID is wrong
- **"Template not found"** → Template ID is wrong
- **"Missing template parameters"** → Template doesn't have all required fields

## Backup: Manual Email Sending
If EmailJS fails, TAB members can be notified manually:
1. User registers → Get Firebase user key
2. Share approval link: `https://shahafwaitzman.github.io/SUPER-TEAM-NETFLIX/approve.html?key={userKey}`
3. Send link to TAB member via Slack/WhatsApp/Email
4. They click link to approve user

