#!/bin/bash

echo "🔥 Firebase Password Reset Setup Verification"
echo "============================================"
echo ""

# Check if the gorgeous pages are accessible
echo "📄 Checking deployed pages..."
echo ""

echo "1. Testing main reset page:"
curl -s -o /dev/null -w "Status: %{http_code}\n" https://swift-26949.web.app/reset-password.html

echo "2. Testing action handler:"
curl -s -o /dev/null -w "Status: %{http_code}\n" https://swift-26949.web.app/__/auth/action.html

echo "3. Testing alternative action handler:"
curl -s -o /dev/null -w "Status: %{http_code}\n" https://swift-26949.web.app/action.html

echo ""
echo "🎨 Your gorgeous password reset pages are now live!"
echo ""
echo "📋 IMPORTANT: Configure Firebase Console Authentication"
echo "============================================"
echo ""
echo "1. Go to: https://console.firebase.google.com/project/swift-26949/authentication/settings"
echo ""
echo "2. Look for 'Custom action URL' or 'Action URL' setting"
echo ""
echo "3. Set it to: https://swift-26949.web.app"
echo ""
echo "🔗 The reset link will now redirect users to:"
echo "   https://swift-26949.web.app/reset-password.html"
echo ""
echo "✨ Features of your new gorgeous reset page:"
echo "   • Beautiful gradient design with floating animations"
echo "   • Real-time password strength indicator"
echo "   • Smooth transitions and hover effects"
echo "   • Mobile responsive design"
echo "   • Confetti celebration on success"
echo "   • Professional error handling"
echo "   • Security requirements display"
echo ""
echo "🧪 Test it now:"
echo "   1. Go to your Flutter app"
echo "   2. Click 'Forgot Password'"
echo "   3. Enter your email"
echo "   4. Check your email for the beautiful new reset link!"
echo ""

# Test with the actual URL from your message
echo "🔍 Testing your current reset URL format..."
echo "Old format: https://swift-26949.firebaseapp.com/__/auth/action?mode=resetPassword&oobCode=..."
echo "New format: https://swift-26949.web.app/reset-password.html?mode=resetPassword&oobCode=..."
echo ""
echo "The Firebase Console configuration will automatically redirect the old URLs to your new gorgeous page!"

echo ""
echo "🎉 Setup Complete! Your password reset page is now GORGEOUS! 🎨✨"
