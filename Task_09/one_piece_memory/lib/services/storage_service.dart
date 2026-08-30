import 'package:shared_preferences/shared_preferences.dart';

/// A singleton service that wraps SharedPreferences for persistent storage.
///
/// This service handles all local persistence needs for the app:
/// - Best score (high score across sessions)
/// - Theme mode preference (dark/light)
///
/// Must be initialized via [init] before any other method is called.
/// Typically initialized in main() before runApp().
class StorageService {
  // Singleton instance
  static final StorageService instance = StorageService._();
  StorageService._();

  // SharedPreferences instance (set after init)
  late SharedPreferences _prefs;

  // Storage keys (centralized to avoid typos)
  static const String _keyBestScore = 'best_score';
  static const String _keyThemeMode = 'theme_mode_dark';

  /// Initialize the service. Must be called once at app startup.
  ///
  /// Example:
  /// ```dart
  /// await StorageService.instance.init();
  /// ```
  Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
  }

  // ==========================================
  // BEST SCORE
  // ==========================================

  /// Get the user's best score. Returns 0 if no score has been saved.
  Future<int> getBestScore() async {
    return _prefs.getInt(_keyBestScore) ?? 0;
  }

  /// Save a new best score.
  Future<void> setBestScore(int score) async {
    await _prefs.setInt(_keyBestScore, score);
  }

  /// Reset the best score to 0.
  Future<void> resetBestScore() async {
    await _prefs.setInt(_keyBestScore, 0);
  }

  // ==========================================
  // THEME MODE
  // ==========================================

  /// Get the saved theme preference.
  /// Returns `true` if dark mode should be used, `false` for light mode.
  /// Defaults to `true` (dark mode) if no preference has been saved.
  Future<bool> getThemeMode() async {
    return _prefs.getBool(_keyThemeMode) ?? true;
  }

  /// Save the theme preference.
  ///
  /// [isDark] - `true` for dark mode, `false` for light mode.
  Future<void> setThemeMode(bool isDark) async {
    await _prefs.setBool(_keyThemeMode, isDark);
  }
}