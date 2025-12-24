# Whitelist of trusted email providers
# Only these domains are allowed for signup
# This is more secure than a blocklist approach

ALLOWED_EMAIL_DOMAINS = {
    # Google
    'gmail.com',
    'googlemail.com',
    
    # Microsoft
    'outlook.com',
    'hotmail.com',
    'live.com',
    'msn.com',
    
    # Yahoo
    'yahoo.com',
    'yahoo.co.in',
    'yahoo.co.uk',
    'ymail.com',
    
    # Apple
    'icloud.com',
    'me.com',
    'mac.com',
    
    # Other popular providers
    'protonmail.com',
    'proton.me',
    'zoho.com',
    'aol.com',
    'mail.com',
    
    # Educational (common in India)
    'edu',  # Any .edu domain
    'ac.in',  # Indian academic institutions
    'edu.in',  # Indian educational institutions
    
    # Indian providers
    'rediffmail.com',
    'rediff.com',
}


def is_allowed_email(email: str) -> bool:
    """
    Check if an email address is from an allowed/trusted provider.
    
    Args:
        email: Email address to check
        
    Returns:
        True if email is from an allowed provider, False otherwise
    """
    if not email or '@' not in email:
        return False
    
    domain = email.split('@')[1].lower()
    
    # Check exact domain match
    if domain in ALLOWED_EMAIL_DOMAINS:
        return True
    
    # Check for .edu domains (educational institutions)
    if domain.endswith('.edu') or domain.endswith('.ac.in') or domain.endswith('.edu.in'):
        return True
    
    return False


def get_email_domain(email: str) -> str:
    """Extract domain from email address"""
    if not email or '@' not in email:
        return ''
    return email.split('@')[1].lower()


def get_allowed_domains_list() -> list:
    """Get a formatted list of allowed domains for display"""
    return sorted(ALLOWED_EMAIL_DOMAINS)

