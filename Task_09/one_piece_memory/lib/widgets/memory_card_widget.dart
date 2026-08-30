import 'package:flutter/material.dart';
import '../models/memory_card.dart';

class MemoryCardWidget extends StatelessWidget {
  final MemoryCard card;
  final VoidCallback onTap;

  const MemoryCardWidget({
    super.key,
    required this.card,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isRevealed = card.isFlipped || card.isMatched;

    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: card.isMatched
                ? theme.colorScheme.primary.withOpacity(0.6)
                : theme.colorScheme.primary.withOpacity(0.1),
            width: card.isMatched ? 2 : 1,
          ),
          boxShadow: card.isMatched
              ? [
                  BoxShadow(
                    color: theme.colorScheme.primary.withOpacity(0.3),
                    blurRadius: 12,
                    spreadRadius: 2,
                  ),
                ]
              : [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.2),
                    blurRadius: 4,
                    offset: const Offset(0, 2),
                  ),
                ],
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(12),
          child: AnimatedSwitcher(
            duration: const Duration(milliseconds: 300),
            transitionBuilder: (Widget child, Animation<double> animation) {
              return FadeTransition(
                opacity: animation,
                child: child,
              );
            },
            child: isRevealed
                ? _buildCardFront(theme)
                : _buildCardBack(theme),
          ),
        ),
      ),
    );
  }

  Widget _buildCardBack(ThemeData theme) {
    return Container(
      key: const ValueKey('back'),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            theme.colorScheme.primary.withOpacity(0.3),
            theme.colorScheme.secondary.withOpacity(0.2),
          ],
        ),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.sailing,
              size: 32,
              color: theme.colorScheme.primary.withOpacity(0.6),
            ),
            const SizedBox(height: 4),
            Text(
              'OHARA',
              style: TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.w700,
                color: theme.colorScheme.primary.withOpacity(0.5),
                letterSpacing: 2,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCardFront(ThemeData theme) {
    return Container(
      key: const ValueKey('front'),
      decoration: BoxDecoration(
        color: theme.cardTheme.color,
      ),
      child: Stack(
        fit: StackFit.expand,
        children: [
          // Character image
          Image.asset(
            card.imagePath,
            fit: BoxFit.cover,
            errorBuilder: (context, error, stackTrace) {
              return Container(
                color: theme.colorScheme.surface,
                child: Center(
                  child: Icon(
                    Icons.image_not_supported,
                    size: 40,
                    color: theme.textTheme.bodyMedium?.color,
                  ),
                ),
              );
            },
          ),
          
          // Gradient overlay at bottom for text readability
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: Container(
              height: 40,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Colors.transparent,
                    Colors.black.withOpacity(0.7),
                  ],
                ),
              ),
            ),
          ),
          
          // Character name
          Positioned(
            bottom: 6,
            left: 6,
            right: 6,
            child: Text(
              card.characterName,
              style: const TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.w700,
                color: Colors.white,
                letterSpacing: 0.5,
              ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              textAlign: TextAlign.center,
            ),
          ),
          
          // Matched indicator
          if (card.isMatched)
            Positioned(
              top: 6,
              right: 6,
              child: Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  color: theme.colorScheme.primary,
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.check,
                  size: 14,
                  color: Colors.black,
                ),
              ),
            ),
        ],
      ),
    );
  }
}