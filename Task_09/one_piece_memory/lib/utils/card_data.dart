/// Static data for One Piece characters used in the memory matching game.
///
/// Each character entry contains:
/// - [name]: Display name shown on the card
/// - [imagePath]: Asset path to the character image (must exist in assets/images/)
///
/// To add more characters:
/// 1. Add the image file to assets/images/
/// 2. Add a new entry to the [characters] list below
/// 3. Ensure pubspec.yaml includes the assets/images/ directory
class CardData {
  /// List of all available One Piece characters for the game.
  /// 
  /// The game uses the first 8 characters for a 4x4 grid (16 cards).
  /// If you want a larger grid (e.g., 6x6 = 36 cards = 18 pairs),
  /// add more characters to this list.
  static const List<CharacterData> characters = [
    CharacterData(
      name: 'Luffy',
      imagePath: 'assets/images/luffy.jpg',
    ),
    CharacterData(
      name: 'Zoro',
      imagePath: 'assets/images/zoro.jpg',
    ),
    CharacterData(
      name: 'Nami',
      imagePath: 'assets/images/nami.jpg',
    ),
    CharacterData(
      name: 'Sanji',
      imagePath: 'assets/images/sanji.jpg',
    ),
    CharacterData(
      name: 'Robin',
      imagePath: 'assets/images/robin.jpg',
    ),
    CharacterData(
      name: 'Chopper',
      imagePath: 'assets/images/chopper.jpg',
    ),
    CharacterData(
      name: 'Ace',
      imagePath: 'assets/images/ace.jpg',
    ),
    CharacterData(
      name: 'Usopp',
      imagePath: 'assets/images/Usopp.jpg',
    ),
  ];
}

/// Simple data class representing a One Piece character.
class CharacterData {
  /// Display name shown on the card when revealed.
  final String name;

  /// Asset path to the character's image file.
  /// Must match a file in the assets/images/ directory.
  final String imagePath;

  const CharacterData({
    required this.name,
    required this.imagePath,
  });
}