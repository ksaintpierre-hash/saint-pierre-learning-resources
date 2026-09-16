type AuthProblem = { code?: string; name?: string; message?: string; status?: number; reasons?: string[] };

// Deliberately never echo server messages, passwords, or tokens into the UI/logs.
export function authFeedback(problem: unknown): string {
  const e: AuthProblem = problem && typeof problem === 'object' ? problem : {};
  const code = e.code || '';
  const message = (e.message || '').toLowerCase();
  if (code === 'same_password' || message.includes('different from the old password'))
    return 'That is already your current password. Choose a different new password. If you just changed it, the earlier change may already have succeeded.';
  if (code === 'weak_password' || e.name === 'AuthWeakPasswordError')
    return 'Choose a stronger, unique password with at least 12 characters, including uppercase and lowercase letters, a number, and a symbol. Avoid commonly used passwords.';
  if (code === 'reauthentication_needed' || code === 'reauthentication_not_valid')
    return 'Please log out and log back in with your current password, then return here to change it. Your sign-in needs to be verified again. [reauthentication_needed]';
  if (code === 'invalid_credentials' || message.includes('invalid login credentials'))
    return 'The email or current password does not match. Check autofill and make sure you are using your most recently saved password.';
  if (code === 'current_password_required' || message.includes('current password is required'))
    return 'Enter your current password in the Current password field.';
  if (code === 'current_password_invalid' || message.includes('current password is incorrect'))
    return 'The current password is incorrect. Enter the password you most recently used to log in.';
  if (code === 'over_email_send_rate_limit')
    return 'Email requests are temporarily limited. Please stop resending and contact support if your earlier email has not arrived. [over_email_send_rate_limit]';
  if (e.status === 429 || code === 'over_request_rate_limit' || message.includes('security purposes'))
    return 'Too many requests were made. Wait before trying once more. [request_rate_limit]';
  if (code === 'email_not_confirmed' || message.includes('email not confirmed'))
    return 'Your email still needs confirmation. Check your inbox and spam folder, or contact support if it has not arrived.';
  if (code === 'email_address_not_authorized')
    return 'The store email service could not send to this address. Please contact support; repeatedly requesting emails will not resolve this. [email_address_not_authorized]';
  if (code === 'user_already_exists' || message.includes('user already registered'))
    return 'An account already exists. Use Log in with your current password.';
  if (e.status === 401 || ['session_not_found','session_expired','refresh_token_not_found','refresh_token_already_used','bad_jwt'].includes(code) || e.name === 'AuthSessionMissingError')
    return 'Your session has expired. Please log in again, then return to your account. [session_expired]';
  if (e.name === 'AuthRetryableFetchError' || e.name === 'TypeError')
    return 'The connection was interrupted. The result is not confirmed. If you were changing your password, try logging in with the new password before submitting another change. [connection_error]';
  const reference = /^[a-z][a-z0-9_]{0,59}$/.test(code) ? code : e.status && Number.isInteger(e.status) ? `http_${e.status}` : 'auth_unknown';
  return `The account service could not finish this step. Contact support with this reference: ${reference}. Do not send your password.`;
}

export function passwordValidation(password: string, confirmation: string, current?: string): string | null {
  if (password !== confirmation) return 'The new passwords do not match.';
  if (password.length < 12) return 'Use at least 12 characters for the new password.';
  if (current !== undefined && password === current) return 'Choose a new password different from your current password.';
  return null;
}
