# E-commerce Admin Panel with AR Try-On

A comprehensive Flutter ecommerce application with advanced AR (Augmented Reality) try-on functionality powered by Banuba SDK.

## 🌟 Features

### Core E-commerce Features

- **Product Management**: Complete product catalog with categories, brands, and detailed product information
- **Order Management**: Full order processing and tracking system
- **User Authentication**: Secure Firebase authentication
- **Payment Processing**: Stripe integration for secure payments
- **Admin Dashboard**: Comprehensive admin panel for managing the store

### 🎯 AR Try-On Features (NEW!)

- **Virtual Product Try-On**: Experience products virtually using AR technology
- **Multiple Effect Categories**: Glasses, jewelry, makeup, hair colors, and more
- **Real-time Camera Rendering**: Live camera feed with AR effects overlay
- **Screenshot Capture**: Save and share AR try-on experiences
- **Cross-platform Support**: Works on both Android and iOS devices

## 🚀 Getting Started

### Prerequisites

- Flutter 3.3.0 or higher
- Dart 3.0 or higher
- Android Studio / VS Code
- Xcode (for iOS development)
- **Banuba License Key** (required for AR functionality)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd ecommerce_admin
   ```

2. **Install dependencies**

   ```bash
   flutter pub get
   ```

3. **Configure AR Try-On**

   - Get your Banuba license key from [Banuba](https://www.banuba.com/)
   - Update the license key in `lib/services/banuba_ar_config.dart`

   ```dart
   static const String licenseKey = "YOUR_BANUBA_LICENSE_KEY";
   ```

4. **iOS Setup**

   ```bash
   cd ios
   pod install
   cd ..
   ```

5. **Run the application**
   ```bash
   flutter run
   ```

## 📱 AR Try-On Usage

### For Users

1. Navigate to any product detail screen
2. Look for the "Try On with Camera" button (for compatible products)
3. Tap the floating AR button (🎯) to access the AR demo
4. Grant camera permissions when prompted
5. Select different effects to try on
6. Capture screenshots of your AR experience

### For Developers

```dart
import 'package:ecommerce_admin_panel/services/banuba_ar_service.dart';

// Initialize AR service
final arService = BanubaARService.instance;
await arService.initializeBanubaSDK();

// Start AR session
await arService.startTryOn('glasses_classic');

// Capture screenshot
final screenshot = await arService.captureScreenshot();
```

## 🏗️ Project Structure

```
lib/
├── services/
│   ├── banuba_ar_service.dart       # Main AR service
│   └── banuba_ar_config.dart        # AR configuration
├── user_section/
│   ├── screens/ar_tryon/            # AR try-on screens
│   └── widgets/ar_tryon_widget.dart # AR widget components
├── admin_section/                   # Admin panel features
├── common/                          # Shared components
└── main.dart                        # App entry point

android/
├── app/src/main/kotlin/com/example/admin/
│   └── BanubaARPlugin.kt            # Android AR implementation

ios/
└── Runner/
    ├── BanubaARPlugin.h             # iOS AR interface
    └── BanubaARPlugin.m             # iOS AR implementation
```

## 🎨 AR Effects Configuration

Add custom AR effects by updating the configuration:

```dart
// lib/services/banuba_ar_config.dart
static const Map<String, EffectInfo> defaultEffects = {
  'custom_effect': EffectInfo(
    id: 'custom_effect',
    name: 'Custom Effect',
    category: categoryGlasses,
    description: 'Your custom AR effect',
    thumbnailUrl: 'assets/effects/thumbnails/custom.png',
    effectPath: 'effects/custom/effect.zip',
  ),
};
```

## 🧪 Testing

Run the integration test script:

```bash
./test_banuba_integration.sh
```

This will check:

- ✅ Required files and dependencies
- ✅ Platform configurations
- ✅ Permissions setup
- ✅ Code compilation

## 📚 Documentation

- **[Banuba AR Integration Guide](BANUBA_AR_INTEGRATION_GUIDE.md)** - Complete setup instructions
- **[API Documentation](docs/api.md)** - Detailed API reference
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute

## 🔧 Platform Requirements

### Android

- API Level 24+ (Android 7.0+)
- Camera2 API support
- OpenGL ES 3.0+

### iOS

- iOS 16.0+
- Metal framework support
- Camera permissions

## 🚨 Troubleshooting

### Common Issues

1. **Camera Permission Denied**

   - Check permissions in device settings
   - Verify manifest declarations

2. **AR Effects Not Loading**

   - Verify Banuba license key
   - Check effect file paths
   - Ensure proper SDK initialization

3. **Performance Issues**
   - Test on physical devices only
   - Close other camera-using apps
   - Check device specifications

### Debug Mode

Enable detailed logging in debug builds for troubleshooting.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for AR functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Banuba** for providing the AR SDK
- **Flutter Team** for the amazing framework
- **Firebase** for backend services
- **Stripe** for payment processing

## 📞 Support

For AR-related issues:

- Check the [Banuba Documentation](https://docs.banuba.com/)
- Review our [Integration Guide](BANUBA_AR_INTEGRATION_GUIDE.md)
- Open an issue in this repository

---

**Note**: AR Try-On requires a valid Banuba license and works best on physical devices with good lighting conditions.
