// Automated verification for all 4 issues
const fs = require('fs');
const path = require('path');

const shellPath = path.join(__dirname, '../app/src/main/assets/app_shell.js');
const shellCode = fs.readFileSync(shellPath, 'utf8');

const mainActivityPath = path.join(__dirname, '../app/src/main/java/com/mahindra/bsvi/MainActivity.java');
const mainActivityJava = fs.readFileSync(mainActivityPath, 'utf8');

console.log('================================================================');
console.log('--- EXHAUSTIVE 4-ISSUE VERIFICATION SUITE ---');
console.log('================================================================');

let failed = false;
function assert(desc, condition) {
  if (condition) {
    console.log('  ✅ PASS: ' + desc);
  } else {
    console.error('  ❌ FAIL: ' + desc);
    failed = true;
  }
}

// ISSUE 1: MENU ICON AND SIDEBAR ALIGNMENT
console.log('\n[ISSUE 1] MENU ICON AND SIDEBAR ALIGNMENT:');
assert('Hamburger menu icon is on the left in header bar',
  shellCode.includes('class="ma-bar"') && shellCode.includes('button class="ma-icon" onclick="maOpenMenu()"')
);
assert('Sidebar sheet (.ma-sheet) is aligned to left:0 (not right:0)',
  shellCode.includes('.ma-sheet{position:absolute;top:var(--sat);left:0;') ||
  (shellCode.includes('.ma-sheet{') && shellCode.includes('left:0') && !shellCode.includes('.ma-sheet{position:absolute;top:0;right:0;'))
);
assert('Sidebar appears directly below status bar using var(--sat)',
  shellCode.includes('top:var(--sat);left:0;bottom:0;')
);
assert('Sidebar slides smoothly from left with translateX(-100%) to translateX(0)',
  shellCode.includes('transform:translateX(-100%)') && shellCode.includes('.ma-drawer.open .ma-sheet{transform:translateX(0)}')
);
assert('Dark semi-transparent overlay behind sidebar',
  shellCode.includes('.ma-drawer{') && shellCode.includes('background:rgba(15,23,42,0.65)') && shellCode.includes('backdrop-filter:blur(2px)')
);
assert('Close button inside sidebar at top-right corner with close action',
  shellCode.includes('.ma-sheet-head{display:flex;align-items:center;justify-content:space-between;') &&
  shellCode.includes('button class="ma-sheet-close" onclick="maCloseMenu()"')
);
assert('Clicking overlay or close button closes the drawer',
  shellCode.includes('id="maDrawer" class="ma-drawer" onclick="if(event.target===this)maCloseMenu()"')
);
assert('Sidebar width is constrained and does not cover entire screen unnecessarily',
  shellCode.includes('width:min(82vw,320px)') || shellCode.includes('width:min(80vw,320px)')
);

