// Example: How to configure password reset in your Flutter app
import 'package:firebase_auth/firebase_auth.dart';

Future<void> sendPasswordResetEmail(String email) async {
  try {
    // Configure action code settings
    ActionCodeSettings actionCodeSettings = ActionCodeSettings(
      // This URL will be used in the password reset email
      url: 'https://swift-26949.web.app/reset-password',
      // This must be true for email link authentication
      handleCodeInApp: true,
      // Your iOS bundle ID (if you have an iOS app)
      iOSBundleId: 'com.example.ecommerce_admin',
      // Your Android package name (if you have an Android app)
      androidPackageName: 'com.example.ecommerce_admin',
      // Whether to install the app if not already installed (Android)
      androidInstallApp: true,
      // Minimum version of the app (Android)
      androidMinimumVersion: '12',
    );

    await FirebaseAuth.instance.sendPasswordResetEmail(
      email: email,
      actionCodeSettings: actionCodeSettings,
    );

    print('Password reset email sent successfully');
  } catch (e) {
    print('Error sending password reset email: $e');
  }
}

// Alternative simpler approach without custom action settings
Future<void> sendSimplePasswordResetEmail(String email) async {
  try {
    await FirebaseAuth.instance.sendPasswordResetEmail(email: email);
    print('Password reset email sent successfully');
  } catch (e) {
    print('Error sending password reset email: $e');
  }
}
