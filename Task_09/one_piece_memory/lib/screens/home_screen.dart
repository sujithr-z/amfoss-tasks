import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/storage_service.dart';
import 'game_screen.dart';
import 'settings_screen.dart';

class HomeScreen extends StatefulWidget {
  final VoidCallback onToggleTheme;
  final bool isDarkMode;

  const HomeScreen({
    super.key,
    required this.onToggleTheme,
    required this.isDarkMode,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _bestScore = 0;

  @override
  void initState() {
    super.initState();
    _loadBestScore();
  }

  Future<void> _loadBestScore() async {
    final score = await StorageService.instance.getBestScore();
    setState(() {
      _bestScore = score;
    });
  }

  void _navigateToGame() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => GameScreen(
          onGameComplete: (score) async {
            final currentBest = await StorageService.instance.getBestScore();
            if (score > currentBest) {
              await StorageService.instance.setBestScore(score);
              _loadBestScore();
            }
          },
        ),
      ),
    );
  }

  void _navigateToSettings() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => SettingsScreen(
          isDarkMode: widget.isDarkMode,
          onToggleTheme: widget.onToggleTheme,
          onBestScoreReset: _loadBestScore,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 32),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Logo/Title
                Icon(
                  Icons.sailing,
                  size: 80,
                  color: theme.colorScheme.primary,
                ),
                const SizedBox(height: 24),
                Text(
                  'OHARA',
                  style: GoogleFonts.orbitron(
                    fontSize: 48,
                    fontWeight: FontWeight.w800,
                    color: theme.colorScheme.primary,
                    letterSpacing: 4,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  'MEMORY MATCHER',
                  style: GoogleFonts.orbitron(
                    fontSize: 20,
                    fontWeight: FontWeight.w500,
                    color: theme.textTheme.bodyMedium?.color,
                    letterSpacing: 3,
                  ),
                ),
                const SizedBox(height: 48),

                // Best Score Card
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 40,
                    vertical: 24,
                  ),
                  decoration: BoxDecoration(
                    color: theme.cardTheme.color,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(
                      color: theme.colorScheme.primary.withOpacity(0.2),
                      width: 2,
                    ),
                  ),
                  child: Column(
                    children: [
                      Text(
                        'BEST SCORE',
                        style: GoogleFonts.orbitron(
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          color: theme.textTheme.bodyMedium?.color,
                          letterSpacing: 2,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        '$_bestScore',
                        style: GoogleFonts.orbitron(
                          fontSize: 48,
                          fontWeight: FontWeight.w800,
                          color: theme.colorScheme.primary,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 48),

                // Play Button
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _navigateToGame,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 18),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.play_arrow, size: 28),
                        const SizedBox(width: 12),
                        Text(
                          'SET SAIL',
                          style: GoogleFonts.orbitron(
                            fontSize: 18,
                            fontWeight: FontWeight.w700,
                            letterSpacing: 2,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // Settings Button
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton(
                    onPressed: _navigateToSettings,
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 18),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      side: BorderSide(
                        color: theme.colorScheme.primary.withOpacity(0.5),
                        width: 2,
                      ),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.settings,
                          size: 24,
                          color: theme.colorScheme.primary,
                        ),
                        const SizedBox(width: 12),
                        Text(
                          'SETTINGS',
                          style: GoogleFonts.orbitron(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                            color: theme.colorScheme.primary,
                            letterSpacing: 2,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}