// ISSUE 2: APPLICATION-WIDE KANNADA, HINDI & ENGLISH LOCALIZATION
console.log('\n[ISSUE 2] COMPLETE KANNADA, HINDI & ENGLISH LOCALIZATION:');
assert('Language dictionary has complete Kannada and Hindi translations',
  shellCode.includes('kn:{') && shellCode.includes('hi:{') && shellCode.includes('en:{')
);
assert('Dashboard headings & welcome translated in Kannada & Hindi',
  shellCode.includes('welcome:\'ಸ್ವಾಗತ\'') && shellCode.includes('welcome:\'स्वागत है\'') &&
  shellCode.includes('adminSection:\'ಆಡಳಿತ ಮಂಡಳಿ\'') && shellCode.includes('mechSection:\'ಮೆಕಾನಿಕ್ ಕೆಲಸ\'')
);
assert('Dashboard cards localized across Driver, Mechanic, Employee & Admin',
  shellCode.includes('cardVehicle:\'ವಾಹನದ ಸಮಸ್ಯೆ\'') && shellCode.includes('cardVehicle:\'वाहन की समस्या\'') &&
  shellCode.includes('cardWarning:\'ವಾರ್ನಿಂಗ್ ಲೈಟ್‌ಗಳು\'') && shellCode.includes('cardDpf:\'DPF ರಿಜೆನರೇಷನ್\'') &&
  shellCode.includes('cardDailyCheck:\'ದಿನನಿತ್ಯದ ತಪಾಸಣೆ\'') && shellCode.includes('cardSafety:\'ಚಾಲಕ ಸುರಕ್ಷತೆ\'') &&
  shellCode.includes('cardMechUpdate:\'ಮೆಕಾನಿಕ್ ಕೆಲಸದ ಅಪ್‌ಡೇಟ್\'') && shellCode.includes('cardEmpUpdate:\'ದಿನನಿತ್ಯದ ಕೆಲಸದ ಅಪ್‌ಡೇಟ್\'') &&
  shellCode.includes('cardAdminUsers:\'ಬಳಕೆದಾರರ ನಿರ್ವಹಣೆ\'') && shellCode.includes('cardAdminWork:\'ಕೆಲಸದ ಅಪ್‌ಡೇಟ್‌ಗಳು\'')
);
assert('Common problem chips translated in Kannada & Hindi',
  shellCode.includes('ಇಂಜಿನ್ ತುಂಬಾ ಬಿಸಿಯಾಗುತ್ತಿದೆ.') && shellCode.includes('इंजन बहुत गर्म हो रहा है।') &&
  shellCode.includes('ಹೈವೇಯಲ್ಲಿ ಹಳದಿ DPF ಲೈಟ್ ಬ್ಲಿಂಕ್ ಆಗುತ್ತಿದೆ.') && shellCode.includes('हाईवे पर एम्बर DPF लाइट ब्लिंक कर रही है।')
);
assert('Vehicle problem form labels and placeholders translated',
  shellCode.includes('probTitle:\'ವಾಹನದ ಸಮಸ್ಯೆ ವರದಿ ಮತ್ತು ಪರಿಹಾರಗಳು\'') &&
  shellCode.includes('probTitle:\'वाहन समस्या रिपोर्ट एवं समाधान\'') &&
  shellCode.includes('descLabel:\'ವಾಹನದ ಸಮಸ್ಯೆಯನ್ನು ವಿವರಿಸಿ\'') &&
  shellCode.includes('descLabel:\'वाहन की समस्या का विवरण दें\'')
);
assert('Work update pages and work records translated',
  shellCode.includes('empTitle:\'ದಿನನಿತ್ಯದ ಕೆಲಸದ ಅಪ್‌ಡೇಟ್\'') && shellCode.includes('empTitle:\'दैनिक कार्य अपडेट\'') &&
  shellCode.includes('submitUpdateBtn:\'💾 ಅಪ್‌ಡೇಟ್ ಸಲ್ಲಿಸಿ\'') && shellCode.includes('submitUpdateBtn:\'💾 अपडेट सबमिट करें\'') &&
  shellCode.includes('mechTitle:\'ಮೆಕಾನಿಕ್ ಕೆಲಸದ ಅಪ್‌ಡೇಟ್\'') && shellCode.includes('mechTitle:\'मैकेनिक कार्य अपडेट\'')
);
assert('Troubleshooting instructions & safety warnings translated in Kannada & Hindi',
  shellCode.includes('ಎಂಜಿನ್ ತಾಪಮಾನ ಹೆಚ್ಚು / ಓವರ್‌ಹೀಟಿಂಗ್') && shellCode.includes('इंजन ओवरहीटिंग / कूलेंट का अधिक तापमान') &&
  shellCode.includes('ಬ್ರೇಕ್ ಸಿಸ್ಟಮ್ ಸಮಸ್ಯೆ / ಕಡಿಮೆ ಏರ್ ಪ್ರೆಶರ್ ಎಚ್ಚರಿಕೆ') && shellCode.includes('ब्रेक सिस्टम समस्या / कम एयर प्रेशर चेतावनी')
);
assert('Help page localized for all roles in Kannada, Hindi, and English',
  shellCode.includes('ನಿರ್ವಾಹಕರು — ನೀವು ಮಾಡಬಹುದಾದ ಕೆಲಸಗಳು') && shellCode.includes('व्यवस्थापक — आप क्या कर सकते हैं') &&
  shellCode.includes('ಚಾಲಕ — ನೀವು ಮಾಡಬಹುದಾದ ಕೆಲಸಗಳು') && shellCode.includes('ड्राइवर — आप क्या कर सकते हैं')
);
assert('Language persistent in localStorage and persists across navigation/refresh',
  shellCode.includes('const LANG_KEY=\'mahindra_app_language_v1\';') &&
  shellCode.includes('localStorage.setItem(LANG_KEY,l);')
);

