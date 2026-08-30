import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class ScoreBoard extends StatelessWidget {
  final int score;
  final int elapsedSeconds;
  final int moves;
  final int matchedPairs;
  final int totalPairs;

  const ScoreBoard({
    super.key,
    required this.score,
    required this.elapsedSeconds,
    required this.moves,
    required this.matchedPairs,
    required this.totalPairs,
  });

  String _formatTime(int totalSeconds) {
    final minutes = totalSeconds ~/ 60;
    final seconds = totalSeconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: theme.cardTheme.color,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: theme.colorScheme.primary.withOpacity(0.2),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildStatChip(
            icon: Icons.star_rounded,
            label: 'Score',
            value: '$score',
            color: theme.colorScheme.primary,
            theme: theme,
          ),
          _buildStatChip(
            icon: Icons.timer_outlined,
            label: 'Time',
            value: _formatTime(elapsedSeconds),
            color: theme.textTheme.bodyLarge?.color ?? Colors.white,
            theme: theme,
          ),
          _buildStatChip(
            icon: Icons.touch_app_rounded,
            label: 'Moves',
            value: '$moves',
            color: theme.textTheme.bodyLarge?.color ?? Colors.white,
            theme: theme,
          ),
          _buildStatChip(
            icon: Icons.check_circle_outline,
            label: 'Pairs',
            value: '$matchedPairs/$totalPairs',
            color: Colors.greenAccent,
            theme: theme,
          ),
        ],
      ),
    );
  }

  Widget _buildStatChip({
    required IconData icon,
    required String label,
    required String value,
    required Color color,
    required ThemeData theme,
  }) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, color: color, size: 20),
        const SizedBox(height: 4),
        Text(
          value,
          style: GoogleFonts.orbitron(
            fontSize: 14,
            fontWeight: FontWeight.w700,
            color: color,
          ),
        ),
        Text(
          label,
          style: theme.textTheme.bodySmall?.copyWith(
            fontSize: 10,
            letterSpacing: 1,
          ),
        ),
      ],
    );
  }
}