/// API and app constants
class AppConstants {
  // API Configuration
  // TODO: Update this to your server IP/domain
  static const String baseUrl = 'http://192.168.1.17/api';
  
  // API Endpoints - Auth
  static const String loginEndpoint = '/auth/login/';
  static const String registerEndpoint = '/auth/register/';
  static const String refreshTokenEndpoint = '/token/refresh/';
  static const String profileEndpoint = '/auth/profile/';
  
  // API Endpoints - OTP
  static const String sendSignupOtpEndpoint = '/users/send-signup-otp/';
  static const String verifySignupOtpEndpoint = '/users/verify-signup-otp/';
  static const String sendPasswordResetOtpEndpoint = '/users/send-password-reset-otp/';
  
  // API Endpoints - Exams
  static const String examsEndpoint = '/exams/';
  static const String startExamEndpoint = '/exam/timer/start/';
  static const String submitAnswerEndpoint = '/exam/timer/submit-answer/';
  static const String submitExamEndpoint = '/exam/timer/submit/';
  static const String remainingTimeEndpoint = '/exam/timer/remaining/';
  
  // API Endpoints - Results
  static const String resultsEndpoint = '/results/';
  static const String dashboardEndpoint = '/dashboard/';
  
  // API Endpoints - Payments
  static const String plansEndpoint = '/payments/plans/';
  static const String createOrderEndpoint = '/payments/create-order/';
  static const String verifyPaymentEndpoint = '/payments/verify-payment/';
  static const String subscriptionStatusEndpoint = '/payments/subscription-status/';
  
  // Storage Keys
  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userDataKey = 'user_data';
  
  // App Info
  static const String appName = 'DCET Mock Test';
  static const String appVersion = '1.0.0';
}