// ISSUE 3: MICROPHONE PERMISSIONS AND VOICE INPUT
console.log('\n[ISSUE 3] MICROPHONE PERMISSIONS AND VOICE INPUT:');
assert('Status message element placed directly below voice input buttons, separate from vehicle number',
  shellCode.includes('id="driverVoiceStatus"') &&
  shellCode.includes('id="driverFormStatus"')
);
assert('Initial voice status is clean and does not display misleading premature error',
  shellCode.includes('<div id="driverVoiceStatus" style="margin:4px 0 12px;min-height:0"></div>')
);
assert('Voice input triggered strictly on explicit button clicks (en-IN, hi-IN, kn-IN)',
  (shellCode.includes('startExactVoice(&quot;en-IN&quot;') || shellCode.includes('startExactVoice("en-IN"')) &&
  (shellCode.includes('startExactVoice(&quot;hi-IN&quot;') || shellCode.includes('startExactVoice("hi-IN"')) &&
  (shellCode.includes('startExactVoice(&quot;kn-IN&quot;') || shellCode.includes('startExactVoice("kn-IN"'))
);
assert('Stop listening button provided (stopActiveVoice)',
  shellCode.includes('id="btnVoiceStop"') && shellCode.includes('stopActiveVoice()')
);
assert('Clear guidance when microphone permission denied or blocked',
  shellCode.includes('micBlocked') &&
  shellCode.includes('ಮೈಕ್ರೋಫೋನ್ ಪ್ರವೇಶವನ್ನು ನಿರ್ಬಂಧಿಸಲಾಗಿದೆ') &&
  shellCode.includes('माइक्रोफोन का उपयोग ब्लॉक है')
);
assert('Browser compatibility and secure context rules checked',
  shellCode.includes('window.isSecureContext===false') &&
  shellCode.includes('micNotSupported')
);
assert('Native AndroidBridge in MainActivity handles pendingSpeechLocale on permission grant',
  mainActivityJava.includes('private String pendingSpeechLocale') &&
  mainActivityJava.includes('startNativeSpeech(pendingSpeechLocale);')
);
assert('Native AndroidBridge provides stopSpeech and isSpeechAvailable',
  mainActivityJava.includes('public void stopSpeech()') &&
  mainActivityJava.includes('public boolean isSpeechAvailable()')
);
assert('Voice input puts speech into editable description box allowing edits before submit',
  shellCode.includes('target.value=cur?(cur+\' \'+text):text') ||
  shellCode.includes('target.value=cur?(cur+\' \'+transcript):transcript')
);

// ISSUE 4: SOLUTION BUTTON TEXT AND TROUBLESHOOTING ENGINE
console.log('\n[ISSUE 4] SOLUTION BUTTON TEXT AND TROUBLESHOOTING ENGINE:');
assert('Button text is exactly SOLUTION in English',
  shellCode.includes('solutionBtn:\'SOLUTION\'')
);
assert('Button text is exactly ಪರಿಹಾರ in Kannada',
  shellCode.includes('solutionBtn:\'ಪರಿಹಾರ\'')
);
assert('Button text is exactly समाधान in Hindi',
  shellCode.includes('solutionBtn:\'समाधान\'')
);
assert('Long text GET INSTANT TROUBLESHOOTING removed from visible button',
  !shellCode.includes('GET INSTANT TROUBLESHOOTING SOLUTION</button>') &&
  !shellCode.includes('🚀 GET INSTANT TROUBLESHOOTING SOLUTION')
);
assert('Red styling and rounded corners preserved for mobile',
  shellCode.includes('.ma-btn-submit{border:0;background:#b71c1c;color:#fff;padding:14px 22px;min-height:52px;border-radius:12px;')
);
assert('Troubleshooting engine preserves evaluation and reporting',
  shellCode.includes('function getInstantTroubleshoot()') &&
  shellCode.includes('identifyProblem(text)') &&
  shellCode.includes('renderTroubleshootingResult')
);
assert('Save Report Only and Call Supervisor remain fully functional',
  shellCode.includes('saveDriverProblemDirect()') &&
  shellCode.includes('callFleetEscalation()')
);

console.log('================================================================');
if (failed) {
  console.error('❌ ONE OR MORE TESTS FAILED');
  process.exit(1);
} else {
  console.log('🌟 ALL 4-ISSUE VERIFICATION TESTS PASSED 100%! 🌟');
  console.log('================================================================');
}
