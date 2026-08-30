import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class GameTimer extends StatelessWidget {
  final int elapsedSeconds;
  final bool isPaused;
  final Color? accentColor;

  const GameTimer({
    super.key,
    required this.elapsedSeconds,
    this.isPaused = false,
    this.accentColor,
  });

  String _formatTime(int totalSeconds) {
    final minutes = totalSeconds ~/ 60;
    final seconds = totalSeconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
  }

  Color _getTimerColor(ThemeData theme) {
    if (accentColor != null) return accentColor!;

    // Color shifts based on elapsed time for visual feedback
    if (elapsedSeconds < 60) {
      return theme.colorScheme.primary; // Purple accent for first minute
    } else if (elapsedSeconds < 180) {
      return Colors.orangeAccent; // Orange for 1-3 minutes
    } else {
      return Colors.redAccent; // Red after 3 minutes (urgency)
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final timerColor = _getTimerColor(theme);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        color: theme.cardTheme.color,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: timerColor.withOpacity(0.3),
          width: 1.5,
        ),
        boxShadow: [
          BoxShadow(
            color: timerColor.withOpacity(0.1),
            blurRadius: 8,
            spreadRadius: 1,
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Animated timer icon
          AnimatedContainer(
            duration: const Duration(milliseconds: 500),
            curve: Curves.easeInOut,
            child: Icon(
              isPaused ? Icons.pause_circle_outline : Icons.timer_outlined,
              color: timerColor,
              size: 22,
            ),
          ),
          const SizedBox(width: 10),
          // Time display
          Text(
            _formatTime(elapsedSeconds),
            style: GoogleFonts.orbitron(
              fontSize: 20,
              fontWeight: FontWeight.w700,
              color: timerColor,
              letterSpacing: 1.5,
            ),
          ),
          // Pause indicator
          if (isPaused) ...[
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
              decoration: BoxDecoration(
                color: timerColor.withOpacity(0.2),
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(
                'PAUSED',
                style: GoogleFonts.orbitron(
                  fontSize: 9,
                  fontWeight: FontWeight.w700,
                  color: timerColor,
                  letterSpacing: 1,
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}