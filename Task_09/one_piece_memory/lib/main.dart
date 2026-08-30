import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'screens/home_screen.dart';
import 'services/storage_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Lock orientation to portrait for the game
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
  ]);

  // Initialize storage service before running the app
  await StorageService.instance.init();

  runApp(const OharaMemoryApp());
}

class OharaMemoryApp extends StatefulWidget {
  const OharaMemoryApp({super.key});

  @override
  State<OharaMemoryApp> createState() => _OharaMemoryAppState();
}

class _OharaMemoryAppState extends State<OharaMemoryApp> {
  // Theme mode is loaded from SharedPreferences
  ThemeMode _themeMode = ThemeMode.dark;

  @override
  void initState() {
    super.initState();
    _loadThemePreference();
  }

  Future<void> _loadThemePreference() async {
    final isDark = await StorageService.instance.getThemeMode();
    setState(() {
      _themeMode = isDark ? ThemeMode.dark : ThemeMode.light;
    });
  }

  void toggleTheme() async {
    final newIsDark = _themeMode == ThemeMode.light;
    await StorageService.instance.setThemeMode(newIsDark);
    setState(() {
      _themeMode = newIsDark ? ThemeMode.dark : ThemeMode.light;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ohara Memory',
      debugShowCheckedModeBanner: false,
      themeMode: _themeMode,
      theme: _buildLightTheme(),
      darkTheme: _buildDarkTheme(),
      home: HomeScreen(
        onToggleTheme: toggleTheme,
        isDarkMode: _themeMode == ThemeMode.dark,
      ),
    );
  }

  // Miruro-inspired dark theme
  ThemeData _buildDarkTheme() {
    const Color primaryAccent = Color(0xFFB5A8FF);
    const Color background = Color(0xFF0B0B0F);
    const Color surface = Color(0xFF151519);
    const Color card = Color(0xFF1A1A20);

    return ThemeData(
      brightness: Brightness.dark,
      primaryColor: primaryAccent,
      scaffoldBackgroundColor: background,
      colorScheme: const ColorScheme.dark(
        primary: primaryAccent,
        secondary: Color(0xFF685BB2),
        surface: surface,
        background: background,
      ),
      cardTheme: CardTheme(
        color: card,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: background,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: TextStyle(
          color: Colors.white,
          fontSize: 20,
          fontWeight: FontWeight.w700,
          letterSpacing: 1.2,
        ),
        iconTheme: IconThemeData(color: Colors.white),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryAccent,
          foregroundColor: Colors.black,
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
          textStyle: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w700,
            letterSpacing: 1.0,
          ),
        ),
      ),
      textTheme: const TextTheme(
        headlineLarge: TextStyle(
          color: Colors.white,
          fontSize: 32,
          fontWeight: FontWeight.w800,
          letterSpacing: 1.5,
        ),
        headlineMedium: TextStyle(
          color: Colors.white,
          fontSize: 22,
          fontWeight: FontWeight.w700,
        ),
        bodyLarge: TextStyle(color: Colors.white, fontSize: 16),
        bodyMedium: TextStyle(color: Color(0xFFA0A0A5), fontSize: 14),
      ),
      useMaterial3: true,
    );
  }

  // Clean light theme
  ThemeData _buildLightTheme() {
    const Color primaryAccent = Color(0xFF685BB2);
    const Color background = Color(0xFFF5F5F5);
    const Color surface = Color(0xFFFFFFFF);

    return ThemeData(
      brightness: Brightness.light,
      primaryColor: primaryAccent,
      scaffoldBackgroundColor: background,
      colorScheme: const ColorScheme.light(
        primary: primaryAccent,
        secondary: Color(0xFFB5A8FF),
        surface: surface,
        background: background,
      ),
      cardTheme: CardTheme(
        color: surface,
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: background,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: TextStyle(
          color: Color(0xFF0B0B0F),
          fontSize: 20,
          fontWeight: FontWeight.w700,
          letterSpacing: 1.2,
        ),
        iconTheme: IconThemeData(color: Color(0xFF0B0B0F)),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryAccent,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
          textStyle: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w700,
            letterSpacing: 1.0,
          ),
        ),
      ),
      textTheme: const TextTheme(
        headlineLarge: TextStyle(
          color: Color(0xFF0B0B0F),
          fontSize: 32,
          fontWeight: FontWeight.w800,
          letterSpacing: 1.5,
        ),
        headlineMedium: TextStyle(
          color: Color(0xFF0B0B0F),
          fontSize: 22,
          fontWeight: FontWeight.w700,
        ),
        bodyLarge: TextStyle(color: Color(0xFF0B0B0F), fontSize: 16),
        bodyMedium: TextStyle(color: Color(0xFF555555), fontSize: 14),
      ),
      useMaterial3: true,
    );
  }
}