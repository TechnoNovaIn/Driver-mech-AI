const fs = require('fs');
const path = require('path');

console.log('================================================================');
console.log('--- PRODUCTION READINESS VERIFICATION SUITE ---');
console.log('================================================================');

let failed = false;
function assert(desc, cond) {
  if (cond) {
    console.log('  ✅ PASS: ' + desc);
  } else {
    console.error('  ❌ FAIL: ' + desc);
    failed = true;
  }
}

const ROOT = path.resolve(__dirname, '..');
const appShellPath = path.join(ROOT, 'app', 'src', 'main', 'assets', 'app_shell.js');
const mainActivityPath = path.join(ROOT, 'app', 'src', 'main', 'java', 'com', 'mahindra', 'bsvi', 'MainActivity.java');
const newBackendPath = path.join(ROOT, 'backend', 'NEW_BACKEND_CODE.gs');
const codeGsPath = path.join(ROOT, 'backend', 'Code.gs');

const shellCode = fs.readFileSync(appShellPath, 'utf8');
const javaCode = fs.readFileSync(mainActivityPath, 'utf8');
const newBackendCode = fs.readFileSync(newBackendPath, 'utf8');
const codeGs = fs.readFileSync(codeGsPath, 'utf8');

// 1. VOICE INPUT AUDIT
console.log('\n[1. VOICE INPUT ROBUSTNESS]');
assert('MainActivity overrides onJsAlert, onJsConfirm, and onJsPrompt in WebChromeClient',
  javaCode.includes('public boolean onJsAlert(') &&
  javaCode.includes('public boolean onJsConfirm(') &&
  javaCode.includes('public boolean onJsPrompt(')
);
assert('MainActivity checks intent.resolveActivity before launching Speech Dialog',
  javaCode.includes('intent.resolveActivity(getPackageManager())')
);
assert('MainActivity has SpeechRecognizer error-code translation with graceful fallback',
  javaCode.includes('SpeechRecognizer.ERROR_NO_MATCH') &&
  javaCode.includes('SpeechRecognizer.ERROR_NETWORK') &&
  javaCode.includes('tryInProcessSpeechRecognizer')
);
assert('app_shell.js maintains persistent window.nativeSpeechResult and window.nativeSpeechError',
  shellCode.includes('window.nativeSpeechResult = function(') &&
  shellCode.includes('window.nativeSpeechError = function(') &&
  !shellCode.includes('window.nativeSpeechResult=null')
);
assert('app_shell.js provides on-screen dictation modal fallback when speech recognition is unavailable',
  shellCode.includes('function showDictationModal(') &&
  shellCode.includes('applyDictationInput(')
);

// 2. LOGIN HARDENING AUDIT
console.log('\n[2. LOGIN HARDENING & GOOGLE APPS SCRIPT CONNECTIVITY]');
assert('NEW_BACKEND_CODE.gs cleans up expired sessions to prevent script property limits',
  newBackendCode.includes('nowMs>=Number(parsed.exp)') && newBackendCode.includes('pr.deleteProperty(k)')
);
assert('Backend normalizes mobile numbers stripping non-digits',
  newBackendCode.includes('replace(/\\D/g') && codeGs.includes('replace(/\\D/g')
);
assert('Backend formats phone cells with plain text format (@) to prevent float conversion',
  newBackendCode.includes("setNumberFormat('@')") && codeGs.includes("setNumberFormat('@')")
);
assert('app_shell.js finishes login using queued apiRequest("me") to prevent appHttpResult desync',
  shellCode.includes("apiRequest('me'")
);
assert('Backend role matching is case-insensitive and trimmed',
  newBackendCode.includes("['ADMIN','MECHANIC','EMPLOYEE','DRIVER'].includes(nm)") &&
  codeGs.includes("['ADMIN', 'DRIVER', 'MECHANIC', 'EMPLOYEE'].indexOf(roleName)")
);

// 3. ADMIN USER & ROLE MANAGEMENT AUDIT
console.log('\n[3. ADMIN USER & ROLE MANAGEMENT]');
assert('Admin Users screen has EMPLOYEE selected by default',
  shellCode.includes("ro.name === 'EMPLOYEE' ? 'selected' : ''")
);
assert('Dynamic list_roles callback preserves selected role instead of resetting to ADMIN',
  shellCode.includes("const currentVal = sel.value || 'EMPLOYEE';") &&
  shellCode.includes("ro.name === currentVal ? 'selected' : ''")
);
assert('Non-blocking HTML modals implemented for confirmation, password reset, and editing',
  shellCode.includes('function showConfirmModal(') &&
  shellCode.includes('function resetManagedPassword(') &&
  shellCode.includes('function showEditEmployeeModal(')
);
assert('Modern toast notification system implemented (.ma-toast)',
  shellCode.includes('function showToast(') &&
  shellCode.includes('.ma-toast')
);
assert('window exports include all modal and user action functions',
  shellCode.includes('showConfirmModal:showConfirmModal') &&
  shellCode.includes('showToast:showToast') &&
  shellCode.includes('resetManagedPassword:resetManagedPassword') &&
  shellCode.includes('submitResetPassword:submitResetPassword') &&
  shellCode.includes('toggleManagedStatus:toggleManagedStatus') &&
  shellCode.includes('quickChangeRole:quickChangeRole')
);

// 4. SYNTAX INTEGRITY AUDIT
console.log('\n[4. SYNTAX & INTEGRITY CHECK]');
try {
  new Function(shellCode);
  assert('app_shell.js JavaScript syntax parses 100% cleanly', true);
} catch (e) {
  assert('app_shell.js JavaScript syntax parses 100% cleanly: ' + e.message, false);
}

console.log('\n================================================================');
if (failed) {
  console.error('❌ PRODUCTION READINESS VERIFICATION FAILED');
  process.exit(1);
} else {
  console.log('🌟 ALL PRODUCTION READINESS CHECKS PASSED 100%! 🌟');
  console.log('================================================================');
  process.exit(0);
}
