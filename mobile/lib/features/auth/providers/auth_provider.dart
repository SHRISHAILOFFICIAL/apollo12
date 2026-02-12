import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/services/api_service.dart';
import '../../../core/constants/app_constants.dart';
import '../../../shared/models/user_model.dart';

/// Auth state
class AuthState {
  final bool isLoading;
  final bool isLoggedIn;
  final User? user;
  final String? error;

  AuthState({
    this.isLoading = false,
    this.isLoggedIn = false,
    this.user,
    this.error,
  });

  AuthState copyWith({
    bool? isLoading,
    bool? isLoggedIn,
    User? user,
    String? error,
  }) {
    return AuthState(
      isLoading: isLoading ?? this.isLoading,
      isLoggedIn: isLoggedIn ?? this.isLoggedIn,
      user: user ?? this.user,
      error: error,
    );
  }
}

/// Auth notifier for state management
class AuthNotifier extends StateNotifier<AuthState> {
  final ApiService _api = ApiService();

  AuthNotifier() : super(AuthState());

  /// Check if user is logged in on app start
  Future<void> checkAuthStatus() async {
    state = state.copyWith(isLoading: true);
    
    final isLoggedIn = await _api.isLoggedIn();
    if (isLoggedIn) {
      try {
        final response = await _api.get(AppConstants.profileEndpoint);
        final user = User.fromJson(response.data);
        state = state.copyWith(
          isLoading: false,
          isLoggedIn: true,
          user: user,
        );
      } catch (e) {
        // Token expired or invalid
        await _api.clearTokens();
        state = state.copyWith(isLoading: false, isLoggedIn: false);
      }
    } else {
      state = state.copyWith(isLoading: false, isLoggedIn: false);
    }
  }

  /// Send OTP for signup
  Future<bool> sendSignupOtp(String email) async {
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      await _api.post(AppConstants.sendSignupOtpEndpoint, data: {'email': email});
      state = state.copyWith(isLoading: false);
      return true;
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: _getErrorMessage(e),
      );
      return false;
    }
  }

  /// Verify OTP
  Future<bool> verifySignupOtp(String email, String otp) async {
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      await _api.post(
        AppConstants.verifySignupOtpEndpoint,
        data: {'email': email, 'otp': otp},
      );
      state = state.copyWith(isLoading: false);
      return true;
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: _getErrorMessage(e),
      );
      return false;
    }
  }

  /// Register new user
  Future<bool> register({
    required String username,
    required String email,
    required String password,
    String? name,
    String? mobile,
  }) async {
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      // Register the user
      await _api.post(
        AppConstants.registerEndpoint,
        data: {
          'username': username,
          'email': email,
          'password': password,
          'confirm_password': password,
          if (mobile != null) 'phone': mobile,
        },
      );

      // Registration successful - now login to get tokens
      return await login(username, password);
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: _getErrorMessage(e),
      );
      return false;
    }
  }

  /// Login with username/email and password
  Future<bool> login(String username, String password) async {
    state = state.copyWith(isLoading: true, error: null);
    
    try {
      final response = await _api.post(
        AppConstants.loginEndpoint,
        data: {
          'username': username,
          'password': password,
        },
      );

      // Save tokens - backend returns {access, refresh}
      await _api.saveTokens(
        response.data['access'],
        response.data['refresh'],
      );

      // Fetch user profile after login
      final profileResponse = await _api.get(AppConstants.profileEndpoint);
      final user = User.fromJson(profileResponse.data);
      
      state = state.copyWith(
        isLoading: false,
        isLoggedIn: true,
        user: user,
      );
      return true;
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: _getErrorMessage(e),
      );
      return false;
    }
  }

  /// Logout
  Future<void> logout() async {
    await _api.clearTokens();
    state = AuthState(isLoggedIn: false);
  }

  /// Clear error
  void clearError() {
    state = state.copyWith(error: null);
  }

  /// Extract error message from exception
  String _getErrorMessage(dynamic e) {
    // For Dio errors
    if (e.toString().contains('DioException')) {
      try {
        final response = (e as dynamic).response;
        if (response != null) {
          final statusCode = response.statusCode;
          final data = response.data;
          
          if (data is Map) {
            // Try common error field names
            final errorMsg = data['error'] ?? 
                           data['detail'] ?? 
                           data['message'] ??
                           data['non_field_errors']?.first;
            if (errorMsg != null) return errorMsg.toString();
          }
          
          return 'Server error: $statusCode';
        }
      } catch (_) {}
    }
    
    // Print error for debugging
    print('Auth Error: $e');
    return 'Connection error. Please try again.';
  }
}

/// Auth provider
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier();
});
