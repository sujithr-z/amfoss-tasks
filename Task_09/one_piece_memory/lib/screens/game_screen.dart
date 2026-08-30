import 'dart:async';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../models/memory_card.dart';
import '../services/storage_service.dart';
import '../utils/game_logic.dart';
import '../widgets/memory_card_widget.dart';
import '../widgets/score_board.dart';

class GameScreen extends StatefulWidget {
  final void Function(int score)? onGameComplete;

  const GameScreen({super.key, this.onGameComplete});

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  // Card state
  List<MemoryCard> _cards = [];
  int? _firstIndex;
  int? _secondIndex;
  bool _isChecking = false; // Locks input while revealing a mismatch

  // Game metrics
  int _score = GameLogic.initialScore;
  int _moves = 0;
  int _matchedPairs = 0;
  bool _gameFinished = false;

  // Timer
  Timer? _timer;
  int _elapsedSeconds = 0;

  // Persistence
  int _bestScore = 0;

  // Total pairs in the current game (8 pairs = 16 cards = 4x4 grid)
  static const int _totalPairs = GameLogic.defaultPairs;

  @override
  void initState() {
    super.initState();
    _loadBestScore();
    _initializeGame();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> _loadBestScore() async {
    final score = await StorageService.instance.getBestScore();
    if (mounted) {
      setState(() => _bestScore = score);
    }
  }

  void _initializeGame() {
    _timer?.cancel();

    final deck = GameLogic.generateDeck(pairCount: _totalPairs);

    setState(() {
      _cards = deck;
      _firstIndex = null;
      _secondIndex = null;
      _isChecking = false;
      _score = GameLogic.initialScore;
      _moves = 0;
      _matchedPairs = 0;
      _gameFinished = false;
      _elapsedSeconds = 0;
    });

    // Start the timer
    _startTimer();
  }

  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (_gameFinished) return;
      setState(() => _elapsedSeconds++);
    });
  }

  void _onCardTap(int index) {
    // Ignore taps if:
    // - Game is finished
    // - Currently checking a mismatch
    // - Card is already flipped or matched
    // - Tapping the same card that's already the first selection
    if (_gameFinished ||
        _isChecking ||
        _cards[index].isFlipped ||
        _cards[index].isMatched ||
        index == _firstIndex) {
      return;
    }

    setState(() {
      _cards[index] = _cards[index].copyWith(isFlipped: true);

      if (_firstIndex == null) {
        // First card of the pair
        _firstIndex = index;
      } else {
        // Second card — check for match
        _secondIndex = index;
        _moves++;
        _isChecking = true;
      }
    });

    // If we have two cards, evaluate the match
    if (_firstIndex != null && _secondIndex != null) {
      _evaluateMatch();
    }
  }

  Future<void> _evaluateMatch() async {
    final first = _cards[_firstIndex!];
    final second = _cards[_secondIndex!];

    if (GameLogic.isMatch(first, second)) {
      // MATCH — keep them face up
      await Future.delayed(const Duration(milliseconds: 400));

      if (!mounted) return;
      setState(() {
        _cards[_firstIndex!] = _cards[_firstIndex!].copyWith(isMatched: true);
        _cards[_secondIndex!] = _cards[_secondIndex!].copyWith(isMatched: true);
        _matchedPairs++;
        _score += GameLogic.matchReward; // Reward for correct match
        _firstIndex = null;
        _secondIndex = null;
        _isChecking = false;
      });

      // Check win condition
      if (GameLogic.isGameComplete(_matchedPairs, _totalPairs)) {
        _finishGame();
      }
    } else {
      // NO MATCH — reveal briefly, then flip back
      await Future.delayed(const Duration(milliseconds: 800));

      if (!mounted) return;
      setState(() {
        _cards[_firstIndex!] = _cards[_firstIndex!].copyWith(isFlipped: false);
        _cards[_secondIndex!] = _cards[_secondIndex!].copyWith(isFlipped: false);
        _score = GameLogic.applyMismatchPenalty(_score); // Penalty for wrong match
        _firstIndex = null;
        _secondIndex = null;
        _isChecking = false;
      });
    }
  }

  Future<void> _finishGame() async {
    _timer?.cancel();
    setState(() => _gameFinished = true);

    // Time bonus: subtract 1 point per second elapsed (minimum 0)
    final timeBonus = GameLogic.calculateFinalScore(
      baseScore: _score,
      elapsedSeconds: _elapsedSeconds,
    );

    bool isNewBest = false;
    if (GameLogic.isNewBestScore(timeBonus, _bestScore)) {
      await StorageService.instance.setBestScore(timeBonus);
      setState(() {
        _bestScore = timeBonus;
        isNewBest = true;
      });
    }

    widget.onGameComplete?.call(timeBonus);

    if (!mounted) return;

    // Show the victory dialog
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => _buildVictoryDialog(timeBonus, isNewBest),
    );
  }

  Widget _buildVictoryDialog(int finalScore, bool isNewBest) {
    final theme = Theme.of(context);
    return AlertDialog(
      backgroundColor: theme.cardTheme.color,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      title: Column(
        children: [
          const Text(
            '🏴‍☠️',
            style: TextStyle(fontSize: 48),
          ),
          const SizedBox(height: 8),
          Text(
            'VICTORY!',
            style: GoogleFonts.orbitron(
              fontSize: 28,
              fontWeight: FontWeight.w800,
              color: theme.colorScheme.primary,
              letterSpacing: 3,
            ),
          ),
        ],
      ),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (isNewBest)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: theme.colorScheme.primary.withOpacity(0.15),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(
                  color: theme.colorScheme.primary,
                  width: 1.5,
                ),
              ),
              child: Text(
                '⭐ NEW BEST SCORE ⭐',
                style: GoogleFonts.orbitron(
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                  color: theme.colorScheme.primary,
                  letterSpacing: 2,
                ),
              ),
            ),
          const SizedBox(height: 16),
          _buildStatRow('Final Score', '$finalScore', theme.colorScheme.primary),
          _buildStatRow('Time', GameLogic.formatTime(_elapsedSeconds), null),
          _buildStatRow('Moves', '$_moves', null),
        ],
      ),
      actions: [
        SizedBox(
          width: double.infinity,
          child: ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              _initializeGame();
            },
            child: Text(
              'SAIL AGAIN',
              style: GoogleFonts.orbitron(
                fontSize: 14,
                fontWeight: FontWeight.w700,
                letterSpacing: 2,
              ),
            ),
          ),
        ),
        const SizedBox(height: 8),
        SizedBox(
          width: double.infinity,
          child: OutlinedButton(
            onPressed: () {
              Navigator.of(context).pop();
              Navigator.of(context).pop();
            },
            child: Text(
              'BACK TO HOME',
              style: GoogleFonts.orbitron(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                letterSpacing: 2,
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildStatRow(String label, String value, Color? valueColor) {
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: theme.textTheme.bodyMedium,
          ),
          Text(
            value,
            style: GoogleFonts.orbitron(
              fontSize: 16,
              fontWeight: FontWeight.w700,
              color: valueColor ?? theme.textTheme.bodyLarge?.color,
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    // Responsive padding so cards fit nicely on small screens
    final horizontalPadding = screenWidth < 380 ? 12.0 : 16.0;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'OHARA MEMORY',
          style: GoogleFonts.orbitron(
            fontSize: 16,
            fontWeight: FontWeight.w700,
            letterSpacing: 2,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Restart Game',
            onPressed: _initializeGame,
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Score Board
            ScoreBoard(
              score: _score,
              elapsedSeconds: _elapsedSeconds,
              moves: _moves,
              matchedPairs: _matchedPairs,
              totalPairs: _totalPairs,
            ),

            // Card grid
            Expanded(
              child: Padding(
                padding: EdgeInsets.symmetric(horizontal: horizontalPadding),
                child: GridView.builder(
                  physics: const NeverScrollableScrollPhysics(),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 4,
                    mainAxisSpacing: 10,
                    crossAxisSpacing: 10,
                    childAspectRatio: 0.72,
                  ),
                  itemCount: _cards.length,
                  itemBuilder: (context, index) {
                    return MemoryCardWidget(
                      card: _cards[index],
                      onTap: () => _onCardTap(index),
                    );
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}