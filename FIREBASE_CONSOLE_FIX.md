## 🚨 URGENT: Fix Firebase Email Template

### The Problem

You're currently getting Firebase's default email template:

```
Hello,
Follow this link to reset your project-370802731084 password for your shahriar12688@gmail.com account.
https://swift-26949.firebaseapp.com/__/auth/action?mode=resetPassword&oobCode=...
```

### The Solution

**You need to set the custom action URL in Firebase Console.**

## 🔧 EXACT STEPS TO FIX:

### 1. Open Firebase Console

Go to: https://console.firebase.google.com/project/swift-26949/authentication/settings

### 2. Configure Action URL

- Click on **"Advanced"** tab
- Find **"Action URL"** setting
- Change from: `https://swift-26949.firebaseapp.com/__/auth/action`
- Change to: `https://swift-26949.web.app`
- Click **"Save"**

### 3. Customize Email Template (Optional)

- Go to: https://console.firebase.google.com/project/swift-26949/authentication/emails
- Click **"Password reset"**
- Update:
  - Subject: `Reset Your ECommerce Admin Password 🔐`
  - Sender name: `ECommerce Admin`
  - Reply-to: `your-email@domain.com`
- Click **"Save"**

## 🎯 What Will Change

**BEFORE (Current):**

- Plain text email
- Generic Firebase branding
- Links to `swift-26949.firebaseapp.com/__/auth/action`

**AFTER (Fixed):**

- Beautiful HTML email template
- Your custom branding
- Links to `swift-26949.web.app/reset-password` (your custom page)

## ✅ Test After Configuration

1. Run your Flutter app
2. Go to forgot password
3. Enter: `shahriar12688@gmail.com`
4. Check email - should be beautiful!
5. Click link - should go to your custom reset page

## 🔍 Verification

Your custom pages are already deployed and working:

- ✅ Reset page: https://swift-26949.web.app/reset-password
- ✅ Email template: Already created
- ❌ Firebase Console: **Needs configuration** (this is what you need to do)

**Time needed: 2-3 minutes**

The key is changing the **Action URL** from the default Firebase URL to your custom domain.
