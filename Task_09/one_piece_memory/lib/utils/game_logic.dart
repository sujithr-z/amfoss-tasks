import '../models/memory_card.dart';
import 'card_data.dart';

/// Pure game logic functions for the memory matching game.
///
/// This class contains no Flutter dependencies — only pure functions
/// that operate on data structures. This makes the game rules
/// testable, reusable, and independent of the UI layer.
///
/// The [GameScreen] widget calls these functions to:
/// - Generate and shuffle the card deck
/// - Evaluate matches
/// - Calculate scores
/// - Determine win conditions
class GameLogic {
  /// Default starting score for a new game.
  static const int initialScore = 1000;

  /// Points awarded for each correct match.
  static const int matchReward = 100;

  /// Points deducted for each incorrect match attempt.
  static const int mismatchPenalty = 20;

  /// Default number of pairs for a standard 4x4 grid game.
  static const int defaultPairs = 8;

  /// Generates a shuffled deck of memory cards.
  ///
  /// Takes the first [pairCount] characters from [CardData.characters],
  /// duplicates each to form a pair (sharing the same [pairId]),
  /// and shuffles the entire deck.
  ///
  /// Returns a list of [MemoryCard] instances ready for gameplay.
  ///
  /// Example:
  /// ```dart
  /// final deck = GameLogic.generateDeck(pairCount: 8);
  /// // Returns 16 cards (8 pairs), shuffled randomly
  /// ```
  static List<MemoryCard> generateDeck({int pairCount = defaultPairs}) {
    final characters = CardData.characters.take(pairCount).toList();
    final List<MemoryCard> deck = [];
    int idCounter = 0;

    for (int i = 0; i < characters.length; i++) {
      final char = characters[i];

      // Create two cards with the same pairId
      deck.add(MemoryCard(
        id: idCounter++,
        pairId: i,
        imagePath: char.imagePath,
        characterName: char.name,
      ));
      deck.add(MemoryCard(
        id: idCounter++,
        pairId: i,
        imagePath: char.imagePath,
        characterName: char.name,
      ));
    }

    // Shuffle the deck
    deck.shuffle();

    return deck;
  }

  /// Checks if two cards form a valid match.
  ///
  /// Two cards match if they have the same [pairId].
  ///
  /// Returns `true` if the cards match, `false` otherwise.
  static bool isMatch(MemoryCard card1, MemoryCard card2) {
    return card1.pairId == card2.pairId;
  }

  /// Calculates the score change for a correct match.
  ///
  /// Returns the points to add to the current score.
  static int calculateMatchReward() {
    return matchReward;
  }

  /// Calculates the score change for an incorrect match.
  ///
  /// Returns the points to subtract from the current score.
  /// The result is always positive (the caller should subtract it).
  static int calculateMismatchPenalty() {
    return mismatchPenalty;
  }

  /// Applies a mismatch penalty to the current score.
  ///
  /// Ensures the score never goes below 0.
  static int applyMismatchPenalty(int currentScore) {
    return (currentScore - mismatchPenalty).clamp(0, 9999);
  }

  /// Checks if the game has been won.
  ///
  /// The game is won when all pairs have been matched.
  static bool isGameComplete(int matchedPairs, int totalPairs) {
    return matchedPairs == totalPairs;
  }

  /// Calculates the final score with a time bonus.
  ///
  /// The time bonus penalizes slow play: each second elapsed
  /// reduces the final score by 1 point.
  ///
  /// Returns the final score (minimum 0).
  ///
  /// Example:
  /// ```dart
  /// final finalScore = GameLogic.calculateFinalScore(
  ///   baseScore: 1200,
  ///   elapsedSeconds: 90,
  /// );
  /// // Returns 1110 (1200 - 90)
  /// ```
  static int calculateFinalScore({
    required int baseScore,
    required int elapsedSeconds,
  }) {
    return (baseScore - elapsedSeconds).clamp(0, 9999);
  }

  /// Determines if a new score is a personal best.
  ///
  /// Returns `true` if [newScore] is greater than [currentBest].
  static bool isNewBestScore(int newScore, int currentBest) {
    return newScore > currentBest;
  }

  /// Formats elapsed seconds into a MM:SS string.
  ///
  /// Example:
  /// ```dart
  /// GameLogic.formatTime(90); // Returns "01:30"
  /// GameLogic.formatTime(5);  // Returns "00:05"
  /// ```
  static String formatTime(int totalSeconds) {
    final minutes = totalSeconds ~/ 60;
    final seconds = totalSeconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
  }

  /// Generates a summary of game performance.
  ///
  /// Returns a map containing:
  /// - `finalScore`: The score after time penalty
  /// - `accuracy`: Percentage of correct matches (0-100)
  /// - `efficiency`: Ratio of matches to total moves (0-1)
  ///
  /// This can be used for analytics or displaying performance stats.
  static Map<String, dynamic> generatePerformanceSummary({
    required int baseScore,
    required int elapsedSeconds,
    required int totalMoves,
    required int matchedPairs,
    required int totalPairs,
  }) {
    final finalScore = calculateFinalScore(
      baseScore: baseScore,
      elapsedSeconds: elapsedSeconds,
    );

    // Accuracy: correct matches / total moves
    final accuracy = totalMoves > 0
        ? ((matchedPairs / totalMoves) * 100).round()
        : 0;

    // Efficiency: minimum possible moves is totalPairs (one move per pair)
    // Actual moves should be >= totalPairs
    final minMoves = totalPairs;
    final efficiency = totalMoves > 0
        ? (minMoves / totalMoves).clamp(0.0, 1.0)
        : 0.0;

    return {
      'finalScore': finalScore,
      'accuracy': accuracy,
      'efficiency': efficiency,
      'totalMoves': totalMoves,
      'elapsedSeconds': elapsedSeconds,
    };
  }
}