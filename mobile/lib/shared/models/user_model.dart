/// User model matching backend API
class User {
  final int id;
  final String username;
  final String email;
  final String? phone;
  final String currentTier;
  final bool emailVerified;
  final DateTime? createdAt;

  User({
    required this.id,
    required this.username,
    required this.email,
    this.phone,
    this.currentTier = 'FREE',
    this.emailVerified = false,
    this.createdAt,
  });

  /// Create from JSON
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] ?? 0,
      username: json['username'] ?? '',
      email: json['email'] ?? '',
      phone: json['phone'],
      currentTier: json['current_tier'] ?? 'FREE',
      emailVerified: json['email_verified'] ?? false,
      createdAt: json['created_at'] != null 
          ? DateTime.tryParse(json['created_at']) 
          : null,
    );
  }

  /// Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'phone': phone,
      'current_tier': currentTier,
      'email_verified': emailVerified,
    };
  }

  /// Check if user has PRO subscription
  bool get isPro => currentTier == 'PRO';
}
