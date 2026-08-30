/// Represents a single card in the memory matching game.
///
/// Each card has a unique [id] (to distinguish the two copies of a pair)
/// and a [pairId] (to identify which cards match each other).
///
/// This model is immutable. Use [copyWith] to create modified copies
/// when the card's state changes (e.g., when flipped or matched).
class MemoryCard {
  /// Unique identifier for this specific card instance.
  /// Even though two cards share the same [pairId], they have different [id]s.
  final int id;

  /// Identifier that links two cards as a matching pair.
  /// Two cards with the same [pairId] form a valid match.
  final int pairId;

  /// Path to the character image asset (e.g., 'assets/images/luffy.jpg').
  final String imagePath;

  /// Display name of the character.
  final String characterName;

  /// Whether the card is currently face-up (showing the character).
  final bool isFlipped;

  /// Whether the card has been successfully matched with its pair.
  /// Matched cards remain face-up for the rest of the game.
  final bool isMatched;

  const MemoryCard({
    required this.id,
    required this.pairId,
    required this.imagePath,
    required this.characterName,
    this.isFlipped = false,
    this.isMatched = false,
  });

  /// Creates a copy of this card with the specified fields replaced.
  MemoryCard copyWith({
    int? id,
    int? pairId,
    String? imagePath,
    String? characterName,
    bool? isFlipped,
    bool? isMatched,
  }) {
    return MemoryCard(
      id: id ?? this.id,
      pairId: pairId ?? this.pairId,
      imagePath: imagePath ?? this.imagePath,
      characterName: characterName ?? this.characterName,
      isFlipped: isFlipped ?? this.isFlipped,
      isMatched: isMatched ?? this.isMatched,
    );
  }

  /// Two cards are equal if they have the same [id].
  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is MemoryCard && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() {
    return 'MemoryCard(id: $id, pairId: $pairId, name: $characterName, flipped: $isFlipped, matched: $isMatched)';
  }
}