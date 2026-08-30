import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/storage_service.dart';

class SettingsScreen extends StatefulWidget {
  final bool isDarkMode;
  final VoidCallback onToggleTheme;
  final VoidCallback onBestScoreReset;

  const SettingsScreen({
    super.key,
    required this.isDarkMode,
    required this.onToggleTheme,
    required this.onBestScoreReset,
  });

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  int _bestScore = 0;

  @override
  void initState() {
    super.initState();
    _loadBestScore();
  }

  Future<void> _loadBestScore() async {
    final score = await StorageService.instance.getBestScore();
    if (mounted) {
      setState(() => _bestScore = score);
    }
  }

  Future<void> _confirmResetScore() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: Theme.of(context).cardTheme.color,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Text(
          'Reset Best Score?',
          style: GoogleFonts.orbitron(
            fontSize: 18,
            fontWeight: FontWeight.w700,
            color: Theme.of(context).colorScheme.primary,
          ),
        ),
        content: const Text(
          'This action cannot be undone. Your best score will be set to 0.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(true),
            style: TextButton.styleFrom(
              foregroundColor: Colors.redAccent,
            ),
            child: const Text('Reset'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      await StorageService.instance.setBestScore(0);
      setState(() => _bestScore = 0);
      
      // Notify HomeScreen to refresh its best score display
      widget.onBestScoreReset();
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: const Text('Best score reset successfully!'),
            backgroundColor: Theme.of(context).colorScheme.primary,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'SETTINGS',
          style: GoogleFonts.orbitron(
            fontSize: 16,
            fontWeight: FontWeight.w700,
            letterSpacing: 2,
          ),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Appearance Section
          _buildSectionHeader('APPEARANCE', theme),
          const SizedBox(height: 12),
          _buildSettingsCard(
            icon: Icons.dark_mode_rounded,
            title: 'Dark Mode',
            subtitle: 'Switch between light and dark themes',
            trailing: Switch.adaptive(
              value: widget.isDarkMode,
              onChanged: (_) => widget.onToggleTheme(),
              activeColor: theme.colorScheme.primary,
            ),
            theme: theme,
          ),
          
          const SizedBox(height: 24),

          // Game Data Section
          _buildSectionHeader('GAME DATA', theme),
          const SizedBox(height: 12),
          _buildSettingsCard(
            icon: Icons.emoji_events_rounded,
            title: 'Best Score',
            subtitle: 'Your highest achieved score',
            trailing: Text(
              '$_bestScore',
              style: GoogleFonts.orbitron(
                fontSize: 24,
                fontWeight: FontWeight.w800,
                color: theme.colorScheme.primary,
              ),
            ),
            theme: theme,
          ),
          const SizedBox(height: 12),
          _buildSettingsCard(
            icon: Icons.delete_forever_rounded,
            title: 'Reset Best Score',
            subtitle: 'Clear your highest score record',
            trailing: IconButton(
              icon: const Icon(Icons.refresh_rounded, color: Colors.redAccent),
              onPressed: _confirmResetScore,
              tooltip: 'Reset Score',
            ),
            theme: theme,
          ),
          
          const SizedBox(height: 40),
          
          // App Info
          Center(
            child: Column(
              children: [
                Text(
                  'OHARA MEMORY MATCHER',
                  style: GoogleFonts.orbitron(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    color: theme.textTheme.bodyMedium?.color,
                    letterSpacing: 2,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  'Version 1.0.0',
                  style: TextStyle(
                    color: theme.textTheme.bodyMedium?.color?.withOpacity(0.5),
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title, ThemeData theme) {
    return Padding(
      padding: const EdgeInsets.only(left: 8),
      child: Text(
        title,
        style: GoogleFonts.orbitron(
          fontSize: 12,
          fontWeight: FontWeight.w700,
          color: theme.colorScheme.primary,
          letterSpacing: 2,
        ),
      ),
    );
  }

  Widget _buildSettingsCard({
    required IconData icon,
    required String title,
    required String subtitle,
    required Widget trailing,
    required ThemeData theme,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: theme.cardTheme.color,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: theme.colorScheme.primary.withOpacity(0.1),
        ),
      ),
      child: Row(
        children: [
          Icon(icon, color: theme.colorScheme.primary, size: 28),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  subtitle,
                  style: theme.textTheme.bodyMedium?.copyWith(fontSize: 12),
                ),
              ],
            ),
          ),
          trailing,
        ],
      ),
    );
  }
}