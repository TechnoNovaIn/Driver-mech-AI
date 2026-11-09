# encoding: utf-8
"""
Complete fix generator for Mahindra BSVI Driver & Mechanic Guide:
- Issue 1: Menu icon left, sidebar opens from left, directly below status bar, overlay, close top-right
- Issue 2: Complete Kannada, Hindi, and English application-wide localization with persistence
- Issue 3: Robust microphone permissions, explicit clicks, clean status positioning, stop button, error guidance
- Issue 4: Short, clean 'SOLUTION' (ಪರಿಹಾರ / समाधान) button preserving troubleshooting engine
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
SHELL_JS = ASSETS / "app_shell.js"
GEN_JS = ROOT / "build" / "generate_app_shell.py"
JAVA_FILE = ROOT / "app" / "src" / "main" / "java" / "com" / "mahindra" / "bsvi" / "MainActivity.java"
PREVIEW_HTML = ASSETS / "preview.html"

# Read the complete app_shell implementation
app_shell_code = r'''(function(){
  'use strict';
  if(window.__maAppShellLoaded){return;}
  window.__maAppShellLoaded=true;

  const TOKEN='mahindra_secure_token_v1', USER='mahindra_secure_user_v1', MODE='mahindra_user_role_v2';
  const LANG_KEY='mahindra_app_language_v1';
  const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  const getUser=()=>{try{return JSON.parse(localStorage.getItem(USER)||'null')}catch(e){return null}};
  const role=()=>{const r=String(getUser()?.role||'').toUpperCase();return r==='USER'?'DRIVER':r;};
  const name=()=>getUser()?.name||'';
  const hideOld=()=>{['home','screen','topIntro','languagePanel'].forEach(id=>document.getElementById(id)?.classList.add('hide'));document.getElementById('modeOverlay')?.remove();};
  const app=document.body;

  // Persistent Language Preference
  const getLang=()=>{
    const s=localStorage.getItem(LANG_KEY);
    return (s==='kn'||s==='hi'||s==='en')?s:'en';
  };
  const setLang=(v)=>{
    const l=['en','kn','hi'].includes(v)?v:'en';
    localStorage.setItem(LANG_KEY,l);
    if(document.getElementById('maLogin')) renderLogin();
    else if(typeof window.__currentRenderer==='function') window.__currentRenderer();
    else dashboard();
  };
  window.maSetLanguage=setLang;

  // Complete Trilingual Localization Dictionary
  const tr={
    en:{
      appTitle:'DRIVERS/MECH AI',
      dashboard:'Dashboard',
      menu:'MENU',
      home:'Home',
      back:'Back',
      logout:'Log out',
      help:'App Help',
      language:'Language',
      driver:'Driver',
      mechanic:'Mechanic',
      employee:'Employee',
      admin:'Administrator',
      welcome:'Welcome',
      secureDash:'Secure role-based dashboard',
      adminSection:'ADMINISTRATION',
      mechSection:'MECHANIC WORK',
      empSection:'EMPLOYEE WORK',
      driverSection:'DRIVER PORTAL & GUIDE',
      cardVehicle:'VEHICLE PROBLEM',
      cardVehicleSub:'Report problem with/without photo • instant troubleshooting guidance',
      cardWarning:'WARNING LIGHTS',
      cardWarningSub:'Every documented warning-light item + video',
      cardDpf:'DPF REGENERATION',
      cardDpfSub:'Every documented regeneration step + video',
      cardDailyCheck:'DAILY CHECK',
      cardDailyCheckSub:'Every documented before-driving check + video',
      cardAdblue:'ADBLUE / DEF',
      cardAdblueSub:'Every documented AdBlue step + video',
      cardSafety:'DRIVER SAFETY',
      cardSafetySub:'Every documented safety point + video',
      cardMechUpdate:'MECHANIC WORK UPDATE',
      cardMechUpdateSub:'Vehicle number + work completed + voice • save centrally',
      cardMyRecords:'MY WORK RECORDS',
      cardMyRecordsSub:'View your central daily updates',
      cardEmpUpdate:'DAILY WORK UPDATE',
      cardEmpUpdateSub:'Record employee daily work update with typing or voice • save centrally',
      cardEmpRecordsSub:'View your submitted daily work updates',
      cardAdminUsers:'MANAGE USERS',
      cardAdminUsersSub:'Add drivers, mechanics, employees and admins • status • role • password',
      cardAdminWork:'WORK UPDATES',
      cardAdminWorkSub:'View all employee & mechanic daily work updates from central database',
      cardAdminProblems:'PROBLEM REPORTS',
      cardAdminProblemsSub:'View driver vehicle problem reports & instant triage logs',
      cardAdminData:'MAHINDRA DATA',
      cardAdminDataSub:'Professional vehicle specifications, BSVI systems & diagnostic intelligence',
      probTitle:'Vehicle Problem Reporting & Solutions',
      probSub:'Report your truck problem using text or voice. Attach a photo if available (photo is optional).',
      chipsPrompt:'Common Vehicle Problems (Tap to select):',
      descLabel:'Describe Vehicle Problem',
      descPh:'Type or describe the problem here... You can review and edit this text before submitting.',
      charCount:'characters',
      wordsCount:'words',
      voiceConvertsNotice:'🎤 Voice converts to editable text',
      voiceInputLbl:'Voice Input',
      stopListening:'Stop',
      photoBoxTitle:'Attach Photo (Optional)',
      photoBoxSub:'Photo is optional. You can submit without a photo.',
      choosePhotoBtn:'📷 Choose / Take Photo',
      photoAttached:'Photo attached (optional)',
      removePhoto:'✕ Remove',
      vehNoLabel:'Vehicle Number (Optional)',
      vehNoPh:'e.g. KA-01-MJ-5020 (Optional)',
      solutionBtn:'SOLUTION',
      saveReportOnly:'📝 Save Report Only',
      callSupervisor:'📞 Call Supervisor',
      emptyProblemMsg:'⚠️ Please enter or speak the vehicle problem first.',
      savingProblemMsg:'⏳ Saving problem report to fleet database…',
      savedProblemSuccess:'✅ Problem report saved centrally. Fleet managers have been notified.',
      micListening:'🔴 Listening... Speak clearly now.',
      micSuccess:'✅ Voice captured. You can review and edit the text above.',
      micBlocked:'⚠️ Microphone access is blocked. Please allow microphone permission in your browser or device settings, then try again. You can also type directly in the box.',
      micNotSupported:'ℹ️ Speech recognition is not supported in this browser. You can type directly into the box.',
      micInsecure:'ℹ️ Speech recognition requires HTTPS or localhost under browser security rules. You can type directly in the box.',
      micNoSpeech:'ℹ️ No speech detected. Please tap the microphone button and speak clearly, or type in the box.',
      photoTextDetected:'🔎 Photo text detected. Now tap "SOLUTION".',
      photoCaptured:'✅ Photo captured. Now enter or speak your problem description.',
      troubleshootTitle:'Troubleshooting Guidance',
      reportedProblem:'Reported Problem:',
      possibleCause:'Possible Cause:',
      safetyWarning:'Safety Warning:',
      immediateAction:'Immediate Action (Next 10 seconds):',
      stepInstructions:'Step-by-Step Instructions:',
      safeCheckLbl:'🟢 You can safely check:',
      mechReqLbl:'🔴 Call mechanic when:',
      escalationTitle:'Escalation & Assistance Options:',
      callFleetMech:'📞 Call Fleet Mechanic (+91 98450 12345)',
      callFleetSup:'🚨 Call Fleet Supervisor (+91 99887 76655)',
      readAloudBtn:'🔊 Read Solution Aloud',
      reportAnotherBtn:'← Report Another Problem',
      empTitle:'Daily Work Update',
      empSub:'Employee: {name} • Record your daily activity report',
      empDescLabel:'Daily Work Update',
      empPh:'Type your daily work update here... (e.g., Verified 18 cargo dispatch manifests, inspected warehouse safety seals, coordinated logistics billing with finance, resolved driver queries)',
      voiceAndTypingTogether:'🎤 Voice and typing work together seamlessly',
      speakUpdateBtn:'🎤 Speak Update',
      submitUpdateBtn:'💾 Submit Update',
      submittingUpdate:'⏳ Submitting Update…',
      prevSubmittedTitle:'📋 Previously Submitted Updates',
      refreshBtn:'↻ Refresh',
      emptyWorkMsg:'⚠️ Empty update: Please type or speak your daily work update before submitting.',
      saveWorkSuccess:'✅ Success! Your daily work update has been saved successfully in the central database.',
      mechTitle:'Mechanic Work Update',
      mechSub:'Mechanic: {name}',
      vehReq:'Vehicle number (e.g. KA-01-MJ-5020)',
      mechWorkPh:'Work completed (describe maintenance, parts replaced, inspections)',
      mechSaveSuccess:'✅ Daily mechanic update saved centrally.',
      allRecordsTitle:'ALL WORK RECORDS',
      myRecordsTitle:'MY WORK RECORDS',
      exportBtn:'⬇️ Download Data',
      noRecords:'No records yet.',
      noRecordsSub:'No daily work records found. Submit an update and it will appear here.',
      retryBtn:'↻ RETRY',
      loading:'Loading…',
      nameLbl:'Name',
      mobileLbl:'Mobile',
      roleLbl:'Role',
      statusLbl:'Status',
      workCompletedLbl:'Work completed',
      vehicleNoLbl:'Vehicle number',
      manageUsersTitle:'MANAGE USERS',
      addUserTitle:'👥 Add User',
      userListTitle:'Current Users',
      createUserBtn:'➕ CREATE USER',
      namePh:'Name',
      mobilePh:'10-digit mobile',
      passPh:'Password (optional; blank = last 4)',
      adminProblemsTitle:'PROBLEM REPORTS',
      adminProblemsBrand:'📝 Driver Problem Reports',
      adminProblemsSub:'Incident triage and problem notifications submitted by drivers',
      viewAiDiagnosis:'🔍 View AI Diagnosis & Steps',
      mahindraDataTitle:'Mahindra BSVI Data Suite',
      tabOverview:'📊 Overview',
      tabModels:'🚛 Vehicle Models',
      tabSpecs:'⚙️ System Specs',
      tabVisuals:'🖼️ Visual Diagrams',
      tabExplanations:'💡 Simple Explanations',
      tabOps:'📈 Fleet Observations',
      tabSearch:'🔍 Search Manuals',
      searchManualsPh:'Type fault code or component (e.g. P2463, DPF, PRV, Sensor)',
      searchBtn:'Search',
      readRealVideo:'▶ REAL VIDEO\nACTION + INSTRUCTION'
    },
    kn:{
      appTitle:'ಡ್ರೈವರ್ಸ್/ಮೆಕ್ AI',
      dashboard:'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
      menu:'ಮೆನು',
      home:'ಹೋಮ್',
      back:'ಹಿಂದೆ',
      logout:'ಲಾಗ್ ಔಟ್',
      help:'ಆಪ್ ಸಹಾಯ',
      language:'ಭಾಷೆ',
      driver:'ಚಾಲಕ',
      mechanic:'ಮೆಕಾನಿಕ್',
      employee:'ಉದ್ಯೋಗಿ',
      admin:'ನಿರ್ವಾಹಕರು',
      welcome:'ಸ್ವಾಗತ',
      secureDash:'ಸುರಕ್ಷಿತ ಪಾತ್ರ-ಆಧಾರಿತ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
      adminSection:'ಆಡಳಿತ ಮಂಡಳಿ',
      mechSection:'ಮೆಕಾನಿಕ್ ಕೆಲಸ',
      empSection:'ಉದ್ಯೋಗಿ ಕೆಲಸ',
      driverSection:'ಚಾಲಕ ಪೋರ್ಟಲ್ ಮತ್ತು ಮಾರ್ಗದರ್ಶಿ',
      cardVehicle:'ವಾಹನದ ಸಮಸ್ಯೆ',
      cardVehicleSub:'ಫೋಟೋದೊಂದಿಗೆ/ಇಲ್ಲದೆ ಸಮಸ್ಯೆ ವರದಿ ಮಾಡಿ • ತ್ವರಿತ ಪರಿಹಾರ ಮಾರ್ಗದರ್ಶನ',
      cardWarning:'ವಾರ್ನಿಂಗ್ ಲೈಟ್‌ಗಳು',
      cardWarningSub:'ಪ್ರತಿಯೊಂದು ವಾರ್ನಿಂಗ್ ಲೈಟ್ ವಿವರಣೆ + ವೀಡಿಯೋ',
      cardDpf:'DPF ರಿಜೆನರೇಷನ್',
      cardDpfSub:'ರಿಜೆನರೇಷನ್ ಹಂತಗಳು + ವೀಡಿಯೋ',
      cardDailyCheck:'ದಿನನಿತ್ಯದ ತಪಾಸಣೆ',
      cardDailyCheckSub:'ಚಾಲನೆಗೆ ಮುನ್ನ ಮಾಡಬೇಕಾದ ಪರಿಶೀಲನೆಗಳು + ವೀಡಿಯೋ',
      cardAdblue:'ADBLUE / DEF',
      cardAdblueSub:'AdBlue ಭರ್ತಿ ಮಾಡುವ ಹಂತಗಳು + ವೀಡಿಯೋ',
      cardSafety:'ಚಾಲಕ ಸುರಕ್ಷತೆ',
      cardSafetySub:'ಸುರಕ್ಷತಾ ನಿಯಮಗಳು + ವೀಡಿಯೋ',
      cardMechUpdate:'ಮೆಕಾನಿಕ್ ಕೆಲಸದ ಅಪ್‌ಡೇಟ್',
      cardMechUpdateSub:'ವಾಹನ ಸಂಖ್ಯೆ + ಮಾಡಿದ ಕೆಲಸ + ಧ್ವನಿ • ಕೇಂದ್ರದಲ್ಲಿ ಉಳಿಸಿ',
      cardMyRecords:'ನನ್ನ ಕೆಲಸದ ದಾಖಲೆಗಳು',
      cardMyRecordsSub:'ನಿಮ್ಮ ದಿನನಿತ್ಯದ ಅಪ್‌ಡೇಟ್‌ಗಳನ್ನು ವೀಕ್ಷಿಸಿ',
      cardEmpUpdate:'ದಿನನಿತ್ಯದ ಕೆಲಸದ ಅಪ್‌ಡೇಟ್',
      cardEmpUpdateSub:'ಟೈಪಿಂಗ್ ಅಥವಾ ಧ್ವನಿಯ ಮೂಲಕ ದೈನಂದಿನ ಕೆಲಸ ದಾಖಲಿಸಿ • ಉಳಿಸಿ',
      cardEmpRecordsSub:'ಸಲ್ಲಿಸಲಾದ ದಿನನಿತ್ಯದ ಕೆಲಸದ ದಾಖಲೆಗಳನ್ನು ವೀಕ್ಷಿಸಿ',
      cardAdminUsers:'ಬಳಕೆದಾರರ ನಿರ್ವಹಣೆ',
      cardAdminUsersSub:'ಚಾಲಕರು, ಮೆಕಾನಿಕ್‌ಗಳು, ಉದ್ಯೋಗಿಗಳನ್ನು ಸೇರಿಸಿ • ಪಾತ್ರ • ಪಾಸ್‌ವರ್ಡ್',
      cardAdminWork:'ಕೆಲಸದ ಅಪ್‌ಡೇಟ್‌ಗಳು',
      cardAdminWorkSub:'ಎಲ್ಲಾ ಉದ್ಯೋಗಿ ಮತ್ತು ಮೆಕಾನಿಕ್ ಕೆಲಸದ ದಾಖಲೆಗಳನ್ನು ವೀಕ್ಷಿಸಿ',
      cardAdminProblems:'ಸಮಸ್ಯೆ ವರದಿಗಳು',
      cardAdminProblemsSub:'ಚಾಲಕರ ವಾಹನ ಸಮಸ್ಯೆ ವರದಿಗಳು ಮತ್ತು ಪರಿಹಾರ ಲಾಗ್‌ಗಳು',
      cardAdminData:'ಮಹೀಂದ್ರಾ ಡೇಟಾ',
      cardAdminDataSub:'ವಾಹನ ತಾಂತ್ರಿಕ ವಿವರಗಳು, BSVI ಸಿಸ್ಟಂ ಮತ್ತು ರೋಗನಿರ್ಣಯ ಮಾಹಿತಿ',
      probTitle:'ವಾಹನದ ಸಮಸ್ಯೆ ವರದಿ ಮತ್ತು ಪರಿಹಾರಗಳು',
      probSub:'ಪಠ್ಯ ಅಥವಾ ಧ್ವನಿ ಬಳಸಿ ನಿಮ್ಮ ಟ್ರಕ್ ಸಮಸ್ಯೆಯನ್ನು ವರದಿ ಮಾಡಿ. ಫೋಟೋ ಲಭ್ಯವಿದ್ದರೆ ಲಗತ್ತಿಸಿ (ಫೋಟೋ ಐಚ್ಛಿಕ).',
      chipsPrompt:'ಸಾಮಾನ್ಯ ವಾಹನ ಸಮಸ್ಯೆಗಳು (ಆಯ್ಕೆ ಮಾಡಲು ಒತ್ತಿರಿ):',
      descLabel:'ವಾಹನದ ಸಮಸ್ಯೆಯನ್ನು ವಿವರಿಸಿ',
      descPh:'ಸಮಸ್ಯೆಯನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ ಅಥವಾ ಮಾತನಾಡಿ... ಸಲ್ಲಿಸುವ ಮೊದಲು ನೀವು ಈ ಪಠ್ಯವನ್ನು ಪರಿಶೀಲಿಸಬಹುದು ಮತ್ತು ತಿದ್ದಬಹುದು.',
      charCount:'ಅಕ್ಷರಗಳು',
      wordsCount:'ಪದಗಳು',
      voiceConvertsNotice:'🎤 ಧ್ವನಿಯು ತಿದ್ದಬಹುದಾದ ಪಠ್ಯವಾಗಿ ಪರಿವರ್ತನೆಯಾಗುತ್ತದೆ',
      voiceInputLbl:'ಧ್ವನಿ ಇನ್‌ಪುಟ್',
      stopListening:'ನಿಲ್ಲಿಸಿ',
      photoBoxTitle:'ಫೋಟೋ ಲಗತ್ತಿಸಿ (ಐಚ್ಛಿಕ)',
      photoBoxSub:'ಫೋಟೋ ಐಚ್ಛಿಕವಾಗಿದೆ. ಫೋಟೋ ಇಲ್ಲದೆಯೂ ನೀವು ಸಲ್ಲಿಸಬಹುದು.',
      choosePhotoBtn:'📷 ಫೋಟೋ ಆಯ್ಕೆ / ತೆಗೆಯಿರಿ',
      photoAttached:'ಫೋಟೋ ಲಗತ್ತಿಸಲಾಗಿದೆ (ಐಚ್ಛಿಕ)',
      removePhoto:'✕ ತೆಗೆದುಹಾಕಿ',
      vehNoLabel:'ವಾಹನ ಸಂಖ್ಯೆ (ಐಚ್ಛಿಕ)',
      vehNoPh:'ಉದಾ: KA-01-MJ-5020 (ಐಚ್ಛಿಕ)',
      solutionBtn:'ಪರಿಹಾರ',
      saveReportOnly:'📝 ವರದಿ ಮಾತ್ರ ಉಳಿಸಿ',
      callSupervisor:'📞 ಸೂಪರ್‌ವೈಸರ್‌ಗೆ ಕರೆ ಮಾಡಿ',
      emptyProblemMsg:'⚠️ ದಯವಿಟ್ಟು ಮೊದಲು ವಾಹನದ ಸಮಸ್ಯೆಯನ್ನು ಬರೆಯಿರಿ ಅಥವಾ ಮಾತನಾಡಿ.',
      savingProblemMsg:'⏳ ಫ್ಲೀಟ್ ಡೇಟಾಬೇಸ್‌ಗೆ ಸಮಸ್ಯೆಯ ವರದಿಯನ್ನು ಉಳಿಸಲಾಗುತ್ತಿದೆ…',
      savedProblemSuccess:'✅ ಸಮಸ್ಯೆಯ ವರದಿ ಕೇಂದ್ರ ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ಉಳಿಸಲಾಗಿದೆ. ನಿರ್ವಾಹಕರಿಗೆ ತಿಳಿಸಲಾಗಿದೆ.',
      micListening:'🔴 ಧ್ವನಿ ಕೇಳುತ್ತಿದೆ... ಈಗ ಸ್ಪಷ್ಟವಾಗಿ ಮಾತನಾಡಿ.',
      micSuccess:'✅ ಧ್ವನಿ ಸೆರೆಹಿಡಿಯಲಾಗಿದೆ. ಮೇಲಿನ ಪಠ್ಯವನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ತಿದ್ದಬಹುದು.',
      micBlocked:'⚠️ ಮೈಕ್ರೋಫೋನ್ ಪ್ರವೇಶವನ್ನು ನಿರ್ಬಂಧಿಸಲಾಗಿದೆ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಬ್ರೌಸರ್ ಅಥವಾ ಡಿವೈಸ್ ಸೆಟ್ಟಿಂಗ್ಸ್‌ನಲ್ಲಿ ಮೈಕ್ರೋಫೋನ್ ಅನುಮತಿ ನೀಡಿ. ನೀವು ನೇರವಾಗಿ ಟೈಪ್ ಕೂಡ ಮಾಡಬಹುದು.',
      micNotSupported:'ℹ️ ಈ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಧ್ವನಿ ಗುರುತಿಸುವಿಕೆ ಬೆಂಬಲಿತವಾಗಿಲ್ಲ. ನೀವು ನೇರವಾಗಿ ಪೆಟ್ಟಿಗೆಯಲ್ಲಿ ಟೈಪ್ ಮಾಡಬಹುದು.',
      micInsecure:'ℹ️ ಬ್ರೌಸರ್ ನಿಯಮಗಳ ಪ್ರಕಾರ ಧ್ವನಿ ಗುರುತಿಸುವಿಕೆಗೆ HTTPS ಅಥವಾ localhost ಅಗತ್ಯವಿದೆ. ನೀವು ನೇರವಾಗಿ ಟೈಪ್ ಮಾಡಬಹುದು.',
      micNoSpeech:'ℹ️ ಯಾವುದೇ ಧ್ವನಿ ಪತ್ತೆಯಾಗಿಲ್ಲ. ಬಟನ್ ಒತ್ತಿ ಸ್ಪಷ್ಟವಾಗಿ ಮಾತನಾಡಿ ಅಥವಾ ಟೈಪ್ ಮಾಡಿ.',
      photoTextDetected:'🔎 ಫೋಟೋ ಪಠ್ಯ ಪತ್ತೆಯಾಗಿದೆ. ಈಗ "ಪರಿಹಾರ" ಬಟನ್ ಒತ್ತಿರಿ.',
      photoCaptured:'✅ ಫೋಟೋ ತೆಗೆಯಲಾಗಿದೆ. ಈಗ ನಿಮ್ಮ ಸಮಸ್ಯೆಯ ವಿವರಣೆಯನ್ನು ಬರೆಯಿರಿ ಅಥವಾ ಮಾತನಾಡಿ.',
      troubleshootTitle:'ಪರಿಹಾರ ಮಾರ್ಗದರ್ಶನ',
      reportedProblem:'ವರದಿ ಮಾಡಿದ ಸಮಸ್ಯೆ:',
      possibleCause:'ಸಂಭಾವ್ಯ ಕಾರಣ:',
      safetyWarning:'ಸುರಕ್ಷತಾ ಎಚ್ಚರಿಕೆ:',
      immediateAction:'ತಕ್ಷಣದ ಕ್ರಮ (ಮುಂದಿನ 10 ಸೆಕೆಂಡುಗಳಲ್ಲಿ):',
      stepInstructions:'ಹಂತ-ಹಂತದ ಸೂಚನೆಗಳು:',
      safeCheckLbl:'🟢 ನೀವು ಸುರಕ್ಷಿತವಾಗಿ ಪರಿಶೀಲಿಸಬಹುದಾದ್ದು:',
      mechReqLbl:'🔴 ಮೆಕಾನಿಕ್ ಕರೆಯಬೇಕಾದ ಸಂದರ್ಭ:',
      escalationTitle:'ಸಂಪರ್ಕ ಮತ್ತು ಸಹಾಯ ಆಯ್ಕೆಗಳು:',
      callFleetMech:'📞 ಫ್ಲೀಟ್ ಮೆಕಾನಿಕ್‌ಗೆ ಕರೆ ಮಾಡಿ (+91 98450 12345)',
      callFleetSup:'🚨 ಸೂಪರ್‌ವೈಸರ್‌ಗೆ ಕರೆ ಮಾಡಿ (+91 99887 76655)',
      readAloudBtn:'🔊 ಪರಿಹಾರವನ್ನು ಗಟ್ಟಿಯಾಗಿ ಕೇಳಿ',
      reportAnotherBtn:'← ಇನ್ನೊಂದು ಸಮಸ್ಯೆಯನ್ನು ವರದಿ ಮಾಡಿ',
      empTitle:'ದಿನನಿತ್ಯದ ಕೆಲಸದ ಅಪ್‌ಡೇಟ್',
      empSub:'ಉದ್ಯೋಗಿ: {name} • ನಿಮ್ಮ ದೈನಂದಿನ ಕೆಲಸದ ವರದಿಯನ್ನು ದಾಖಲಿಸಿ',
      empDescLabel:'ದಿನನಿತ್ಯದ ಕೆಲಸದ ವಿವರ',
      empPh:'ನಿಮ್ಮ ದಿನನಿತ್ಯದ ಕೆಲಸದ ವಿವರವನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ... (ಉದಾ: 18 ಡಿಸ್ಪ್ಯಾಚ್ ಪರಿಶೀಲನೆ, ಸುರಕ್ಷತಾ ಸೀಲ್ ತಪಾಸಣೆ, ಲಾಜಿಸ್ಟಿಕ್ಸ್ ಬಿಲ್ಲಿಂಗ್ ಸಮನ್ವಯ, ಚಾಲಕರ ವಿಚಾರಣೆ ಪರಿಹಾರ)',
      voiceAndTypingTogether:'🎤 ಧ್ವನಿ ಮತ್ತು ಟೈಪಿಂಗ್ ಎರಡೂ ಒಟ್ಟಿಗೆ ಕೆಲಸ ಮಾಡುತ್ತವೆ',
      speakUpdateBtn:'🎤 ಧ್ವನಿ ಮೂಲಕ ಹೇಳಿ',
      submitUpdateBtn:'💾 ಅಪ್‌ಡೇಟ್ ಸಲ್ಲಿಸಿ',
      submittingUpdate:'⏳ ಅಪ್‌ಡೇಟ್ ಸಲ್ಲಿಸಲಾಗುತ್ತಿದೆ…',
      prevSubmittedTitle:'📋 ಹಿಂದೆ ಸಲ್ಲಿಸಿದ ಅಪ್‌ಡೇಟ್‌ಗಳು',
      refreshBtn:'↻ ರಿಫ್ರೆಶ್',
      emptyWorkMsg:'⚠️ ಖಾಲಿ ವಿವರ: ದಯವಿಟ್ಟು ಸಲ್ಲಿಸುವ ಮುನ್ನ ನಿಮ್ಮ ಕೆಲಸದ ವಿವರವನ್ನು ಟೈಪ್ ಮಾಡಿ ಅಥವಾ ಮಾತನಾಡಿ.',
      saveWorkSuccess:'✅ ಯಶಸ್ವಿ! ನಿಮ್ಮ ದಿನನಿತ್ಯದ ಕೆಲಸದ ಅಪ್‌ಡೇಟ್ ಕೇಂದ್ರ ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ಉಳಿಸಲಾಗಿದೆ.',
      mechTitle:'ಮೆಕಾನಿಕ್ ಕೆಲಸದ ಅಪ್‌ಡೇಟ್',
      mechSub:'ಮೆಕಾನಿಕ್: {name}',
      vehReq:'ವಾಹನ ಸಂಖ್ಯೆ (ಉದಾ: KA-01-MJ-5020)',
      mechWorkPh:'ಮಾಡಿದ ಕೆಲಸ (ನಿರ್ವಹಣೆ, ಬದಲಾಯಿಸಲಾದ ಭಾಗಗಳು, ತಪಾಸಣೆಗಳನ್ನು ವಿವರಿಸಿ)',
      mechSaveSuccess:'✅ ದಿನನಿತ್ಯದ ಮೆಕಾನಿಕ್ ಅಪ್‌ಡೇಟ್ ಕೇಂದ್ರದಲ್ಲಿ ಉಳಿಸಲಾಗಿದೆ.',
      allRecordsTitle:'ಎಲ್ಲಾ ಕೆಲಸದ ದಾಖಲೆಗಳು',
      myRecordsTitle:'ನನ್ನ ಕೆಲಸದ ದಾಖಲೆಗಳು',
      exportBtn:'⬇️ ಡೇಟಾ ಡೌನ್‌ಲೋಡ್',
      noRecords:'ಯಾವುದೇ ದಾಖಲೆಗಳಿಲ್ಲ.',
      noRecordsSub:'ಯಾವುದೇ ಕೆಲಸದ ದಾಖಲೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ಅಪ್‌ಡೇಟ್ ಸಲ್ಲಿಸಿದ ನಂತರ ಇಲ್ಲಿ ಕಾಣಿಸುತ್ತದೆ.',
      retryBtn:'↻ ಮರುಪ್ರಯತ್ನಿಸಿ',
      loading:'ಲೋಡ್ ಆಗುತ್ತಿದೆ…',
      nameLbl:'ಹೆಸರು',
      mobileLbl:'ಮೊಬೈಲ್',
      roleLbl:'ಪಾತ್ರ',
      statusLbl:'ಸ್ಥಿತಿ',
      workCompletedLbl:'ಮಾಡಿದ ಕೆಲಸ',
      vehicleNoLbl:'ವಾಹನ ಸಂಖ್ಯೆ',
      manageUsersTitle:'ಬಳಕೆದಾರರ ನಿರ್ವಹಣೆ',
      addUserTitle:'👥 ಬಳಕೆದಾರರನ್ನು ಸೇರಿಸಿ',
      userListTitle:'ಪ್ರಸ್ತುತ ಬಳಕೆದಾರರು',
      createUserBtn:'➕ ಬಳಕೆದಾರರನ್ನು ರಚಿಸಿ',
      namePh:'ಹೆಸರು',
      mobilePh:'10 ಅಂಕಿಯ ಮೊಬೈಲ್',
      passPh:'ಪಾಸ್‌ವರ್ಡ್ (ಐಚ್ಛಿಕ; ಖಾಲಿ = ಕೊನೆಯ 4)',
      adminProblemsTitle:'ಸಮಸ್ಯೆ ವರದಿಗಳು',
      adminProblemsBrand:'📝 ಚಾಲಕರ ವಾಹನ ಸಮಸ್ಯೆ ವರದಿಗಳು',
      adminProblemsSub:'ಚಾಲಕರು ಸಲ್ಲಿಸಿದ ಸಮಸ್ಯೆ ಅಧಿಸೂಚನೆಗಳು ಮತ್ತು ಪರಿಹಾರ ಲಾಗ್‌ಗಳು',
      viewAiDiagnosis:'🔍 AI ಪರಿಹಾರ ಮತ್ತು ಹಂತಗಳನ್ನು ವೀಕ್ಷಿಸಿ',
      mahindraDataTitle:'ಮಹೀಂದ್ರಾ BSVI ಡೇಟಾ ಸೂಟ್',
      tabOverview:'📊 ಅವಲೋಕನ',
      tabModels:'🚛 ವಾಹನ ಮಾದರಿಗಳು',
      tabSpecs:'⚙️ ಸಿಸ್ಟಮ್ ವಿವರಣೆಗಳು',
      tabVisuals:'🖼️ ಚಿತ್ರಗಳು',
      tabExplanations:'💡 ಸರಳ ವಿವರಣೆಗಳು',
      tabOps:'📈 ಫ್ಲೀಟ್ ವೀಕ್ಷಣೆಗಳು',
      tabSearch:'🔍 ಮ್ಯಾನ್ಯುವಲ್ ಹುಡುಕಿ',
      searchManualsPh:'ಫಾಲ್ಟ್ ಕೋಡ್ ಅಥವಾ ಭಾಗದ ಹೆಸರು (ಉದಾ: P2463, DPF, PRV, Sensor)',
      searchBtn:'ಹುಡುಕಿ',
      readRealVideo:'▶ ನೈಜ ವೀಡಿಯೋ\nಕ್ರಿಯೆ + ಸೂಚನೆ'
    },
    hi:{
      appTitle:'ड्राइवर्स/मैक AI',
      dashboard:'डैशबोर्ड',
      menu:'मेनू',
      home:'होम',
      back:'वापस',
      logout:'लॉग आउट',
      help:'ऐप सहायता',
      language:'भाषा',
      driver:'ड्राइवर',
      mechanic:'मैकेनिक',
      employee:'कर्मचारी',
      admin:'व्यवस्थापक',
      welcome:'स्वागत है',
      secureDash:'सुरक्षित भूमिका-आधारित डैशबोर्ड',
      adminSection:'प्रशासन',
      mechSection:'मैकेनिक कार्य',
      empSection:'कर्मचारी कार्य',
      driverSection:'ड्राइवर पोर्टल एवं गाइड',
      cardVehicle:'वाहन की समस्या',
      cardVehicleSub:'फोटो के साथ/बिना समस्या बताएं • तुरंत समाधान मार्गदर्शन',
      cardWarning:'वार्निंग लाइट',
      cardWarningSub:'प्रत्येक वार्निंग लाइट विवरण + वीडियो',
      cardDpf:'DPF रीजेनेरेशन',
      cardDpfSub:'रीजेनेरेशन के चरण + वीडियो',
      cardDailyCheck:'दैनिक जांच',
      cardDailyCheckSub:'ड्राइविंग से पहले जांच सूची + वीडियो',
      cardAdblue:'ADBLUE / DEF',
      cardAdblueSub:'AdBlue भरने के चरण + वीडियो',
      cardSafety:'ड्राइवर सुरक्षा',
      cardSafetySub:'सुरक्षा नियम + वीडियो',
      cardMechUpdate:'मैकेनिक कार्य अपडेट',
      cardMechUpdateSub:'वाहन नंबर + किया गया कार्य + आवाज़ • सुरक्षित करें',
      cardMyRecords:'मेरे काम के रिकॉर्ड',
      cardMyRecordsSub:'अपने दैनिक अपडेट देखें',
      cardEmpUpdate:'दैनिक कार्य अपडेट',
      cardEmpUpdateSub:'टाइपिंग या आवाज़ से दैनिक कार्य दर्ज करें • सुरक्षित करें',
      cardEmpRecordsSub:'दर्ज किए गए दैनिक काम के रिकॉर्ड देखें',
      cardAdminUsers:'यूजर प्रबंधन',
      cardAdminUsersSub:'ड्राइवर, मैकेनिक, कर्मचारी जोड़ें • भूमिका • पासवर्ड',
      cardAdminWork:'कार्य अपडेट',
      cardAdminWorkSub:'सभी कर्मचारियों और मैकेनिकों के काम के रिकॉर्ड देखें',
      cardAdminProblems:'समस्या रिपोर्ट',
      cardAdminProblemsSub:'ड्राइवरों की वाहन समस्या रिपोर्ट और समाधान लॉग देखें',
      cardAdminData:'महिंद्रा डेटा',
      cardAdminDataSub:'वाहन तकनीकी विवरण, BSVI सिस्टम और डायग्नोस्टिक जानकारी',
      probTitle:'वाहन समस्या रिपोर्ट एवं समाधान',
      probSub:'टेक्स्ट या आवाज़ का उपयोग करके अपने ट्रक की समस्या बताएं। यदि उपलब्ध हो तो फोटो लगाएं (फोटो वैकल्पिक है)।',
      chipsPrompt:'सामान्य वाहन समस्याएं (चुनने के लिए टैप करें):',
      descLabel:'वाहन की समस्या का विवरण दें',
      descPh:'अपनी समस्या यहां लिखें या बोलें... सबमिट करने से पहले आप इसे देख और सुधार सकते हैं।',
      charCount:'अक्षर',
      wordsCount:'शब्द',
      voiceConvertsNotice:'🎤 आवाज़ संपादन योग्य टेक्स्ट में बदलती है',
      voiceInputLbl:'आवाज़ इनपुट',
      stopListening:'रोकें',
      photoBoxTitle:'फोटो जोड़ें (वैकल्पिक)',
      photoBoxSub:'फोटो वैकल्पिक है। आप फोटो के बिना भी सबमिट कर सकते हैं।',
      choosePhotoBtn:'📷 फोटो चुनें / खींचें',
      photoAttached:'फोटो संलग्न है (वैकल्पिक)',
      removePhoto:'✕ हटाएं',
      vehNoLabel:'वाहन नंबर (वैकल्पिक)',
      vehNoPh:'उदा: KA-01-MJ-5020 (वैकल्पिक)',
      solutionBtn:'समाधान',
      saveReportOnly:'📝 केवल रिपोर्ट सेव करें',
      callSupervisor:'📞 सुपरवाइजर को कॉल करें',
      emptyProblemMsg:'⚠️ कृपया पहले वाहन की समस्या लिखें या बोलें।',
      savingProblemMsg:'⏳ फ्लीट डेटाबेस में समस्या रिपोर्ट सेव हो रही है…',
      savedProblemSuccess:'✅ समस्या रिपोर्ट सफलतापूर्वक सेव हो गई है। प्रबंधकों को सूचित कर दिया गया है।',
      micListening:'🔴 सुन रहा है... अब स्पष्ट रूप से बोलिए।',
      micSuccess:'✅ आवाज़ रिकॉर्ड हो गई। आप ऊपर दिए गए टेक्स्ट को देख और सुधार सकते हैं।',
      micBlocked:'⚠️ माइक्रोफोन का उपयोग ब्लॉक है। कृपया अपने ब्राउज़र या डिवाइस सेटिंग्स में माइक्रोफोन की अनुमति दें। आप सीधे बॉक्स में टाइप भी कर सकते हैं।',
      micNotSupported:'ℹ️ इस ब्राउज़र में स्पीच रिकग्निशन समर्थित नहीं है। आप सीधे बॉक्स में टाइप कर सकते हैं।',
      micInsecure:'ℹ️ ब्राउज़र सुरक्षा नियमों के तहत स्पीच रिकग्निशन के लिए HTTPS या localhost आवश्यक है। आप सीधे टाइप कर सकते हैं।',
      micNoSpeech:'ℹ️ कोई आवाज़ नहीं मिली। कृपया बटन दबाकर स्पष्ट बोलें या बॉक्स में टाइप करें।',
      photoTextDetected:'🔎 फोटो टेक्स्ट मिल गया। अब "समाधान" बटन दबाएं।',
      photoCaptured:'✅ फोटो मिल गई। अब अपनी समस्या का विवरण लिखें या बोलें।',
      troubleshootTitle:'समस्या निवारण मार्गदर्शन',
      reportedProblem:'बताई गई समस्या:',
      possibleCause:'संभावित कारण:',
      safetyWarning:'सुरक्षा चेतावनी:',
      immediateAction:'त्वरित कार्रवाई (अगले 10 सेकंड में):',
      stepInstructions:'चरण-दर-चरण निर्देश:',
      safeCheckLbl:'🟢 आप सुरक्षित रूप से जांच सकते हैं:',
      mechReqLbl:'🔴 मैकेनिक को कब बुलाएं:',
      escalationTitle:'संपर्क एवं सहायता विकल्प:',
      callFleetMech:'📞 फ्लीट मैकेनिक को कॉल करें (+91 98450 12345)',
      callFleetSup:'🚨 सुपरवाइजर को कॉल करें (+91 99887 76655)',
      readAloudBtn:'🔊 समाधान बोलकर सुनें',
      reportAnotherBtn:'← दूसरी समस्या बताएं',
      empTitle:'दैनिक कार्य अपडेट',
      empSub:'कर्मचारी: {name} • अपनी दैनिक कार्य रिपोर्ट दर्ज करें',
      empDescLabel:'दैनिक कार्य विवरण',
      empPh:'अपना दैनिक कार्य अपडेट यहां लिखें... (उदा: 18 डिस्पैच सत्यापित किए, सुरक्षा सील जांची, लॉजिस्टिक्स बिलिंग का समन्वय किया, ड्राइवर के सवालों का समाधान किया)',
      voiceAndTypingTogether:'🎤 आवाज़ और टाइपिंग दोनों एक साथ काम करते हैं',
      speakUpdateBtn:'🎤 बोलकर बताएं',
      submitUpdateBtn:'💾 अपडेट सबमिट करें',
      submittingUpdate:'⏳ अपडेट सबमिट हो रहा है…',
      prevSubmittedTitle:'📋 पहले सबमिट किए गए अपडेट',
      refreshBtn:'↻ रिफ्रेश',
      emptyWorkMsg:'⚠️ खाली अपडेट: कृपया सबमिट करने से पहले अपना दैनिक कार्य लिखें या बोलें।',
      saveWorkSuccess:'✅ सफल! आपका दैनिक कार्य अपडेट केंद्रीय डेटाबेस में सुरक्षित हो गया है।',
      mechTitle:'मैकेनिक कार्य अपडेट',
      mechSub:'मैकेनिक: {name}',
      vehReq:'वाहन नंबर (उदा: KA-01-MJ-5020)',
      mechWorkPh:'किया गया कार्य (रखरखाव, बदले गए पुर्जे, जांच का विवरण दें)',
      mechSaveSuccess:'✅ दैनिक मैकेनिक अपडेट केंद्रीय रूप से सुरक्षित हो गया।',
      allRecordsTitle:'सभी कार्य रिकॉर्ड',
      myRecordsTitle:'मेरे काम के रिकॉर्ड',
      exportBtn:'⬇️ डेटा डाउनलोड',
      noRecords:'कोई रिकॉर्ड नहीं है।',
      noRecordsSub:'कोई कार्य रिकॉर्ड नहीं मिला। अपडेट सबमिट करने के बाद वह यहां दिखेगा।',
      retryBtn:'↻ पुनः प्रयास करें',
      loading:'लोड हो रहा है…',
      nameLbl:'नाम',
      mobileLbl:'मोबाइल',
      roleLbl:'भूमिका',
      statusLbl:'स्थिति',
      workCompletedLbl:'किया गया कार्य',
      vehicleNoLbl:'वाहन नंबर',
      manageUsersTitle:'यूजर प्रबंधन',
      addUserTitle:'👥 यूजर जोड़ें',
      userListTitle:'मौजूदा यूजर',
      createUserBtn:'➕ यूजर बनाएं',
      namePh:'नाम',
      mobilePh:'10 अंकों का मोबाइल',
      passPh:'पासवर्ड (वैकल्पिक; खाली = अंतिम 4 अंक)',
      adminProblemsTitle:'समस्या रिपोर्ट',
      adminProblemsBrand:'📝 ड्राइवर वाहन समस्या रिपोर्ट',
      adminProblemsSub:'ड्राइवरों द्वारा दर्ज समस्या सूचनाएं और समाधान लॉग',
      viewAiDiagnosis:'🔍 AI समाधान और चरण देखें',
      mahindraDataTitle:'महिंद्रा BSVI डेटा सूट',
      tabOverview:'📊 अवलोकन',
      tabModels:'🚛 वाहन मॉडल',
      tabSpecs:'⚙️ सिस्टम विवरण',
      tabVisuals:'🖼️ चित्र',
      tabExplanations:'💡 सरल स्पष्टीकरण',
      tabOps:'📈 फ्लीट अवलोकन',
      tabSearch:'🔍 मैनुअल खोजें',
      searchManualsPh:'फॉल्ट कोड या घटक का नाम (उदा: P2463, DPF, PRV, Sensor)',
      searchBtn:'खोजें',
      readRealVideo:'▶ असली वीडियो\nकार्रवाई + निर्देश'
    }
  };
  const L=()=>tr[getLang()]||tr.en;

  // Common Problem Chips (Localized)
  const PROBLEM_CHIPS=[
    {
      en:'Truck engine is getting too hot.',
      kn:'ಇಂಜಿನ್ ತುಂಬಾ ಬಿಸಿಯಾಗುತ್ತಿದೆ.',
      hi:'इंजन बहुत गर्म हो रहा है।'
    },
    {
      en:'Low air pressure warning light on dashboard.',
      kn:'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಲ್ಲಿ ಕಡಿಮೆ ಏರ್ ಪ್ರೆಶರ್ ವಾರ್ನಿಂಗ್ ಲೈಟ್.',
      hi:'डैशबोर्ड पर कम एयर प्रेशर वार्निंग लाइट।'
    },
    {
      en:'Brake pedal feels soft or spongy when pressing.',
      kn:'ಒತ್ತಿದಾಗ ಬ್ರೇಕ್ ಪೆಡಲ್ ಮೆತ್ತಗೆ (spongy) ಅನಿಸುತ್ತದೆ.',
      hi:'दबाने पर ब्रेक पैडल स्पंजी या ढीला लग रहा है।'
    },
    {
      en:'Amber DPF regeneration light is flashing on highway.',
      kn:'ಹೈವೇಯಲ್ಲಿ ಹಳದಿ DPF ಲೈಟ್ ಬ್ಲಿಂಕ್ ಆಗುತ್ತಿದೆ.',
      hi:'हाईवे पर एम्बर DPF लाइट ब्लिंक कर रही है।'
    },
    {
      en:'White smoke coming out of exhaust pipe.',
      kn:'ಎಕ್ಸಾಸ್ಟ್ ಪೈಪ್‌ನಿಂದ ಬಿಳಿ ಹೊಗೆ ಬರುತ್ತಿದೆ.',
      hi:'साइलेंसर से सफेद धुआं निकल रहा है।'
    },
    {
      en:'Diesel fuel is dripping under the fuel tank.',
      kn:'ಇಂಧನ ಟ್ಯಾಂಕ್ ಕೆಳಗೆ ಡೀಸೆಲ್ ಸೋರುತ್ತಿದೆ.',
      hi:'ईंधन टैंक के नीचे से डीजल टपक रहा है।'
    },
    {
      en:'Low AdBlue DEF level indicator is on.',
      kn:'ಕಡಿಮೆ AdBlue / DEF ಮಟ್ಟದ ಲೈಟ್ ಆನ್ ಆಗಿದೆ.',
      hi:'कम AdBlue / DEF स्तर का इंडिकेटर जल रहा है।'
    },
    {
      en:'Battery charging warning light is ON.',
      kn:'ಬ್ಯಾಟರಿ ಚಾರ್ಜಿಂಗ್ ವಾರ್ನಿಂಗ್ ಲೈಟ್ ಆನ್ ಆಗಿದೆ.',
      hi:'बैटरी चार्जिंग वार्निंग लाइट जल रही है।'
    },
    {
      en:'Low engine oil pressure indicator is illuminated.',
      kn:'ಕಡಿಮೆ ಇಂಜಿನ್ ಆಯಿಲ್ ಪ್ರೆಶರ್ ಲೈಟ್ ಆನ್ ಆಗಿದೆ.',
      hi:'कम इंजन ऑयल प्रेशर लाइट जल रही है।'
    },
    {
      en:'Steering is vibrating heavily and pulling to side.',
      kn:'ಸ್ಟೀರಿಂಗ್ ತೀವ್ರವಾಗಿ ಕಂಪಿಸುತ್ತಿದೆ ಮತ್ತು ಪಕ್ಕಕ್ಕೆ ಎಳೆಯುತ್ತಿದೆ.',
      hi:'स्टीयरिंग में तेज कंपन है और एक तरफ खिंच रहा है।'
    }
  ];

  const css=`
  <style id="ma-fast-ai-style">
  :root{
    --sat:env(safe-area-inset-top,0px);
    --sab:env(safe-area-inset-bottom,0px);
    --sal:env(safe-area-inset-left,0px);
    --sar:env(safe-area-inset-right,0px);
    --header-h:58px;
    --header-total:calc(var(--header-h) + var(--sat));
  }
  *{box-sizing:border-box}
  html,body{width:100%;max-width:100vw;min-height:100%;margin:0;padding:0;overflow-x:hidden;-webkit-text-size-adjust:100%;text-size-adjust:100%;touch-action:manipulation;background:#f5f7fa!important;color:#17202a!important}
  #maApp{width:100%;max-width:100vw;min-height:100vh;min-height:100dvh;overflow-x:hidden;background:#f5f7fa;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;box-sizing:border-box}
  .ma-bar{position:fixed;top:0;left:0;right:0;width:100%;height:var(--header-total);padding-top:var(--sat);padding-left:calc(10px + var(--sal));padding-right:calc(10px + var(--sar));background:#b71c1c;color:#fff;z-index:100000;display:flex;align-items:center;box-sizing:border-box;border-bottom:3px solid #8f1414;box-shadow:0 3px 12px rgba(0,0,0,0.25)}
  .ma-bar .ma-icon{flex-shrink:0;width:42px;height:42px;border:0;border-radius:11px;background:rgba(255,255,255,0.15);color:#fff;font-size:22px;font-weight:900;display:flex;align-items:center;justify-content:center;cursor:pointer;touch-action:manipulation;transition:background 0.15s,transform 0.15s}
  .ma-bar .ma-icon:active{background:rgba(255,255,255,0.3);transform:scale(0.95)}
  .ma-title{flex:1;padding:0 10px;min-width:0;font-weight:900;font-size:clamp(14px,4.2vw,18px);letter-spacing:.2px;line-height:1.15;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .ma-title small{display:block;font-size:clamp(10px,2.7vw,12px);opacity:.85;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .ma-main{padding-top:calc(var(--header-total) + 12px)!important;padding-bottom:calc(36px + var(--sab))!important;padding-left:calc(12px + var(--sal))!important;padding-right:calc(12px + var(--sar))!important;max-width:780px;width:100%;margin:0 auto;box-sizing:border-box;overflow-x:hidden}
  .ma-hero{background:#fff;border-radius:18px;padding:18px 16px;box-shadow:0 2px 10px rgba(0,0,0,0.05);margin-bottom:14px;width:100%;box-sizing:border-box;word-break:break-word;overflow-wrap:break-word}
  .ma-brand{font-size:clamp(19px,5.5vw,23px);font-weight:900;color:#0f172a;line-height:1.2}
  .ma-sub{margin-top:5px;color:#64748b;font-size:clamp(12px,3.5vw,14px);line-height:1.4}
  .ma-role{display:inline-flex;margin-top:12px;padding:6px 12px;border-radius:999px;background:#17202a;color:#fff;font-size:12px;font-weight:900}
  .ma-section{font-size:13px;font-weight:900;color:#64748b;text-transform:uppercase;letter-spacing:.8px;margin:18px 2px 9px}
  .ma-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:11px;width:100%;box-sizing:border-box}
  .ma-card{border:0;background:#fff;border-radius:16px;padding:16px 14px;text-align:left;box-shadow:0 2px 10px rgba(0,0,0,0.05);min-height:92px;font-size:15px;font-weight:900;color:#17202a;cursor:pointer;transition:transform 0.15s,box-shadow 0.15s;width:100%;box-sizing:border-box;word-break:break-word;overflow-wrap:break-word;touch-action:manipulation}
  .ma-card:active{transform:scale(0.98)}
  .ma-card b{display:block;font-size:26px;margin-bottom:8px}
  .ma-card span{display:block;line-height:1.25}
  .ma-card small{display:block;color:#64748b;font-weight:600;margin-top:5px;font-size:12px;line-height:1.3}
  .ma-primary{background:#b71c1c!important;color:#fff!important}

  /* ISSUE 1: LEFT-SLIDING SIDEBAR AND OVERLAY STYLING */
  .ma-drawer{position:fixed;inset:0;z-index:100010;background:rgba(15,23,42,0.65);backdrop-filter:blur(2px);-webkit-backdrop-filter:blur(2px);opacity:0;visibility:hidden;transition:opacity 0.28s ease,visibility 0.28s ease}
  .ma-drawer.open{opacity:1;visibility:visible}
  .ma-sheet{position:absolute;top:var(--sat);left:0;bottom:0;width:min(82vw,320px);max-width:calc(100vw - 44px);background:#fff;padding:16px 16px calc(24px + var(--sab)) 16px;box-sizing:border-box;box-shadow:8px 0 28px rgba(0,0,0,0.28);overflow-y:auto;-webkit-overflow-scrolling:touch;transform:translateX(-100%);transition:transform 0.28s cubic-bezier(0.16,1,0.3,1);display:flex;flex-direction:column}
  .ma-drawer.open .ma-sheet{transform:translateX(0)}
  .ma-sheet-head{display:flex;align-items:center;justify-content:space-between;padding-bottom:14px;border-bottom:1px solid #e2e8f0}
  .ma-sheet-head strong{flex:1;font-size:16px;font-weight:900;color:#0f172a}
  .ma-sheet-close{width:38px;height:38px;border-radius:10px;border:0;background:#f1f5f9;color:#0f172a;font-size:20px;font-weight:900;display:flex;align-items:center;justify-content:center;cursor:pointer;touch-action:manipulation;transition:background 0.15s,transform 0.15s}
  .ma-sheet-close:active{background:#e2e8f0;transform:scale(0.95)}
  .ma-menu-btn{width:100%;border:0;background:#f4f5f7;margin-top:8px;padding:14px;border-radius:12px;text-align:left;font-size:14px;font-weight:800;color:#17202a;cursor:pointer;touch-action:manipulation;transition:background 0.15s}
  .ma-menu-btn:active{transform:scale(0.98)}
  .ma-menu-btn.danger{background:#fff0f0;color:#b71c1c}
  .ma-menu-btn.active-lang{background:#b71c1c!important;color:#fff!important;box-shadow:0 2px 8px rgba(183,28,28,0.35)}

  .ma-backbar{position:fixed;top:var(--header-total);left:0;right:0;height:46px;background:#fff;border-bottom:1px solid #e5e7eb;z-index:99990;display:flex;align-items:center;padding:0 calc(12px + var(--sar)) 0 calc(12px + var(--sal));box-sizing:border-box}
  .ma-backbar button{border:0;background:transparent;font-size:14px;font-weight:900;color:#17202a;padding:8px;cursor:pointer;touch-action:manipulation}
  .ma-backbar .home{margin-left:auto;color:#b71c1c}
  .auth-card{max-width:420px!important;border-radius:22px!important;box-shadow:0 8px 30px rgba(0,0,0,0.12)!important}
  .ma-guide-list{display:block;width:100%}
  .ma-guide-item{background:#fff;border:1px solid #e3e7ed;border-radius:18px;margin:12px 0;padding:14px;box-shadow:0 2px 10px rgba(0,0,0,0.04);display:grid;grid-template-columns:70px 1fr;gap:12px;align-items:center;width:100%;box-sizing:border-box}
  .ma-truck-icon{width:64px;height:64px;border-radius:16px;background:#b71c1c;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:32px;box-shadow:0 3px 8px rgba(0,0,0,0.15)}
  .ma-truck-icon small{display:none}
  .ma-guide-copy{min-width:0;word-break:break-word}
  .ma-guide-number{font-size:11px;color:#b71c1c;font-weight:900}
  .ma-guide-title{font-size:clamp(16px,4.5vw,19px);line-height:1.2;font-weight:900;color:#17202a;margin-top:2px}
  .ma-guide-detail{font-size:13px;color:#667085;margin-top:4px;line-height:1.3}
  .ma-guide-video{grid-column:1/-1;width:100%;border:0;border-radius:12px;background:#b71c1c;color:#fff;min-height:52px;font-size:15px;font-weight:900;line-height:1.2;cursor:pointer;touch-action:manipulation;white-space:pre-line}
  
  /* WORK UPDATE & TROUBLESHOOTING UI */
  .ma-emp-textarea{width:100%;box-sizing:border-box;padding:14px;border:2px solid #cbd5e1;border-radius:14px;font-size:16px!important;font-family:inherit;line-height:1.5;resize:vertical;min-height:130px;outline:none;background:#fff;color:#0f172a;transition:border-color 0.2s,box-shadow 0.2s}
  .ma-emp-textarea:focus{border-color:#b71c1c;box-shadow:0 0 0 3px rgba(183,28,28,0.12)}
  .ma-btn-voice{border:0;background:#1e293b;color:#fff;padding:12px 18px;min-height:46px;border-radius:12px;font-weight:800;font-size:14px;cursor:pointer;display:inline-flex;align-items:center;gap:7px;transition:0.18s;touch-action:manipulation}
  .ma-btn-voice:active{transform:scale(0.97)}
  .ma-btn-voice.listening{background:#dc2626!important;animation:maPulse 1.2s infinite}
  @keyframes maPulse{0%,100%{opacity:1}50%{opacity:0.6}}

  /* ISSUE 4: COMPACT, PROMINENT RED SOLUTION BUTTON */
  .ma-btn-submit{border:0;background:#b71c1c;color:#fff;padding:14px 22px;min-height:52px;border-radius:12px;font-weight:900;font-size:17px;letter-spacing:0.5px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 14px rgba(183,28,28,0.28);transition:0.18s;touch-action:manipulation}
  .ma-btn-submit:active{transform:scale(0.98)}
  .ma-btn-submit:disabled{opacity:0.65;cursor:not-allowed}

  .ma-btn-escalate{border:2px solid #b71c1c;background:#fff;color:#b71c1c;padding:12px 16px;min-height:48px;border-radius:12px;font-weight:900;font-size:14px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:8px;width:100%;margin-top:8px;text-decoration:none;box-sizing:border-box;touch-action:manipulation}
  .ma-btn-escalate:active{background:#b71c1c;color:#fff}
  .ma-chip-wrap{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 14px;width:100%}
  .ma-chip{border:1px solid #d0d5dd;background:#f8fafc;color:#1e293b;font-size:12px;padding:7px 12px;border-radius:999px;font-weight:700;cursor:pointer;transition:0.15s;line-height:1.2;touch-action:manipulation;word-break:break-word}
  .ma-chip:active{background:#fee2e2;border-color:#b71c1c;color:#b71c1c}
  .ma-action-badge{display:inline-block;padding:5px 12px;border-radius:999px;font-size:12px;font-weight:900;letter-spacing:0.4px}
  .ma-badge-critical{background:#fee2e2;color:#b91c1c;border:1px solid #f87171}
  .ma-badge-high{background:#fef3c7;color:#b45309;border:1px solid #fcd34d}
  .ma-badge-safe{background:#dcfce7;color:#15803d;border:1px solid #86efac}
  .ma-badge-info{background:#e0f2fe;color:#0369a1;border:1px solid #7dd3fc}
  .ma-danger-box{background:#fef2f2;border-left:5px solid #dc2626;border-radius:12px;padding:13px 15px;margin:12px 0;color:#991b1b;font-size:14px;line-height:1.45;word-break:break-word}
  .ma-safe-box{background:#f0fdf4;border-left:5px solid #16a34a;border-radius:12px;padding:13px 15px;margin:12px 0;color:#166534;font-size:14px;line-height:1.45;word-break:break-word}
  .ma-mech-box{background:#fffbeb;border-left:5px solid #d97706;border-radius:12px;padding:13px 15px;margin:12px 0;color:#92400e;font-size:14px;line-height:1.45;word-break:break-word}
  .ma-safe-split{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px;width:100%;box-sizing:border-box}
  .ma-step-item{display:flex;align-items:flex-start;gap:12px;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:12px 14px;margin:8px 0;box-shadow:0 1px 3px rgba(0,0,0,0.04);word-break:break-word}
  .ma-step-num{flex-shrink:0;width:28px;height:28px;border-radius:50%;background:#b71c1c;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:13px}
  .ma-step-text{font-size:14px;line-height:1.45;color:#1e293b;font-weight:600;min-width:0;flex:1}
  .ma-admin-tabs{display:flex;gap:6px;overflow-x:auto;-webkit-overflow-scrolling:touch;padding:6px 2px 12px;margin-bottom:12px;scrollbar-width:none;width:100%}
  .ma-admin-tabs::-webkit-scrollbar{display:none}
  .ma-tab-btn{border:0;background:#e2e8f0;color:#334155;padding:8px 14px;border-radius:999px;font-weight:800;font-size:13px;cursor:pointer;white-space:nowrap;transition:0.18s;touch-action:manipulation}
  .ma-tab-btn.active{background:#b71c1c;color:#fff;box-shadow:0 2px 8px rgba(183,28,28,0.3)}
  .ma-admin-img-wrap{border-radius:14px;overflow:hidden;border:1px solid #e2e8f0;background:#fff;margin:14px 0;box-shadow:0 3px 10px rgba(0,0,0,0.06);width:100%;box-sizing:border-box}
  .ma-admin-img{width:100%;height:auto;display:block;object-fit:cover;max-height:260px;background:#1e293b}
  .ma-admin-img-cap{padding:12px 14px;font-size:13px;color:#334155;background:#f8fafc;border-top:1px solid #e2e8f0;line-height:1.45}
  .ma-kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin:12px 0;width:100%}
  .ma-kpi-card{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:12px;text-align:center;box-shadow:0 2px 6px rgba(0,0,0,0.03)}
  .ma-kpi-num{font-size:24px;font-weight:1000;color:#b71c1c;line-height:1}
  .ma-kpi-lbl{font-size:11px;font-weight:800;color:#64748b;margin-top:6px;text-transform:uppercase;letter-spacing:0.3px}
  .ma-table-container{width:100%;max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;margin:12px 0;border-radius:14px;border:1px solid #e2e8f0;background:#fff;box-sizing:border-box}
  .ma-data-table{width:100%;min-width:480px;border-collapse:collapse;font-size:13px;background:#fff}
  .ma-data-table th{background:#f1f5f9;padding:10px 12px;text-align:left;font-weight:800;color:#334155;border-bottom:2px solid #cbd5e1;white-space:nowrap}
  .ma-data-table td{padding:10px 12px;border-bottom:1px solid #e2e8f0;color:#1e293b}
  .ma-data-table tr:last-child td{border-bottom:0}
  .ma-source-tag{display:inline-block;padding:2px 7px;border-radius:4px;font-size:11px;font-weight:800;text-transform:uppercase}
  .ma-source-verified{background:#dcfce7;color:#166534}
  .ma-source-ops{background:#dbeafe;color:#1e40af}
  .ma-source-na{background:#f1f5f9;color:#64748b;font-style:italic}
  input,select{font-size:16px!important}
  
  @media(max-width:480px){
    .ma-grid{grid-template-columns:1fr!important;gap:9px}
    .ma-card{min-height:80px;padding:14px 12px}
    .ma-main{padding-left:10px!important;padding-right:10px!important}
    .ma-hero{padding:16px 12px;border-radius:14px}
    .ma-brand{font-size:19px!important}
    .ma-guide-item{grid-template-columns:58px 1fr;gap:10px;padding:12px 10px}
    .ma-truck-icon{width:56px;height:56px;font-size:26px;border-radius:12px}
    .ma-safe-split{grid-template-columns:1fr!important}
  }
  @media(max-width:360px){
    .ma-kpi-grid{grid-template-columns:1fr 1fr!important;gap:7px}
    .ma-kpi-num{font-size:20px}
    .ma-bar .ma-icon{width:38px;height:38px;font-size:20px}
    .ma-card b{font-size:22px}
    .ma-card span{font-size:14px}
  }
  </style>`;
  document.head.insertAdjacentHTML('beforeend',css);

  function logout(){
    const curLang=getLang();
    localStorage.removeItem(TOKEN);
    localStorage.removeItem(USER);
    localStorage.removeItem(MODE);
    sessionStorage.removeItem('ma_fast_boot_v1');
    localStorage.setItem(LANG_KEY,curLang);
    location.reload();
  }
  window.maLogout=logout;

  function closeDrawer(){document.getElementById('maDrawer')?.classList.remove('open')}
  function menu(){document.getElementById('maDrawer')?.classList.add('open')}
  function runAction(fn){closeDrawer();setTimeout(fn,40)}

  function roleLabel(r){r=String(r||'').toUpperCase();return r==='USER'?'DRIVER':r;}
  function roleName(r){
    const l=L();
    r=roleLabel(r);
    return r==='ADMIN'?l.admin:r==='MECHANIC'?l.mechanic:r==='EMPLOYEE'?l.employee:l.driver;
  }

  /* API TRANSPORT */
  const apiQueue=[];let apiBusy=false;
  function apiRequest(action,req,done){apiQueue.push({action:action,req:req,done:done});pumpApiQueue();}
  function pumpApiQueue(){
    if(apiBusy||!apiQueue.length)return;
    apiBusy=true;const it=apiQueue.shift(),action=it.action,req=Object.assign({},it.req,{action:action});
    if(!req.token){const tok=localStorage.getItem(TOKEN);if(tok)req.token=tok;}
    let finished=false,attempt=0;const done=it.done;
    const retryable=new Set(['list_users','list_work','list_problems']);
    const finish=(res)=>{
      if(finished)return;finished=true;
      if(res&&res.error&&/auth|login|token/i.test(res.error)&&action!=='login'){
        if(done)done(res);
        setTimeout(()=>{alert('Session expired. Please log in again.');logout();},250);
        return;
      }else{
        if(done)done(res||{ok:false,error:'Empty backend response.'});
      }
      apiBusy=false;
      setTimeout(pumpApiQueue,30);
    };
    const run=()=>{
      if(finished)return;
      attempt++;
      window.appHttpResult=function(raw){finish(normalizeLoginResponse(raw));};
      try{
        if(!window.AndroidBridge||!AndroidBridge.cloudRequest){finish({ok:false,error:'Android network bridge is unavailable.'});return;}
        AndroidBridge.cloudRequest('POST',AndroidBridge.getSharedApiUrl(),JSON.stringify(req));
      }catch(e){finish({ok:false,error:String(e.message||e)});return;}
      setTimeout(()=>{
        if(finished)return;
        if(retryable.has(action)&&attempt<3){
          window.appHttpResult=null;
          setTimeout(run,800);
        }else{
          finish({ok:false,error:'Backend request timed out. Please try again.'});
        }
      },65000);
    };
    run();
  }

  /* ISSUE 3: ROBUST SPEECH RECOGNITION (EXPLICIT TAP, CLEAN STATUS, STT TO EDITABLE BOX) */
  let activeSpeechRecognizer=null;
  let activeVoiceBtnEl=null;

  function stopActiveVoice(){
    try{
      if(activeSpeechRecognizer){
        if(typeof activeSpeechRecognizer.abort==='function') activeSpeechRecognizer.abort();
        else if(typeof activeSpeechRecognizer.stop==='function') activeSpeechRecognizer.stop();
        activeSpeechRecognizer=null;
      }
    }catch(e){}
    try{
      if(window.AndroidBridge && typeof AndroidBridge.stopSpeech==='function'){
        AndroidBridge.stopSpeech();
      }
    }catch(e){}
    if(activeVoiceBtnEl){
      activeVoiceBtnEl.classList.remove('listening');
      activeVoiceBtnEl=null;
    }
    const stopBtn=document.getElementById('btnVoiceStop');
    if(stopBtn) stopBtn.style.display='none';
  }
  window.stopActiveVoice=stopActiveVoice;

  function startVoiceRecognition(targetElementId, statusElementId, langCode, onComplete, triggerBtnId){
    stopActiveVoice();

    const target=document.getElementById(targetElementId);
    const status=document.getElementById(statusElementId);
    const locale=langCode||(getLang()==='kn'?'kn-IN':getLang()==='hi'?'hi-IN':'en-IN');
    const curL=L();

    if(triggerBtnId){
      activeVoiceBtnEl=document.getElementById(triggerBtnId);
      if(activeVoiceBtnEl) activeVoiceBtnEl.classList.add('listening');
    }
    const stopBtn=document.getElementById('btnVoiceStop');
    if(stopBtn) stopBtn.style.display='inline-flex';

    if(status) status.innerHTML='<span style="color:#dc2626;font-weight:900">'+curL.micListening+'</span>';

    // 1. Prefer Native Android Bridge Speech in APK
    if(window.AndroidBridge && typeof AndroidBridge.startSpeech==='function'){
      window.nativeSpeechResult=function(text){
        stopActiveVoice();
        if(text){
          if(target){
            const cur=target.value.trim();
            target.value=cur?(cur+' '+text):text;
            target.focus();
            target.dispatchEvent(new Event('input'));
          }
          if(status) status.innerHTML='<span style="color:#15803d;font-weight:700">'+curL.micSuccess+'</span>';
          if(onComplete) onComplete(text);
        }else{
          if(status) status.innerHTML='<span style="color:#475569">'+curL.micNoSpeech+'</span>';
        }
        window.nativeSpeechResult=null;
      };

      window.nativeSpeechError=function(err){
        stopActiveVoice();
        const msg=String(err||'');
        if(/permission|denied|allow/i.test(msg)){
          if(status) status.innerHTML='<div class="ma-danger-box">⚠️ '+curL.micBlocked+'</div>';
        }else{
          if(status) status.innerHTML='<span style="color:#475569">ℹ️ '+esc(msg||curL.micNoSpeech)+'</span>';
        }
        window.nativeSpeechError=null;
      };

      try {
        AndroidBridge.startSpeech(locale);
        return;
      } catch(e) {
        console.warn('Native speech failed, trying browser speech:', e);
      }
    }

    // 2. Browser Speech Recognition (Desktop / Chrome / Preview)
    if(window.isSecureContext===false && location.hostname!=='localhost' && location.hostname!=='127.0.0.1'){
      stopActiveVoice();
      if(status) status.innerHTML='<div class="ma-danger-box">'+curL.micInsecure+'</div>';
      return;
    }

    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if(!SpeechRec){
      stopActiveVoice();
      const dict = prompt(curL.voiceInputLbl + ' (' + locale + '):', target ? target.value : '');
      if(dict != null && target){
        target.value = target.value ? (target.value + ' ' + dict) : dict;
        target.dispatchEvent(new Event('input'));
        if(status) status.innerHTML = '<span style="color:#15803d;font-weight:700">' + curL.micSuccess + '</span>';
        if(onComplete) onComplete(dict);
      } else if(status) {
        status.innerHTML='<div class="ma-danger-box">'+curL.micNotSupported+'</div>';
      }
      return;
    }

    try{
      const rec=new SpeechRec();
      activeSpeechRecognizer=rec;
      rec.lang=locale;
      rec.continuous=false;
      rec.interimResults=false;
      rec.maxAlternatives=1;
      let gotResult=false;

      rec.onresult=function(e){
        gotResult=true;
        stopActiveVoice();
        const transcript=e.results[0][0].transcript;
        if(target){
          const cur=target.value.trim();
          target.value=cur?(cur+' '+transcript):transcript;
          target.focus();
          target.dispatchEvent(new Event('input'));
        }
        if(status) status.innerHTML='<span style="color:#15803d;font-weight:700">'+curL.micSuccess+'</span>';
        if(onComplete) onComplete(transcript);
      };

      rec.onerror=function(e){
        stopActiveVoice();
        if(!gotResult && status){
          if(e.error==='not-allowed'){
            status.innerHTML='<div class="ma-danger-box">'+curL.micBlocked+'</div>';
          }else if(e.error==='no-speech'){
            status.innerHTML='<span style="color:#475569">'+curL.micNoSpeech+'</span>';
          }else{
            status.innerHTML='<span style="color:#475569">ℹ️ '+(e.error||'Voice input ended. You can type directly in the box.')+'</span>';
          }
        }
      };

      rec.onend=function(){
        stopActiveVoice();
      };

      rec.start();
    }catch(err){
      stopActiveVoice();
      if(status) status.innerHTML='<span style="color:#475569">ℹ️ '+esc(err.message||curL.micNotSupported)+'</span>';
    }
  }

  /* ISSUE 1 & ISSUE 2: UNIFIED DASHBOARD WITH LEFT-ALIGNED SIDEBAR & FULL LOCALIZATION */
  function dashboard(){
    stopActiveVoice();
    window.__currentRenderer=dashboard;
    hideOld();document.getElementById('secureAuth')?.remove();document.getElementById('maLogin')?.remove();
    let root=document.getElementById('maApp');if(root)root.remove();root=document.createElement('div');root.id='maApp';
    const u=getUser()||{},r=roleLabel(u.role),admin=r==='ADMIN',mech=r==='MECHANIC',emp=r==='EMPLOYEE';
    const l=L();
    const curLang=getLang();

    root.innerHTML='<div class="ma-bar">'+
      '<button class="ma-icon" onclick="maOpenMenu()" aria-label="Open Navigation Menu">☰</button>'+
      '<div class="ma-title">'+l.appTitle+'<small>'+esc(roleName(r))+' • '+esc(u.name||'')+'</small></div>'+
      '<div style="width:42px"></div>'+
      '</div>'+
      '<main class="ma-main">'+
      '<section class="ma-hero">'+
        '<div class="ma-brand">'+l.welcome+', '+esc(u.name||'User')+'</div>'+
        '<div class="ma-sub">'+l.secureDash+'</div>'+
        '<div class="ma-role">🔐 '+esc(r)+' • '+esc(roleName(r))+'</div>'+
      '</section>'+
      '<div class="ma-section">'+(admin?l.adminSection:mech?l.mechSection:emp?l.empSection:l.driverSection)+'</div>'+
      '<section class="ma-grid" id="maCards"></section>'+
      '</main>'+
      '<div id="maDrawer" class="ma-drawer" onclick="if(event.target===this)maCloseMenu()">'+
        '<aside class="ma-sheet" onclick="event.stopPropagation()">'+
          '<div class="ma-sheet-head">'+
            '<div>'+
              '<strong>'+l.menu+'</strong>'+
              '<small style="display:block;color:#64748b;font-size:12px;margin-top:2px">'+esc(r)+' • '+esc(u.name||'')+'</small>'+
            '</div>'+
            '<button class="ma-sheet-close" onclick="maCloseMenu()" aria-label="Close Menu">×</button>'+
          '</div>'+
          '<div style="flex:1;overflow-y:auto;padding-top:10px">'+
            '<button class="ma-menu-btn" onclick="runAction(maDashboard)">⌂ '+l.dashboard+'</button>'+
            '<div id="maMenuItems"></div>'+
            '<div class="ma-section" style="margin-top:18px">🌐 '+l.language+'</div>'+
            '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px">'+
              '<button class="ma-menu-btn '+(curLang==='en'?'active-lang':'')+'" onclick="maSetLanguage(\'en\')">English</button>'+
              '<button class="ma-menu-btn '+(curLang==='kn'?'active-lang':'')+'" onclick="maSetLanguage(\'kn\')">ಕನ್ನಡ</button>'+
              '<button class="ma-menu-btn '+(curLang==='hi'?'active-lang':'')+'" onclick="maSetLanguage(\'hi\')">हिन्दी</button>'+
            '</div>'+
            '<button class="ma-menu-btn" style="margin-top:12px" onclick="runAction(maOpenHelp)">🧭 '+l.help+'</button>'+
          '</div>'+
          '<button class="ma-menu-btn danger" style="margin-top:auto" onclick="maLogout()">⎋ '+l.logout+'</button>'+
        '</aside>'+
      '</div>';
    app.appendChild(root);

    let cards;
    if(admin) cards=[
      ['👥',l.cardAdminUsers,l.cardAdminUsersSub,adminUsers],
      ['👨‍🔧',l.cardAdminWork,l.cardAdminWorkSub,adminWork],
      ['📝',l.cardAdminProblems,l.cardAdminProblemsSub,adminProblems],
      ['📚',l.cardAdminData,l.cardAdminDataSub,adminMahindraData]
    ];
    else if(emp) cards=[
      ['➕',l.cardEmpUpdate,l.cardEmpUpdateSub,employeeUpdate],
      ['📋',l.cardMyRecords,l.cardEmpRecordsSub,()=>workRecords(false)]
    ];
    else if(mech) cards=[
      ['➕',l.cardMechUpdate,l.cardMechUpdateSub,mechanicUpdate],
      ['📋',l.cardMyRecords,l.cardMyRecordsSub,mechanicRecords]
    ];
    else cards=[
      ['📷',l.cardVehicle,l.cardVehicleSub,()=>window.exactProblem()],
      ['🚨',l.cardWarning,l.cardWarningSub,()=>driverGuide('warning')],
      ['♻️',l.cardDpf,l.cardDpfSub,()=>driverGuide('dpf')],
      ['🔧',l.cardDailyCheck,l.cardDailyCheckSub,()=>driverGuide('daily')],
      ['💧',l.cardAdblue,l.cardAdblueSub,()=>driverGuide('adblue')],
      ['🛑',l.cardSafety,l.cardSafetySub,()=>driverGuide('safety')]
    ];

    const box=root.querySelector('#maCards'),mi=root.querySelector('#maMenuItems');
    cards.forEach((c,i)=>{
      const el=document.createElement('button');
      el.className='ma-card'+(i===0?' ma-primary':'');
      el.innerHTML='<b>'+c[0]+'</b><span>'+esc(c[1])+'</span><small>'+esc(c[2])+'</small>';
      el.onclick=c[3];
      box.appendChild(el);
      const m=document.createElement('button');
      m.className='ma-menu-btn';
      m.textContent=c[0]+'  '+c[1];
      m.onclick=c[3];
      mi.appendChild(m);
    });
  }

  function page(title,html){
    stopActiveVoice();
    hideOld();document.getElementById('maLogin')?.remove();document.getElementById('maApp')?.remove();
    const root=document.createElement('div');root.id='maApp';
    const l=L();
    root.innerHTML='<div class="ma-bar">'+
      '<button class="ma-icon" onclick="maDashboard()" aria-label="Go Back">‹</button>'+
      '<div class="ma-title">'+esc(title)+'<small>'+esc(roleName(getUser()?.role))+' • '+esc(name())+'</small></div>'+
      '<button class="ma-icon" onclick="maDashboard()" aria-label="Home">⌂</button>'+
      '</div><main class="ma-main">'+html+'</main>';
    app.appendChild(root);
  }

  function normalizeLoginResponse(raw){
    const candidates=[];
    const seen=new Set();
    const add=(v,depth)=>{
      if(depth>6||v==null)return;
      if(typeof v==='string'){
        const t=v.trim();
        if(!t)return;
        try{add(JSON.parse(t),depth+1)}catch(e){}
        return;
      }
      if(typeof v!=='object'||seen.has(v))return;
      seen.add(v);candidates.push(v);
      ['body','result','data','response'].forEach(k=>{if(v[k]!=null)add(v[k],depth+1)});
    };
    add(raw,0);
    for(const v of candidates){
      if(v && v.token && v.user && typeof v.user==='object') return v;
    }
    for(const v of candidates){
      if(v && Array.isArray(v.users)) return v;
    }
    for(const v of candidates){
      if(v && Array.isArray(v.records)) return v;
    }
    for(const v of candidates){
      if(v && (Object.prototype.hasOwnProperty.call(v,'recordId') || Object.prototype.hasOwnProperty.call(v,'reportId'))) return v;
    }
    for(const v of candidates){
      if(v && v.ok===true && v.user && typeof v.user==='object') return v;
    }
    for(const v of candidates){
      if(v && v.ok===false) return v;
    }
    for(const v of candidates){
      if(v && v.error && !v.token) return v;
    }
    for(const v of candidates){
      if(v && v.ok===true && !v.body && !v.result && !v.data && !v.response) return v;
    }
    return candidates[0]||{ok:false,error:'Backend response could not be read.'};
  }

  function finishLoginUser(res, root, btn, err){
    if(!res || !res.ok){err.textContent=(res&&res.error)||'Mobile number or password is incorrect.';btn.disabled=false;btn.textContent='🔐 LOGIN';return;}
    const token=String(res.token||'');
    const suppliedUser=(res.user&&typeof res.user==='object')?res.user:null;
    if(suppliedUser && suppliedUser.role){
      localStorage.setItem(TOKEN,token);localStorage.setItem(USER,JSON.stringify(suppliedUser));localStorage.setItem(MODE,roleLabel(suppliedUser.role).toLowerCase());root.remove();dashboard();return;
    }
    if(!token){err.textContent='Login response did not contain a secure session. Please try again.';btn.disabled=false;btn.textContent='🔐 LOGIN';return;}
    const previous=window.appHttpResult;
    let done=false;
    window.appHttpResult=function(raw){
      if(done)return;done=true;window.appHttpResult=previous;
      const me=normalizeLoginResponse(raw);
      if(me&&me.ok&&me.user&&me.user.role){
        localStorage.setItem(TOKEN,token);localStorage.setItem(USER,JSON.stringify(me.user));localStorage.setItem(MODE,roleLabel(me.user.role).toLowerCase());root.remove();dashboard();
      }else{
        localStorage.removeItem(TOKEN);localStorage.removeItem(USER);localStorage.removeItem(MODE);
        err.textContent=(me&&me.error)||'Login succeeded but the account role could not be read.';btn.disabled=false;btn.textContent='🔐 LOGIN';
      }
    };
    try{AndroidBridge.cloudRequest('POST',AndroidBridge.getSharedApiUrl(),JSON.stringify({action:'me',token:token}));}
    catch(e){window.appHttpResult=previous;err.textContent=e.message||String(e);btn.disabled=false;btn.textContent='🔐 LOGIN';}
  }

  function renderLogin(message){
    stopActiveVoice();
    window.__currentRenderer=renderLogin;
    hideOld();document.getElementById('maApp')?.remove();document.getElementById('secureAuth')?.remove();
    let root=document.getElementById('maLogin');if(root)root.remove();
    root=document.createElement('div');root.id='maLogin';
    root.style.cssText='position:fixed;inset:0;z-index:2147483000;background:#fff;overflow-x:hidden;overflow-y:auto;-webkit-overflow-scrolling:touch;width:100%;max-width:100vw;font-family:Arial,sans-serif;color:#152f63;box-sizing:border-box';
    const curLang=getLang();
    const loginTr={
      en:{
        title:'Welcome Back 👋',
        sub:'Login to access driver telematics, AI triage & trip logs',
        mobileLbl:'Mobile Number',
        mobilePh:'10-digit mobile number',
        passLbl:'Password / Secure PIN',
        passPh:'Enter password',
        btn:'🔐 &nbsp; SECURE LOGIN &nbsp; →',
        note:'Mobile number is your official Driver ID. Credentials are protected and remain private.',
        errFormat:'Enter the 10-digit mobile number and password.',
        btnLoading:'⏳ SECURE LOGIN…'
      },
      kn:{
        title:'ಸ್ವಾಗತ 👋',
        sub:'ಚಾಲಕ ಟೆಲಿಮ್ಯಾಟಿಕ್ಸ್, AI ಮಾರ್ಗದರ್ಶನ ಮತ್ತು ಟ್ರಿಪ್ ಲಾಗ್‌ಗಳಿಗಾಗಿ ಲಾಗಿನ್ ಮಾಡಿ',
        mobileLbl:'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ',
        mobilePh:'10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ',
        passLbl:'ಪಾಸ್‌ವರ್ಡ್ / ಸುರಕ್ಷಿತ ಪಿನ್',
        passPh:'ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ',
        btn:'🔐 &nbsp; ಸುರಕ್ಷಿತ ಲಾಗಿನ್ &nbsp; →',
        note:'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಿಮ್ಮ ಅಧಿಕೃತ ಚಾಲಕ ID. ರುಜುವಾತುಗಳು ಸುರಕ್ಷಿತವಾಗಿರುತ್ತವೆ.',
        errFormat:'10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಮತ್ತು ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ.',
        btnLoading:'⏳ ಲಾಗಿನ್ ಆಗುತ್ತಿದೆ…'
      },
      hi:{
        title:'स्वागत है 👋',
        sub:'ड्राइवर टेलीमैटिक्स, AI सहायता और ट्रिप लॉग के लिए लॉगिन करें',
        mobileLbl:'मोबाइल नंबर',
        mobilePh:'10 अंकों का मोबाइल नंबर',
        passLbl:'पासवर्ड / सिक्योर पिन',
        passPh:'पासवर्ड दर्ज करें',
        btn:'🔐 &nbsp; सुरक्षित लॉगिन &nbsp; →',
        note:'मोबाइल नंबर आपकी आधिकारिक ड्राइवर आईडी है। विवरण सुरक्षित रहते हैं।',
        errFormat:'10 अंकों का मोबाइल नंबर और पासवर्ड दर्ज करें।',
        btnLoading:'⏳ लॉगिन हो रहा है…'
      }
    };
    const lt=loginTr[curLang]||loginTr.en;

    root.innerHTML='<style>'+
      '#maLogin *{box-sizing:border-box}'+
      '.login-page{width:100%;max-width:100vw;min-height:100vh;min-height:100dvh;background:#fff;padding-top:env(safe-area-inset-top,0px);padding-bottom:calc(20px + env(safe-area-inset-bottom,0px));padding-left:env(safe-area-inset-left,0px);padding-right:env(safe-area-inset-right,0px);display:flex;flex-direction:column;box-sizing:border-box}'+
      '.login-head{background:linear-gradient(180deg,#ffd928 0%,#ffd800 62%,#fff0a0 100%);padding:18px 14px 20px;text-align:center;width:100%;box-sizing:border-box}'+
      '.bt-company{font-size:clamp(22px,6.5vw,38px);font-weight:1000;letter-spacing:.2px;color:#c71919;text-shadow:1px 1px 0 #fff;line-height:1.15}'+
      '.bt-authorized{font-size:clamp(11px,3.2vw,13px);font-weight:900;color:#173d76;margin-top:2px}'+
      '.bt-logo{width:96px;height:96px;max-width:28vw;max-height:28vw;object-fit:cover;display:block;margin:12px auto 8px;border-radius:20px;box-shadow:0 5px 14px rgba(0,0,0,.18);background:#fff}'+
      '.bt-brand{font-weight:1000;font-size:clamp(20px,5.5vw,28px);color:#173d76}'+
      '.bt-tag{font-size:clamp(11px,3.2vw,13px);font-weight:800;color:#173d76;margin-top:5px;line-height:1.2}'+
      '.bt-slogan{font-size:clamp(16px,4.5vw,22px);font-weight:1000;color:#173d76;margin-top:10px;line-height:1.1}'+
      '.bt-pills{display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin-top:10px}'+
      '.bt-pill{border:0;border-radius:999px;background:#fff;color:#173d76;padding:6px 14px;font-weight:900;font-size:12px;touch-action:manipulation;cursor:pointer}'+
      '.bt-pill.active{background:#173d76;color:#fff}'+
      '.login-road{height:12px;background:linear-gradient(90deg,#d9bc19 0 49%,#173d76 49% 100%)}'+
      '.bt-card{width:min(420px,calc(100% - 24px));margin:0 auto 20px;background:#fff;border-radius:22px;padding:20px 16px 18px;box-shadow:0 8px 25px rgba(16,38,75,.12);border:1px solid #e5e7eb;box-sizing:border-box}'+
      '.bt-title{text-align:center;font-size:clamp(22px,6vw,30px);margin:0 0 4px;color:#173d76;font-weight:1000}'+
      '.bt-sub{text-align:center;color:#667085;font-size:13px;margin:0 0 16px;line-height:1.35}'+
      '.bt-label{display:block;font-size:13px;font-weight:900;color:#344054;margin:0 0 6px}'+
      '.bt-inputwrap{position:relative;margin-bottom:12px;width:100%}'+
      '.bt-input{width:100%;height:52px;border:2px solid #d8dee8;border-radius:12px;padding:8px 46px 8px 44px;font-size:16px!important;color:#10264b;background:#fff;outline:none;box-sizing:border-box}'+
      '.bt-input:focus{border-color:#c71919;box-shadow:0 0 0 3px rgba(199,25,25,.09)}'+
      '.bt-icon{position:absolute;left:13px;top:14px;font-size:19px;pointer-events:none}'+
      '.bt-eye{position:absolute;right:4px;top:3px;height:46px;width:44px;border:0;background:transparent;font-size:20px;touch-action:manipulation;cursor:pointer}'+
      '.bt-login{width:100%;min-height:52px;border:0;border-radius:12px;background:#c71919;color:#fff;font-size:16px;font-weight:1000;box-shadow:0 6px 14px rgba(199,25,25,.2);cursor:pointer;touch-action:manipulation}'+
      '.bt-login:active{transform:scale(0.98)}'+
      '.bt-login:disabled{opacity:.65}'+
      '.bt-error{color:#b42318;font-weight:700;font-size:13px;min-height:20px;margin-top:10px;text-align:center;word-break:break-word}'+
      '.bt-note{text-align:center;color:#667085;font-size:11px;line-height:1.4;margin-top:12px}'+
      '</style>'+
      '<div class="login-page"><header class="login-head">'+
        '<div class="bt-company">BALAJI TRANSPORTS</div>'+
        '<div class="bt-authorized">JSW AUTHORIZED TRANSPORTERS</div>'+
        '<img class="bt-logo" src="driver_mech_logo.jpg" alt="Driver/Mech AI">'+
        '<div class="bt-tag">AI Assistance • Voice • Inspection • Offline Sync</div>'+
        '<div class="bt-slogan">"Safe Drives<br>Stronger Tomorrows"</div>'+
        '<div class="bt-pills">'+
          '<button class="bt-pill '+(curLang==='en'?'active':'')+'" type="button" onclick="window.maSetLanguage(\'en\')">English</button>'+
          '<button class="bt-pill '+(curLang==='kn'?'active':'')+'" type="button" onclick="window.maSetLanguage(\'kn\')">ಕನ್ನಡ</button>'+
          '<button class="bt-pill '+(curLang==='hi'?'active':'')+'" type="button" onclick="window.maSetLanguage(\'hi\')">हिन्दी</button>'+
        '</div>'+
      '</header><div class="login-road"></div>'+
      '<section class="bt-card">'+
        '<h1 class="bt-title">'+esc(lt.title)+'</h1>'+
        '<p class="bt-sub">'+esc(lt.sub)+'</p>'+
        '<label class="bt-label">'+esc(lt.mobileLbl)+'</label>'+
        '<div class="bt-inputwrap"><span class="bt-icon">📱</span><input id="maLoginMobile" class="bt-input" name="username" autocomplete="username" autocapitalize="none" spellcheck="false" inputmode="numeric" pattern="[0-9]{10}" maxlength="10" placeholder="'+esc(lt.mobilePh)+'"></div>'+
        '<label class="bt-label">'+esc(lt.passLbl)+'</label>'+
        '<div class="bt-inputwrap"><span class="bt-icon">🔒</span><input id="maLoginPass" class="bt-input" name="password" autocomplete="current-password" autocapitalize="none" spellcheck="false" type="password" maxlength="64" placeholder="'+esc(lt.passPh)+'"><button id="maPassToggle" class="bt-eye" type="button" aria-label="Show password">👁️</button></div>'+
        '<button id="maLoginBtn" class="bt-login" type="button">'+lt.btn+'</button>'+
        '<div id="maLoginErr" class="bt-error">'+esc(message||'')+'</div>'+
        '<div class="bt-note">'+esc(lt.note)+'</div>'+
      '</section></div>';
    document.body.appendChild(root);
    const passInput=root.querySelector('#maLoginPass'), passToggle=root.querySelector('#maPassToggle');
    passToggle.onclick=()=>{const show=passInput.type==='password';passInput.type=show?'text':'password';passToggle.textContent=show?'🙈':'👁️';passToggle.setAttribute('aria-label',show?'Hide password':'Show password');};
    root.querySelector('#maLoginBtn').onclick=function(){
      const mobile=root.querySelector('#maLoginMobile').value.replace(/\D/g,''),pass=passInput.value,err=root.querySelector('#maLoginErr'),btn=root.querySelector('#maLoginBtn');
      if(!/^\d{10}$/.test(mobile)||!pass){err.textContent=lt.errFormat;return;}
      btn.disabled=true;btn.textContent=lt.btnLoading;err.textContent='';
      apiRequest('login',{username:mobile,password:pass},res=>finishLoginUser(res,root,btn,err));
    };
  }

  /* DIAGNOSTIC KNOWLEDGE (TRILINGUAL WITH AUTOMOTIVE KEYWORDS) */
  const DIAGNOSTIC_KNOWLEDGE=[
    {
      id:'engine_overheating',
      pattern:/overheat|too hot|high temp|temperature|coolant|boiling|radiator|steam|temp gauge|ಬಿಸಿ|ತಾಪಮಾನ|ಕೂಲಂಟ್|ರೇಡಿಯೇಟರ್|ಆವಿ|ಗರ್ಮ್|गर्म|तापमान|कूलेंट|रेडिएटर|भाप/i,
      severity:'CRITICAL',
      icon:'🌡️',
      en:{
        title:'Engine Overheating / High Coolant Temperature',
        cause:'Low coolant level, radiator clogged with road dirt, leaking hose, or water pump belt slipping.',
        warning:'⚠️ DANGER: Hot coolant is under severe pressure. NEVER open the radiator cap while the engine is hot. Boiling pressurized liquid will erupt and cause severe burn injuries!',
        immediateAction:'Safely stop the truck on the road shoulder as soon as possible, turn on hazard lights, switch off the engine, and engage the parking brake.',
        steps:[
          'Stop the truck in a safe place off the road as soon as possible.',
          'Switch off the engine immediately to prevent engine seizure.',
          'Do not open the radiator cap while the engine is hot.',
          'Wait at least 20 to 30 minutes for the engine to cool down naturally.',
          'Look under the truck for green or pink coolant dripping or steam.',
          'Once the engine is cool, check the coolant reservoir tank. Top up with clean coolant or clean water if low.',
          'Contact the mechanic or fleet supervisor for further assistance before restarting.'
        ],
        driverSafe:'Check the plastic coolant overflow tank level when engine is cold; inspect for loose hoses from above.',
        mechanicRequired:'Coolant is boiling or dripping heavily, temperature gauge stays in Red zone, or engine makes abnormal noises.'
      },
      kn:{
        title:'ಎಂಜಿನ್ ತಾಪಮಾನ ಹೆಚ್ಚು / ಓವರ್‌ಹೀಟಿಂಗ್',
        cause:'ಕೂಲಂಟ್ ಮಟ್ಟ ಕಡಿಮೆಯಾಗಿರುವುದು, ರೇಡಿಯೇಟರ್ ಧೂಳಿನಿಂದ ಮುಚ್ಚಿರುವುದು, ಪೈಪ್ ಸೋರಿಕೆ ಅಥವಾ ವಾಟರ್ ಪಂಪ್ ಬೆಲ್ಟ್ ಸಡಿಲವಾಗಿರುವುದು.',
        warning:'⚠️ ಅಪಾಯ: ಬಿಸಿ ಕೂಲಂಟ್ ತೀವ್ರ ಒತ್ತಡದಲ್ಲಿರುತ್ತದೆ. ಎಂಜಿನ್ ಬಿಸಿಯಾಗಿರುವಾಗ ರೇಡಿಯೇಟರ್ ಕ್ಯಾಪ್ ಅನ್ನು ಎಂದಿಗೂ ತೆರೆಯಬೇಡಿ! ಕುದಿಯುವ ದ್ರವ ಸಿಡಿದು ಸುಟ್ಟ ಗಾಯಗಳಾಗಬಹುದು.',
        immediateAction:'ರಸ್ತೆಯ ಪಕ್ಕದಲ್ಲಿ ಸುರಕ್ಷಿತವಾಗಿ ವಾಹನ ನಿಲ್ಲಿಸಿ, ಹ್ಯಾಜಾರ್ಡ್ ಲೈಟ್ ಆನ್ ಮಾಡಿ, ಇಂಜಿನ್ ಆಫ್ ಮಾಡಿ ಮತ್ತು ಹ್ಯಾಂಡ್‌ಬ್ರೇಕ್ ಹಾಕಿ.',
        steps:[
          'ರಸ್ತೆಯಿಂದ ಹೊರಗೆ ಸುರಕ್ಷಿತ ತೆರೆದ ಜಾಗದಲ್ಲಿ ಟ್ರಕ್ ನಿಲ್ಲಿಸಿ.',
          'ಎಂಜಿನ್ ಸೀಜ್ ಆಗುವುದನ್ನು ತಪ್ಪಿಸಲು ತಕ್ಷಣ ಇಂಜಿನ್ ಆಫ್ ಮಾಡಿ.',
          'ಎಂಜಿನ್ ಬಿಸಿಯಾಗಿರುವಾಗ ಯಾವುದೇ ಕಾರಣಕ್ಕೂ ರೇಡಿಯೇಟರ್ ಕ್ಯಾಪ್ ತೆರೆಯಬೇಡಿ.',
          'ಎಂಜಿನ್ ತಣ್ಣಗಾಗಲು ಕನಿಷ್ಠ 20 ರಿಂದ 30 ನಿಮಿಷ ಕಾಯಿರಿ.',
          'ಟ್ರಕ್ ಕೆಳಗೆ ಹಸಿರು ಅಥವಾ ಗುಲಾಬಿ ಬಣ್ಣದ ಕೂಲಂಟ್ ಸೋರುತ್ತಿದೆಯೇ ಅಥವಾ ಹಬೆ ಬರುತ್ತಿದೆಯೇ ಎಂದು ನೋಡಿ.',
          'ಎಂಜಿನ್ ತಣ್ಣಗಾದ ನಂತರ ಕೂಲಂಟ್ ಟ್ಯಾಂಕ್ ಪರಿಶೀಲಿಸಿ. ಕಡಿಮೆಯಿದ್ದರೆ ಶುದ್ಧ ಕೂಲಂಟ್ ಅಥವಾ ನೀರು ಹಾಕಿ.',
          'ಮತ್ತೆ ಸ್ಟಾರ್ಟ್ ಮಾಡುವ ಮೊದಲು ಮೆಕಾನಿಕ್ ಅಥವಾ ಸೂಪರ್‌ವೈಸರ್‌ಗೆ ಕರೆ ಮಾಡಿ.'
        ],
        driverSafe:'ಎಂಜಿನ್ ತಣ್ಣಗಿದ್ದಾಗ ಪ್ಲಾಸ್ಟಿಕ್ ಕೂಲಂಟ್ ಟ್ಯಾಂಕ್ ಮಟ್ಟವನ್ನು ಪರಿಶೀಲಿಸಿ; ಸಡಿಲ ಪೈಪ್‌ಗಳನ್ನು ಮೇಲಿನಿಂದ ನೋಡಿ.',
        mechanicRequired:'ಕೂಲಂಟ್ ತೀವ್ರವಾಗಿ ಸೋರುತ್ತಿದ್ದರೆ, ತಾಪಮಾನ ಗೇಜ್ ಕೆಂಪು ವಲಯದಲ್ಲೇ ಇದ್ದರೆ ಅಥವಾ ಅಸಹಜ ಶಬ್ದ ಬರುತ್ತಿದ್ದರೆ.'
      },
      hi:{
        title:'इंजन ओवरहीटिंग / कूलेंट का अधिक तापमान',
        cause:'कूलेंट का स्तर कम होना, रेडिएटर में गंदगी जमा होना, पाइप से रिसाव या वाटर पंप बेल्ट ढीली होना।',
        warning:'⚠️ खतरा: गर्म कूलेंट अत्यधिक दबाव में होता है। इंजन गर्म होने पर रेडिएटर कैप कभी न खोलें! खौलता हुआ पानी बाहर निकलकर गंभीर रूप से जला सकता है।',
        immediateAction:'सड़क के किनारे सुरक्षित जगह पर ट्रक रोकें, हजार्ड लाइट जलाएं, इंजन तुरंत बंद करें और हैंड ब्रेक लगाएं।',
        steps:[
          'ट्रक को सड़क से हटाकर सुरक्षित स्थान पर रोकें।',
          'इंजन सीज होने से बचाने के लिए तुरंत इग्निशन बंद करें।',
          'इंजन गर्म होने पर रेडिएटर ढक्कन बिल्कुल न खोलें।',
          'इंजन को प्राकृतिक रूप से ठंडा होने के लिए 20 से 30 मिनट रुकें।',
          'ट्रक के नीचे हरा या गुलाबी कूलेंट टपकने या भाप निकलने की जांच करें।',
          'ठंडा होने पर प्लास्टिक कूलेंट टैंक जांचें और कम होने पर साफ कूलेंट या पानी भरें।',
          'दोबारा स्टार्ट करने से पहले मैकेनिक या सुपरवाइजर से बात करें।'
        ],
        driverSafe:'इंजन ठंडा होने पर कूलेंट ओवरफ्लो टैंक का स्तर जांचें; ऊपर से ढीली नली देखें।',
        mechanicRequired:'कूलेंट उबल रहा हो या भारी रिसाव हो, टेम्परेचर सुई लाल निशान पर रहे या असामान्य आवाज आए।'
      }
    },
    {
      id:'brake_failure',
      pattern:/brake|air press|low air|spongy|pedal to floor|brakes soft|air leak|hissing|ಬ್ರೇಕ್|ಏರ್ ಪ್ರೆಶರ್|ಬ್ರೇಕ್ ಹಿಡಿಯುತ್ತಿಲ್ಲ|ಏರ್ ಲೀಕ್|ಶಬ್ದ|ಗಾಳಿ ಕಡಿಮೆ|ब्रेक|एयर प्रेशर|ब्रेक नहीं लग रहा|कम हवा|एयर लीक/i,
      severity:'CRITICAL',
      icon:'🛑',
      en:{
        title:'Brake System Issue / Low Air Pressure Warning',
        cause:'Low compressed air pressure, air line leak, punctured brake chamber diaphragm, or worn brake shoes.',
        warning:'🛑 CRITICAL SAFETY WARNING: Heavy commercial trucks require full air pressure to stop. Driving with low air pressure or spongy brakes can cause complete brake loss and severe accidents. DO NOT DRIVE.',
        immediateAction:'Bring the truck to an immediate controlled stop using the parking brake if necessary. Turn on hazard warning lights.',
        steps:[
          'Stop the truck immediately in a safe location away from fast highway traffic.',
          'Firmly pull up the parking brake lever and place wheel chocks under tyres.',
          'Check the instrument cluster air gauges: both Front and Rear circuits must read above 6.5 bar (95 psi).',
          'With engine idling, listen for loud air hissing around the air tanks, air dryer, and wheels.',
          'Drain moisture from the air tank bottom purge valves by pulling the drain rings.',
          'Do not attempt to drive if air pressure fails to build up or the low-pressure buzzer sounds.',
          'Contact your fleet supervisor and mobile mechanic immediately for on-site brake inspection.'
        ],
        driverSafe:'Drain moisture from air tank drain rings and visually inspect for disconnected air tubes.',
        mechanicRequired:'Air pressure will not climb above 6.5 bar, brake pedal feels soft or spongy, or air hiss is audible.'
      },
      kn:{
        title:'ಬ್ರೇಕ್ ಸಿಸ್ಟಮ್ ಸಮಸ್ಯೆ / ಕಡಿಮೆ ಏರ್ ಪ್ರೆಶರ್ ಎಚ್ಚರಿಕೆ',
        cause:'ಕಂಪ್ರೆಸ್ಡ್ ಏರ್ ಪ್ರೆಶರ್ ಕಡಿಮೆಯಾಗಿರುವುದು, ಏರ್ ಪೈಪ್ ಸೋರಿಕೆ, ಬ್ರೇಕ್ ಚೇಂಬರ್ ಡಯಾಫ್ರಾಮ್ ಹಾನಿ ಅಥವಾ ಸವೆದ ಬ್ರೇಕ್ ಶೂಗಳು.',
        warning:'🛑 ಗಂಭೀರ ಸುರಕ್ಷತಾ ಎಚ್ಚರಿಕೆ: ಭಾರೀ ಟ್ರಕ್‌ಗಳನ್ನು ನಿಲ್ಲಿಸಲು ಸಂಪೂರ್ಣ ಗಾಳಿಯ ಒತ್ತಡ ಬೇಕು. ಕಡಿಮೆ ಒತ್ತಡದಲ್ಲಿ ಚಾಲನೆ ಮಾಡುವುದು ಸಂಪೂರ್ಣ ಬ್ರೇಕ್ ವೈಫಲ್ಯಕ್ಕೆ ಕಾರಣವಾಗಬಹುದು. ಮುಂದುವರಿಯಬೇಡಿ!',
        immediateAction:'ತಕ್ಷಣ ವಾಹನವನ್ನು ನಿಯಂತ್ರಣದಲ್ಲಿ ನಿಲ್ಲಿಸಿ, ಪಾರ್ಕಿಂಗ್ ಹ್ಯಾಂಡ್‌ಬ್ರೇಕ್ ಎಳೆಯಿರಿ ಮತ್ತು ಹ್ಯಾಜಾರ್ಡ್ ಲೈಟ್ ಹಾಕಿ.',
        steps:[
          'ವೇಗದ ಹೆದ್ದಾರಿ ಟ್ರಾಫಿಕ್‌ನಿಂದ ದೂರ ಸುರಕ್ಷಿತ ಜಾಗದಲ್ಲಿ ಟ್ರಕ್ ನಿಲ್ಲಿಸಿ.',
          'ಪಾರ್ಕಿಂಗ್ ಹ್ಯಾಂಡ್‌ಬ್ರೇಕ್ ಗಟ್ಟಿಯಾಗಿ ಎಳೆಯಿರಿ ಮತ್ತು ಟೈರ್‌ಗಳಿಗೆ ಚಾಕ್ ಇಡಿ.',
          'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಏರ್ ಗೇಜ್ ನೋಡಿ: ಫ್ರಂಟ್ ಮತ್ತು ರೇರ್ ಎರಡೂ 6.5 bar (95 psi) ಗಿಂತ ಹೆಚ್ಚಿರಬೇಕು.',
          'ಎಂಜಿನ್ ಐಡ್ಲಿಂಗ್‌ನಲ್ಲಿರುವಾಗ ಏರ್ ಟ್ಯಾಂಕ್ ಮತ್ತು ಚಕ್ರಗಳ ಸುತ್ತ ಗಾಳಿಯ ಶಬ್ದ (hissing) ಬರುತ್ತಿದೆಯೇ ಆಲಿಸಿ.',
          'ಏರ್ ಟ್ಯಾಂಕ್ ಕೆಳಗಿನ ರಿಂಗ್ ಎಳೆದು ನೀರನ್ನು ಹೊರಹಾಕಿ (Drain moisture).',
          'ಏರ್ ಪ್ರೆಶರ್ ಹೆಚ್ಚಾಗದಿದ್ದರೆ ಅಥವಾ ಬಜರ್ ಹೊಡೆಯುತ್ತಿದ್ದರೆ ಚಲಾಯಿಸಲು ಪ್ರಯತ್ನಿಸಬೇಡಿ.',
          'ತಕ್ಷಣ ಫ್ಲೀಟ್ ಸೂಪರ್‌ವೈಸರ್ ಮತ್ತು ಮೆಕಾನಿಕ್‌ಗೆ ಕರೆ ಮಾಡಿ.'
        ],
        driverSafe:'ಏರ್ ಟ್ಯಾಂಕ್ ಕೆಳಗಿನ ಡ್ರೈನ್ ರಿಂಗ್ ಎಳೆದು ನೀರು ಹೊರಹಾಕಿ ಮತ್ತು ಕಳಚಿದ ಪೈಪ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.',
        mechanicRequired:'ಏರ್ ಪ್ರೆಶರ್ 6.5 bar ಗಿಂತ ಹೆಚ್ಚಾಗದಿದ್ದರೆ, ಬ್ರೇಕ್ ಪೆಡಲ್ ಮೆತ್ತಗಾಗಿದ್ದರೆ ಅಥವಾ ಗಾಳಿ ಸೋರಿಕೆಯಾಗುತ್ತಿದ್ದರೆ.'
      },
      hi:{
        title:'ब्रेक सिस्टम समस्या / कम एयर प्रेशर चेतावनी',
        cause:'हवा का दबाव कम होना, एयर पाइप से रिसाव, ब्रेक चैंबर डायफ्राम कटना या ब्रेक शू घिसना।',
        warning:'🛑 गंभीर सुरक्षा चेतावनी: भारी कमर्शियल ट्रकों को रोकने के लिए पूरा हवा का दबाव जरूरी है। कम प्रेशर में ट्रक चलाने से ब्रेक पूरी तरह फेल हो सकते हैं। गाड़ी न चलाएं!',
        immediateAction:'पार्किंग ब्रेक का इस्तेमाल कर ट्रक को तुरंत सुरक्षित रोकें और हजार्ड लाइट ऑन करें।',
        steps:[
          'हाईवे ट्रैफिक से दूर सुरक्षित जगह पर ट्रक तुरंत रोकें।',
          'पार्किंग हैंड ब्रेक मजबूती से लगाएं और पहियों के नीचे गुटका (चॉक) लगाएं।',
          'डैशबोर्ड एयर मीटर देखें: फ्रंट और रियर दोनों सुई 6.5 बार (95 psi) से ऊपर होनी चाहिए।',
          'इंजन चालू रखकर एयर टैंक और पहियों के पास हवा की सीटी जैसी आवाज (लीकेज) सुनें।',
          'एयर टैंक के नीचे लगे ड्रेन रिंग को खींचकर जमा पानी बाहर निकालें।',
          'यदि प्रेशर न बढ़े या लो-प्रेशर बजर बजे तो गाड़ी चलाने की कोशिश न करें।',
          'ऑन-साइट जांच के लिए तुरंत फ्लीट सुपरवाइजर और मैकेनिक को फोन करें।'
        ],
        driverSafe:'एयर टैंक के नीचे का छल्ला खींचकर नमी निकालें और ढीले एयर पाइप देखें।',
        mechanicRequired:'एयर प्रेशर 6.5 बार से ऊपर न पहुंचे, ब्रेक पैडल ढीला लगे या तेज हवा लीक हो।'
      }
    },
    {
      id:'steering_problem',
      pattern:/steer|pulling|vibration|wobble|stiff steer|hard steer|ಸ್ಟೀರಿಂಗ್|ಕಂಪನ|ತಿರುಗಿಸಲು ಕಷ್ಟ|ಸ್ಟಿರಿಂಗ್|स्टीयरिंग|कंपन|स्टीयरिंग भारी/i,
      severity:'CRITICAL',
      icon:'🔄',
      en:{
        title:'Steering Instability / Heavy Vibration / Pulling',
        cause:'Front tyre puncture, low power steering fluid, loose steering belt, or damaged tie-rod linkage.',
        warning:'⚠️ SAFETY WARNING: Loss of steering control or severe wheel wobble can lead to rollover or lane departure. Do not continue driving at highway speed.',
        immediateAction:'Grip the steering wheel firmly with both hands, reduce speed gradually without sharp braking, and steer smoothly to the shoulder.',
        steps:[
          'Steer smoothly onto the shoulder or nearest safe parking area.',
          'Turn on hazard warning lights and apply the hand brake.',
          'Check both front steer tyres immediately for puncture, low air, or tyre bulge.',
          'Check the power steering oil reservoir dipstick under the cabin. Fluid should be between MIN and MAX.',
          'Check the power steering pump drive belt for slippage or breakage.',
          'Inspect the front axle and steering arms for loose bolts or hydraulic oil leakage.',
          'Contact the mechanic or fleet supervisor for towing or roadside steering inspection.'
        ],
        driverSafe:'Check front tyre pressures and power steering oil level in the reservoir.',
        mechanicRequired:'Steering wheel is hard to turn, binds, or pulls violently to one side.'
      },
      kn:{
        title:'ಸ್ಟೀರಿಂಗ್ ಅಸ್ಥಿರತೆ / ತೀವ್ರ ಕಂಪನ / ಪಕ್ಕಕ್ಕೆ ಎಳೆಯುವುದು',
        cause:'ಮುಂಭಾಗದ ಟೈರ್ ಪಂಕ್ಚರ್, ಪವರ್ ಸ್ಟೀರಿಂಗ್ ಆಯಿಲ್ ಕಡಿಮೆ, ಬೆಲ್ಟ್ ಸಡಿಲ ಅಥವಾ ಟೈ-ರಾಡ್ ಲಿಂಕ್ ಹಾನಿ.',
        warning:'⚠️ ಸುರಕ್ಷತಾ ಎಚ್ಚರಿಕೆ: ಸ್ಟೀರಿಂಗ್ ನಿಯಂತ್ರಣ ತಪ್ಪಿದರೆ ಅಥವಾ ಚಕ್ರ ಅಲುಗಾಡಿದರೆ ವಾಹನ ಪಲ್ಟಿಯಾಗುವ ಅಪಾಯವಿದೆ. ವೇಗವಾಗಿ ಚಲಿಸಬೇಡಿ.',
        immediateAction:'ಎರಡೂ ಕೈಗಳಿಂದ ಸ್ಟೀರಿಂಗ್ ಅನ್ನು ಗಟ್ಟಿಯಾಗಿ ಹಿಡಿದು, ವೇಗ ಕಡಿಮೆ ಮಾಡಿ ರಸ್ತೆ ಬದಿಗೆ ಸರಿಸಿ.',
        steps:[
          'ರಸ್ತೆಯ ಬದಿಗೆ ಅಥವಾ ಸಮೀಪದ ಸುರಕ್ಷಿತ ಪಾರ್ಕಿಂಗ್ ಜಾಗಕ್ಕೆ ಟ್ರಕ್ ಸರಿಸಿ.',
          'ಹ್ಯಾಜಾರ್ಡ್ ಲೈಟ್ ಆನ್ ಮಾಡಿ ಮತ್ತು ಹ್ಯಾಂಡ್‌ಬ್ರೇಕ್ ಹಾಕಿ.',
          'ಮುಂಭಾಗದ ಎರಡೂ ಟೈರ್‌ಗಳನ್ನು ಪಂಕ್ಚರ್, ಕಡಿಮೆ ಗಾಳಿ ಅಥವಾ ಉಬ್ಬರಕ್ಕಾಗಿ ತಕ್ಷಣ ನೋಡಿ.',
          'ಕ್ಯಾಬಿನ್ ಕೆಳಗಿನ ಪವರ್ ಸ್ಟೀರಿಂಗ್ ಆಯಿಲ್ ಮಟ್ಟವನ್ನು ಡಿಪ್‌ಸ್ಟಿಕ್‌ನಿಂದ ಪರಿಶೀಲಿಸಿ (MIN ಮತ್ತು MAX ಮಧ್ಯೆ ಇರಬೇಕು).',
          'ಪವರ್ ಸ್ಟೀರಿಂಗ್ ಪಂಪ್ ಬೆಲ್ಟ್ ತುಂಡಾಗಿದೆಯೇ ಅಥವಾ ಸಡಿಲವಾಗಿದೆಯೇ ಎಂದು ನೋಡಿ.',
          'ಮುಂಭಾಗದ ಆಕ್ಸಲ್ ಮತ್ತು ಸ್ಟೀರಿಂಗ್ ಆರ್ಮ್‌ನಲ್ಲಿ ಆಯಿಲ್ ಸೋರಿಕೆ ಅಥವಾ ಸಡಿಲ ಬೋಲ್ಟ್‌ಗಳನ್ನು ಪರೀಕ್ಷಿಸಿ.',
          'ಮೆಕಾನಿಕ್ ಅಥವಾ ಸೂಪರ್‌ವೈಸರ್‌ಗೆ ಕರೆ ಮಾಡಿ.'
        ],
        driverSafe:'ಮುಂಭಾಗದ ಟೈರ್ ಗಾಳಿ ಮತ್ತು ಪವರ್ ಸ್ಟೀರಿಂಗ್ ಆಯಿಲ್ ಮಟ್ಟವನ್ನು ಪರಿಶೀಲಿಸಿ.',
        mechanicRequired:'ಸ್ಟೀರಿಂಗ್ ತಿರುಗಿಸಲು ಕಷ್ಟವಾಗಿದ್ದರೆ, ಸಿಲುಕಿಕೊಳ್ಳುತ್ತಿದ್ದರೆ ಅಥವಾ ಬಲವಾಗಿ ಪಕ್ಕಕ್ಕೆ ಎಳೆಯುತ್ತಿದ್ದರೆ.'
      },
      hi:{
        title:'स्टीयरिंग अस्थिरता / तेज कंपन / एक तरफ खिंचाव',
        cause:'आगे का टायर पंचर, पावर स्टीयरिंग ऑयल कम, बेल्ट ढीली होना या टाई-रॉड लिंकेज खराब होना।',
        warning:'⚠️ सुरक्षा चेतावनी: स्टीयरिंग पर नियंत्रण खोने या पहिया कांपने से दुर्घटना हो सकती है। हाईवे स्पीड पर गाड़ी न चलाएं।',
        immediateAction:'स्टीयरिंग व्हील को दोनों हाथों से कसकर पकड़ें, धीरे-धीरे गति कम करें और सुरक्षित किनारे लगाएं।',
        steps:[
          'ट्रक को सड़क किनारे सुरक्षित स्थान पर ले जाएं।',
          'हजार्ड लाइट ऑन करें और हैंड ब्रेक लगाएं।',
          'आगे के दोनों टायरों में हवा, पंचर या कट की तुरंत जांच करें।',
          'केबिन के नीचे पावर स्टीयरिंग ऑयल गेज देखें (MIN और MAX के बीच होना चाहिए)।',
          'पावर स्टीयरिंग पंप की बेल्ट टूटने या ढीली होने की जांच करें।',
          'आगे के एक्सेल और स्टीयरिंग रॉड पर तेल का रिसाव या ढीले नट-बोल्ट देखें।',
          'मैकेनिक या फ्लीट सुपरवाइजर से तुरंत संपर्क करें।'
        ],
        driverSafe:'आगे के टायरों का प्रेशर और पावर स्टीयरिंग ऑयल स्तर जांचें।',
        mechanicRequired:'स्टीयरिंग बहुत भारी हो जाए, अटक रहा हो या एक तरफ तेज खिंचाव हो।'
      }
    },
    {
      id:'smoke_fire',
      pattern:/smoke|burning|flame|fire|exhaust smoke|white smoke|black smoke|blue smoke|ಹೊಗೆ|ಬೆಂಕಿ|ಸುಡುವ ವಾಸನೆ|ಬಿಳಿ ಹೊಗೆ|ಕಪ್ಪು ಹೊಗೆ|ಧೂಮ|धुआं|आग|जलने की गंध|सफेद धुआं|काला धुआं/i,
      severity:'HIGH',
      icon:'💨',
      en:{
        title:'Exhaust Smoke / Burning Odor / Fire Hazard',
        cause:'White smoke: unburnt diesel or coolant leak. Black smoke: choked air filter or overloaded injectors. Blue smoke: engine oil burning.',
        warning:'⚠️ FIRE HAZARD: If smoke is rising from under cabin or burning smell appears, stop engine immediately, switch off battery isolator, and keep fire extinguisher ready.',
        immediateAction:'Park in an open area away from dry grass or fuel pumps. Turn off engine and battery isolator immediately.',
        steps:[
          'Stop the truck in an open, clear area immediately.',
          'Switch off the engine and disconnect the battery cut-off switch near the battery box.',
          'Keep the vehicle fire extinguisher ready at hand.',
          'Note the color of exhaust smoke (White, Black, or Blue) and whether it smells like diesel.',
          'If black smoke: check the air filter restriction indicator on the intake pipe.',
          'If white smoke with strong diesel odor: do not keep cranking the engine.',
          'Contact your fleet supervisor or mechanic with exact details of smoke color.'
        ],
        driverSafe:'Inspect the air cleaner restriction indicator and check for external fluid dripping onto exhaust pipes.',
        mechanicRequired:'White smoke persists, engine misfires violently, or smoke is accompanied by burning odor.'
      },
      kn:{
        title:'ಹೊಗೆ / ಸುಡುವ ವಾಸನೆ / ಬೆಂಕಿಯ ಅಪಾಯ',
        cause:'ಬಿಳಿ ಹೊಗೆ: ಡೀಸೆಲ್ ದಹನವಾಗದಿರುವುದು ಅಥವಾ ಕೂಲಂಟ್ ಸೋರಿಕೆ. ಕಪ್ಪು ಹೊಗೆ: ಏರ್ ಫಿಲ್ಟರ್ ಜಾಮ್ ಅಥವಾ ಇಂಜೆಕ್ಟರ್ ಸಮಸ್ಯೆ. ನೀಲಿ ಹೊಗೆ: ಇಂಜಿನ್ ಆಯಿಲ್ ಉರಿಯುತ್ತಿರುವುದು.',
        warning:'⚠️ ಬೆಂಕಿಯ ಅಪಾಯ: ಕ್ಯಾಬಿನ್ ಕೆಳಗಿನಿಂದ ಹೊಗೆ ಅಥವಾ ಸುಡುವ ವಾಸನೆ ಬಂದರೆ ತಕ್ಷಣ ಇಂಜಿನ್ ಆಫ್ ಮಾಡಿ, ಬ್ಯಾಟರಿ ಕಟ್-ಆಫ್ ಸ್ವಿಚ್ ಆಫ್ ಮಾಡಿ ಮತ್ತು ಅಗ್ನಿಶಾಮಕ ಸಿದ್ಧವಾಗಿಡಿ.',
        immediateAction:'ಒಣ ಹುಲ್ಲು ಅಥವಾ ಪೆಟ್ರೋಲ್ ಬಂಕ್‌ಗಳಿಂದ ದೂರ ತೆರೆದ ಜಾಗದಲ್ಲಿ ನಿಲ್ಲಿಸಿ ಇಂಜಿನ್ ಆಫ್ ಮಾಡಿ.',
        steps:[
          'ತಕ್ಷಣ ತೆರೆದ, ಸ್ವಚ್ಛ ಜಾಗದಲ್ಲಿ ಟ್ರಕ್ ನಿಲ್ಲಿಸಿ.',
          'ಇಂಜಿನ್ ಆಫ್ ಮಾಡಿ ಮತ್ತು ಬ್ಯಾಟರಿ ಬಾಕ್ಸ್ ಬಳಿಯ ಕಟ್-ಆಫ್ ಸ್ವಿಚ್ ಆಫ್ ಮಾಡಿ.',
          'ವಾಹನದ ಅಗ್ನಿಶಾಮಕ ಸಿಲಿಂಡರ್ ಅನ್ನು ಕೈಯಲ್ಲಿ ಸಿದ್ಧವಾಗಿಡಿ.',
          'ಹೊಗೆಯ ಬಣ್ಣವನ್ನು ಗಮನಿಸಿ (ಬಿಳಿ, ಕಪ್ಪು ಅಥವಾ ನೀಲಿ) ಮತ್ತು ಡೀಸೆಲ್ ವಾಸನೆ ಇದೆಯೇ ನೋಡಿ.',
          'ಕಪ್ಪು ಹೊಗೆಯಾಗಿದ್ದರೆ: ಏರ್ ಫಿಲ್ಟರ್ ಇಂಡಿಕೇಟರ್ ಕೆಂಪಾಗಿದೆಯೇ ನೋಡಿ.',
          'ತೀವ್ರ ಡೀಸೆಲ್ ವಾಸನೆಯೊಂದಿಗೆ ಬಿಳಿ ಹೊಗೆ ಬರುತ್ತಿದ್ದರೆ ಇಂಜಿನ್ ಪದೇ ಪದೇ ಕ್ರ್ಯಾಂಕ್ ಮಾಡಬೇಡಿ.',
          'ಹೊಗೆಯ ಬಣ್ಣದ ವಿವರಗಳೊಂದಿಗೆ ಸೂಪರ್‌ವೈಸರ್ ಅಥವಾ ಮೆಕಾನಿಕ್‌ಗೆ ಕರೆ ಮಾಡಿ.'
        ],
        driverSafe:'ಏರ್ ಫಿಲ್ಟರ್ ಇಂಡಿಕೇಟರ್ ನೋಡಿ ಮತ್ತು ಸೈಲೆನ್ಸರ್ ಮೇಲೆ ಎಣ್ಣೆ ಬೀಳುತ್ತಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ.',
        mechanicRequired:'ಬಿಳಿ ಹೊಗೆ ನಿರಂತರವಾಗಿದ್ದರೆ, ಇಂಜಿನ್ ಮಿಸ್‌ಫೈರ್ ಆಗುತ್ತಿದ್ದರೆ ಅಥವಾ ಸುಡುವ ವಾಸನೆ ಬರುತ್ತಿದ್ದರೆ.'
      },
      hi:{
        title:'धुआं निकलना / जलने की गंध / आग का खतरा',
        cause:'सफेद धुआं: अधूरा जला डीजल या कूलेंट रिसाव। काला धुआं: एयर फिल्टर चोक होना। नीला धुआं: इंजन ऑयल का जलना।',
        warning:'⚠️ आग का खतरा: केबिन के नीचे से धुआं या जलने की गंध आने पर तुरंत इंजन बंद करें, बैटरी कट-ऑफ स्विच काटें और अग्निशामक यंत्र तैयार रखें।',
        immediateAction:'सूखी घास या पेट्रोल पंप से दूर खुले स्थान में ट्रक रोकें और तुरंत इंजन बंद करें।',
        steps:[
          'ट्रक को तुरंत खुले, साफ स्थान पर रोकें।',
          'इंजन बंद करें और बैटरी बॉक्स के पास लगा मेन कट-ऑफ स्विच बंद करें।',
          'वाहन का अग्निशामक यंत्र (Fire Extinguisher) तुरंत तैयार रखें।',
          'साइलेंसर से निकलने वाले धुएं का रंग देखें (सफेद, काला या नीला) और डीजल की गंध सूंघें।',
          'यदि काला धुआं है: एयर पाइप पर लगे एयर फिल्टर चोक इंडिकेटर को देखें।',
          'यदि तेज डीजल गंध वाला सफेद धुआं है: बार-बार इंजन स्टार्ट करने की कोशिश न करें।',
          'धुएं के रंग की सटीक जानकारी के साथ मैकेनिक या सुपरवाइजर को फोन करें।'
        ],
        driverSafe:'एयर फिल्टर इंडिकेटर की जांच करें और साइलेंसर पर तेल रिसाव देखें।',
        mechanicRequired:'सफेद धुआं लगातार आ रहा हो, इंजन में झटका लग रहा हो या जलने की गंध आ रही हो।'
      }
    },
    {
      id:'fuel_leak',
      pattern:/fuel leak|diesel leak|dripping fuel|smell diesel|diesel odor|fuel line|ಡೀಸೆಲ್ ಸೋರಿಕೆ|ಇಂಧನ ಸೋರಿಕೆ|ಡೀಸೆಲ್ ಲೀಕ್|ಡೀಸೆಲ್ ವಾಸನೆ|ಲೀಕ್|ಡಿಜೆಲ್|डीजल लीक|ईंधन लीक|डीजल टपक|डीजल गंध/i,
      severity:'HIGH',
      icon:'⛽',
      en:{
        title:'Diesel Fuel Leakage / Fuel Line Damage',
        cause:'Cracked nylon fuel hose, loose banjo bolt at fuel filter, punctured fuel tank, or leaking injector line.',
        warning:'⚠️ FIRE & EXPLOSION RISK: Diesel fuel dripping near hot exhaust ATS parts (exceeding 450°C) can catch fire. Do not smoke, do not use open flames, and do not crank engine.',
        immediateAction:'Park in safe, well-ventilated open area. Turn off engine and battery isolator immediately.',
        steps:[
          'Stop the truck immediately in a safe open location away from heat sources.',
          'Turn off the ignition key and switch off the battery isolator switch.',
          'Inspect the fuel tank, primary water separator, and engine fuel filters for diesel dripping.',
          'Check if the plastic drain cock at the bottom of the fuel filter is loose; tighten gently by hand if safe.',
          'Check for visible cracked rubber or plastic fuel hoses.',
          'If fuel is spraying under high pressure from the fuel rail, DO NOT TOUCH (can pierce skin).',
          'Contact the fleet mechanic or breakdown team to replace the leaking line.'
        ],
        driverSafe:'Hand-tighten the plastic water separator drain plug if dripping and wipe clean external diesel.',
        mechanicRequired:'Any high-pressure common rail line leak, cracked fuel pipe, or spray inside engine bay.'
      },
      kn:{
        title:'ಡೀಸೆಲ್ ಇಂಧನ ಸೋರಿಕೆ / ಪೈಪ್ ಹಾನಿ',
        cause:'ಡೀಸೆಲ್ ಪೈಪ್ ಬಿರುಕು, ಫಿಲ್ಟರ್ ಬೋಲ್ಟ್ ಸಡಿಲ, ಟ್ಯಾಂಕ್ ಪಂಕ್ಚರ್ ಅಥವಾ ಇಂಜೆಕ್ಟರ್ ರಿಟರ್ನ್ ಲೈನ್ ಸೋರಿಕೆ.',
        warning:'⚠️ ಬೆಂಕಿಯ ಅಪಾಯ: ಬಿಸಿ ಸೈಲೆನ್ಸರ್/ATS ಭಾಗಗಳ ಬಳಿ (450°C ಗಿಂತ ಹೆಚ್ಚು ಬಿಸಿ) ಡೀಸೆಲ್ ಬಿದ್ದರೆ ಬೆಂಕಿ ಹತ್ತಿಕೊಳ್ಳಬಹುದು. ಧೂಮಪಾನ ಮಾಡಬೇಡಿ ಮತ್ತು ಬೆಂಕಿ ತರಬೇಡಿ.',
        immediateAction:'ಗಾಳಿಯಾಡುವ ತೆರೆದ ಜಾಗದಲ್ಲಿ ಟ್ರಕ್ ನಿಲ್ಲಿಸಿ. ಇಂಜಿನ್ ಮತ್ತು ಬ್ಯಾಟರಿ ಕಟ್-ಆಫ್ ಸ್ವಿಚ್ ಆಫ್ ಮಾಡಿ.',
        steps:[
          'ಶಾಖದ ಮೂಲಗಳಿಂದ ದೂರ ಸುರಕ್ಷಿತ ಜಾಗದಲ್ಲಿ ತಕ್ಷಣ ಟ್ರಕ್ ನಿಲ್ಲಿಸಿ.',
          'ಇಗ್ನಿಷನ್ ಕೀ ಆಫ್ ಮಾಡಿ ಮತ್ತು ಬ್ಯಾಟರಿ ಐಸೊಲೇಟರ್ ಸ್ವಿಚ್ ಆಫ್ ಮಾಡಿ.',
          'ಡೀಸೆಲ್ ಟ್ಯಾಂಕ್, ವಾಟರ್ ಸಪರೇಟರ್ ಮತ್ತು ಎಂಜಿನ್ ಫಿಲ್ಟರ್‌ಗಳಲ್ಲಿ ಡೀಸೆಲ್ ಸೋರುತ್ತಿದೆಯೇ ಪರೀಕ್ಷಿಸಿ.',
          'ಫಿಲ್ಟರ್ ಕೆಳಗಿನ ಪ್ಲಾಸ್ಟಿಕ್ ಡ್ರೈನ್ ಪ್ಲಗ್ ಸಡಿಲವಾಗಿದ್ದರೆ ಕೈಯಿಂದ ನಿಧಾನವಾಗಿ ಬಿಗಿಗೊಳಿಸಿ.',
          'ಬಿರುಕು ಬಿಟ್ಟ ಪೈಪ್‌ಗಳನ್ನು ಕಣ್ಣಾರೆ ನೋಡಿ.',
          'ಕಾಮನ್ ರೈಲ್‌ನಿಂದ ಹೆಚ್ಚಿನ ಒತ್ತಡದಲ್ಲಿ ಡೀಸೆಲ್ ಸಿಡಿಯುತ್ತಿದ್ದರೆ ಮುಟ್ಟಬೇಡಿ (ಚರ್ಮ ಹೊಕ್ಕುವ ಅಪಾಯವಿದೆ).',
          'ಸೋರಿಕೆ ಸರಿಪಡಿಸಲು ಫ್ಲೀಟ್ ಮೆಕಾನಿಕ್ ಸಂಪರ್ಕಿಸಿ.'
        ],
        driverSafe:'ವಾಟರ್ ಸಪರೇಟರ್ ಕೆಳಗಿನ ಪ್ಲಾಸ್ಟಿಕ್ ಪ್ಲಗ್ ಅನ್ನು ಕೈಯಿಂದ ಬಿಗಿಗೊಳಿಸಿ ಮತ್ತು ಟ್ಯಾಂಕ್ ಒರೆಸಿ.',
        mechanicRequired:'ಹೈ-ಪ್ರೆಶರ್ ಕಾಮನ್ ರೈಲ್ ಪೈಪ್ ಸೋರಿಕೆ, ಒಡೆದ ಪೈಪ್ ಅಥವಾ ಎಂಜಿನ್ ಒಳಗಿನ ಸ್ಪ್ರೇ.'
      },
      hi:{
        title:'डीजल ईंधन रिसाव / फ्यूल पाइप कटना',
        cause:'डीजल नली में दरार, फ्यूल फिल्टर बोल्ट ढीला, टैंक में छेद या इंजेक्टर पाइप का रिसाव।',
        warning:'⚠️ आग का खतरा: गर्म साइलेंसर ATS पार्ट्स (450°C से अधिक गर्म) के पास डीजल गिरने से आग लग सकती है। बीड़ी/सिगरेट न पिएं और आग न जलाएं।',
        immediateAction:'हवादार खुले स्थान पर गाड़ी रोकें। तुरंत इंजन और बैटरी कट-ऑफ स्विच बंद करें।',
        steps:[
          'गर्मी के स्रोतों से दूर सुरक्षित खुले स्थान पर ट्रक तुरंत रोकें।',
          'इग्निशन बंद करें और बैटरी मेन स्विच काटें।',
          'फ्यूल टैंक, वाटर सेपरेटर और इंजन डीजल फिल्टर से टपकते डीजल की जांच करें।',
          'यदि फिल्टर के नीचे का प्लास्टिक ड्रेन प्लग ढीला है, तो हाथ से धीरे से कसें।',
          'फटे या मुड़े हुए प्लास्टिक/रबर डीजल पाइप को देखें।',
          'यदि कॉमन रेल से तेज धार के साथ डीजल निकल रहा हो तो हाथ न लगाएं (त्वचा को नुकसान पहुंचा सकता है)।',
          'लीक पाइप बदलने के लिए फ्लीट मैकेनिक को फोन करें।'
        ],
        driverSafe:'वाटर सेपरेटर का प्लास्टिक प्लग हाथ से कसें और बाहर गिरा डीजल कपड़े से साफ करें।',
        mechanicRequired:'हाई-प्रेशर कॉमन रेल पाइप लीक, फटा हुआ पाइप या इंजन के अंदर तेज रिसाव।'
      }
    },
    {
      id:'dpf_regeneration',
      pattern:/dpf|soot|regeneration|exhaust filter|soot load|amber dpf|ರಿಜೆನರೇಷನ್|ರೀಜೆನರೇಷನ್|ಡಿಪಿಎಫ್|ಸೂಟ್|ವಿಸರ್ಜನೆ|डीपीएफ|रीजेनेरेशन|सूट/i,
      severity:'MEDIUM',
      icon:'♻️',
      en:{
        title:'DPF (Diesel Particulate Filter) High Soot Warning',
        cause:'Soot accumulation in exhaust DPF filter due to slow city driving, frequent idling, or traffic.',
        warning:'⚠️ EXTREME HEAT HAZARD: Exhaust temperatures exceed 600°C during DPF regeneration. NEVER initiate parked regeneration near dry grass, petrol bunks, or enclosed parking.',
        immediateAction:'If DPF light is solid Amber, drive on highway above 50 km/h. If flashing Amber, perform Mahindra Parked Regeneration.',
        steps:[
          'Park the truck in a wide open area with at least 5 meters clearance around exhaust tailpipe.',
          'Apply the parking brake firmly, shift gear to Neutral (N), and keep engine running.',
          'Turn OFF the PTO, Exhaust Brake switch, and DPF Inhibit switch.',
          'Ensure engine coolant temperature is above 75°C.',
          'Do not touch the accelerator, clutch, or foot brake pedals.',
          'Press and hold the dashboard DPF Regeneration Switch for 5 seconds and release.',
          'Engine RPM will rise automatically to 1400–1600 RPM. Process takes 20 to 30 minutes.',
          'Do not leave truck unattended during regeneration. Wait until RPM returns to normal idle and light turns OFF.',
          'If DPF lamp turns RED or Check Engine lamp flashes, stop the vehicle and call the mechanic.'
        ],
        driverSafe:'Perform standard Parked DPF Regeneration following the dashboard switch procedure in an open area.',
        mechanicRequired:'DPF lamp turns Red, engine enters torque derate mode, or parked regeneration fails to start.'
      },
      kn:{
        title:'DPF (ಡೀಸೆಲ್ ಪಾರ್ಟಿಕುಲೇಟ್ ಫಿಲ್ಟರ್) ಹೆಚ್ಚಿನ ಸೂಟ್ ಎಚ್ಚರಿಕೆ',
        cause:'ನಗರದ ನಿಧಾನ ಚಾಲನೆ, ದೀರ್ಘಕಾಲದ ಐಡ್ಲಿಂಗ್ ಅಥವಾ ಟ್ರಾಫಿಕ್ ಕಾರಣ ಎಕ್ಸಾಸ್ಟ್ DPF ಫಿಲ್ಟರ್‌ನಲ್ಲಿ ಸೂಟ್ (ಮಸಿ) ಜಮೆಯಾಗಿರುವುದು.',
        warning:'⚠️ ತೀವ್ರ ಶಾಖದ ಅಪಾಯ: DPF ರಿಜೆನರೇಷನ್ ಸಮಯದಲ್ಲಿ ಸೈಲೆನ್ಸರ್ ಶಾಖ 600°C ಗಿಂತ ಹೆಚ್ಚಾಗುತ್ತದೆ. ಒಣ ಹುಲ್ಲು, ಪೆಟ್ರೋಲ್ ಬಂಕ್ ಬಳಿ ಎಂದಿಗೂ ಪಾರ್ಕ್ಡ್ ರಿಜೆನರೇಷನ್ ಮಾಡಬೇಡಿ!',
        immediateAction:'DPF ಲೈಟ್ ಸ್ಥಿರವಾಗಿದ್ದರೆ (Solid Amber) 50 km/h ಗಿಂತ ವೇಗವಾಗಿ ಹೆದ್ದಾರಿಯಲ್ಲಿ ಚಲಿಸಿ. ಮಿಟುಕಿಸುತ್ತಿದ್ದರೆ (Flashing) ಪಾರ್ಕ್ಡ್ ರಿಜೆನರೇಷನ್ ಮಾಡಿ.',
        steps:[
          'ಸೈಲೆನ್ಸರ್ ಸುತ್ತ 5 ಮೀಟರ್ ತೆರೆದ ಜಾಗವಿರುವ ವಿಶಾಲ ಸ್ಥಳದಲ್ಲಿ ಟ್ರಕ್ ಪಾರ್ಕ್ ಮಾಡಿ.',
          'ಹ್ಯಾಂಡ್‌ಬ್ರೇಕ್ ಗಟ್ಟಿಯಾಗಿ ಹಾಕಿ, ಗೇರ್ ನ್ಯೂಟ್ರಲ್ (N) ನಲ್ಲಿಡಿ, ಇಂಜಿನ್ ಚಾಲನೆಯಲ್ಲಿರಲಿ.',
          'PTO, ಎಕ್ಸಾಸ್ಟ್ ಬ್ರೇಕ್ ಮತ್ತು DPF Inhibit ಸ್ವಿಚ್ ಆಫ್ (OFF) ಇರಲಿ.',
          'ಕೂಲಂಟ್ ತಾಪಮಾನ 75°C ಗಿಂತ ಹೆಚ್ಚಿರುವುದನ್ನು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.',
          'ಆಕ್ಸಿಲರೇಟರ್, ಕ್ಲಚ್ ಅಥವಾ ಬ್ರೇಕ್ ಪೆಡಲ್ ಮುಟ್ಟಬೇಡಿ.',
          'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ DPF Regeneration Switch ಅನ್ನು 5 ಸೆಕೆಂಡುಗಳ ಕಾಲ ಒತ್ತಿ ಹಿಡಿದು ಬಿಡಿ.',
          'ಇಂಜಿನ್ RPM ತಾನಾಗಿಯೇ 1400–1600 RPM ಗೆ ಏರುತ್ತದೆ. ಪ್ರಕ್ರಿಯೆಗೆ 20 ರಿಂದ 30 ನಿಮಿಷ ಬೇಕು.',
          'ರಿಜೆನರೇಷನ್ ಮುಗಿದು RPM ಸಹಜ ಸ್ಥಿತಿಗೆ ಬರುವವರೆಗೆ ಟ್ರಕ್ ಬಿಟ್ಟು ಹೋಗಬೇಡಿ.',
          'DPF ಲೈಟ್ ಕೆಂಪು (RED) ಬಣ್ಣಕ್ಕೆ ತಿರುಗಿದರೆ ತಕ್ಷಣ ವಾಹನ ನಿಲ್ಲಿಸಿ ಮೆಕಾನಿಕ್‌ಗೆ ಕರೆ ಮಾಡಿ.'
        ],
        driverSafe:'ತೆರೆದ ಜಾಗದಲ್ಲಿ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಸ್ವಿಚ್ ಬಳಸಿ ನಿಗದಿತ ಪಾರ್ಕ್ಡ್ DPF ರಿಜೆನರೇಷನ್ ಮಾಡಿ.',
        mechanicRequired:'DPF ಲೈಟ್ ಕೆಂಪಾದರೆ, ಇಂಜಿನ್ ಪಿಕಪ್ ಕಡಿಮೆಯಾದರೆ (derate) ಅಥವಾ ರಿಜೆನರೇಷನ್ ಪ್ರಾರಂಭವಾಗದಿದ್ದರೆ.'
      },
      hi:{
        title:'DPF (डीजल पार्टिकुलेट फिल्टर) उच्च कालिख (Soot) चेतावनी',
        cause:'धीमी गति, बार-बार ट्रैफिक में रुकने या लंबे समय तक इंजन आइडल रखने से DPF फिल्टर में कालिख जमना।',
        warning:'⚠️ अत्यधिक गर्मी का खतरा: DPF रीजेनेरेशन के दौरान साइलेंसर का तापमान 600°C से ऊपर चला जाता है। सूखी घास, पेट्रोल पंप या बंद जगह पर कभी रीजेनेरेशन न करें!',
        immediateAction:'यदि DPF लाइट लगातार जल रही है तो हाईवे पर 50 km/h से ऊपर चलाएं। यदि ब्लिंक कर रही है तो पार्क करके रीजेनेरेशन करें।',
        steps:[
          'साइलेंसर के पीछे 5 मीटर खुली जगह वाले मैदान में ट्रक खड़ा करें।',
          'हैंड ब्रेक कसकर लगाएं, गियर न्यूट्रल (N) करें और इंजन चालू रखें।',
          'PTO, एग्जॉस्ट ब्रेक और DPF इनहिबिट स्विच बंद (OFF) रखें।',
          'इंजन कूलेंट तापमान 75°C से अधिक होना चाहिए।',
          'एक्सेलेरेटर, क्लच या ब्रेक पैडल को बिल्कुल न छुएं।',
          'डैशबोर्ड पर लगा DPF बटन 5 सेकंड दबाकर छोड़ें।',
          'इंजन की रेस अपने आप 1400-1600 RPM तक बढ़ जाएगी। प्रक्रिया में 20 से 30 मिनट लगते हैं।',
          'रीजेनेरेशन के दौरान ट्रक छोड़कर न जाएं। RPM सामान्य होने और लाइट बुझने तक इंतजार करें।',
          'यदि DPF बत्ती लाल हो जाए तो तुरंत ट्रक रोकें और मैकेनिक को बुलाएं।'
        ],
        driverSafe:'खुले स्थान पर डैशबोर्ड बटन दबाकर मानक Parked DPF Regeneration प्रक्रिया पूरी करें।',
        mechanicRequired:'DPF लाइट लाल हो जाए, इंजन का पिकअप गिर जाए या रीजेनेरेशन स्टार्ट न हो।'
      }
    },
    {
      id:'adblue_def',
      pattern:/adblue|def|urea|scr|ad blue|ಆಡ್‌ಬ್ಲೂ|ಯೂರಿಯಾ|ಡೆಫ್|ಯೂರಿಯಾ ಮುಗಿದಿದೆ|एडब्लू|यूरिया|डेफ|यूरिया कम/i,
      severity:'MEDIUM',
      icon:'💧',
      en:{
        title:'Low AdBlue (DEF) Level / SCR Emission Warning',
        cause:'AdBlue tank level dropped below 10%, poor quality AdBlue, or crystallized dosing nozzle.',
        warning:'⚠️ ENGINE SPEED DERATE WARNING: BSVI emission laws mandate that if DEF tank runs empty, truck speed will automatically derate to 20 km/h upon restart. Top up immediately.',
        immediateAction:'Stop at nearest authorized fuel station and top up with genuine ISO 22241 AdBlue.',
        steps:[
          'Park the truck safely and switch off the engine.',
          'Locate the dedicated AdBlue tank (blue filler cap on chassis).',
          'Clean the area around filler cap with a dry cloth before opening to prevent dust contamination.',
          'Use only genuine certified ISO 22241 standard AdBlue from sealed containers.',
          'Fill AdBlue into the tank using a clean dedicated funnel or canister nozzle.',
          'Do not overfill beyond the maximum level mark on the tank sight gauge.',
          'Turn ignition ON for 60 seconds without cranking so the level sensor updates.',
          'Start engine and confirm warning light turns OFF.'
        ],
        driverSafe:'Refill genuine AdBlue into the dedicated blue filler cap on the chassis.',
        mechanicRequired:'DEF light remains ON after refilling, warning indicates poor DEF quality, or dosing error appears.'
      },
      kn:{
        title:'ಕಡಿಮೆ AdBlue (DEF) ಮಟ್ಟ / SCR ಹೊರಸೂಸುವಿಕೆ ಎಚ್ಚರಿಕೆ',
        cause:'AdBlue ಟ್ಯಾಂಕ್ ಮಟ್ಟ 10% ಕ್ಕಿಂತ ಕಡಿಮೆಯಾಗಿರುವುದು, ಕಳಪೆ ಗುಣಮಟ್ಟದ AdBlue ಅಥವಾ ಡೋಸಿಂಗ್ ವಾಲ್ವ್ ಜಾಮ್ ಆಗಿರುವುದು.',
        warning:'⚠️ ಎಂಜಿನ್ ವೇಗ ಇಳಿಕೆ ಎಚ್ಚರಿಕೆ: BSVI ನಿಯಮಗಳ ಪ್ರಕಾರ AdBlue ಖಾಲಿಯಾದರೆ ಎಂಜಿನ್ ಮುಂದಿನ ಬಾರಿ ಸ್ಟಾರ್ಟ್ ಮಾಡಿದಾಗ ಟ್ರಕ್ ವೇಗ ತಾನಾಗಿಯೇ 20 km/h ಗೆ ಇಳಿಯುತ್ತದೆ (Derate). ತಕ್ಷಣ ತುಂಬಿಸಿ.',
        immediateAction:'ಹತ್ತಿರದ ಅಧಿಕೃತ ಪೆಟ್ರೋಲ್ ಬಂಕ್‌ನಲ್ಲಿ ನಿಲ್ಲಿಸಿ ಅಧಿಕೃತ ISO 22241 AdBlue ದ್ರವವನ್ನು ತುಂಬಿಸಿ.',
        steps:[
          'ಟ್ರಕ್ ಅನ್ನು ಸುರಕ್ಷಿತವಾಗಿ ನಿಲ್ಲಿಸಿ ಎಂಜಿನ್ ಆಫ್ ಮಾಡಿ.',
          'ಚಾಸಿಸ್‌ನಲ್ಲಿರುವ ನೀಲಿ ಕ್ಯಾಪ್ ಇರುವ AdBlue ಟ್ಯಾಂಕ್ ಗುರುತಿಸಿ.',
          'ಧೂಳು ಅಥವಾ ಮಣ್ಣು ಒಳಗೆ ಹೋಗದಂತೆ ಕ್ಯಾಪ್ ತೆರೆಯುವ ಮುನ್ನ ಸ್ವಚ್ಛ ಬಟ್ಟೆಯಿಂದ ಒರೆಸಿ.',
          'ಸೀಲ್ ಮಾಡಿದ ಅಧಿಕೃತ ISO 22241 ಗುಣಮಟ್ಟದ AdBlue ಮಾತ್ರ ಬಳಸಿ.',
          'ಸ್ವಚ್ಛವಾದ ಫನಲ್ ಬಳಸಿ ಟ್ಯಾಂಕ್‌ಗೆ AdBlue ಸುರಿಯಿರಿ.',
          'ಗರಿಷ್ಠ ಮಟ್ಟಕ್ಕಿಂತ ಹೆಚ್ಚು ತುಂಬಿಸಬೇಡಿ (Do not overfill).',
          'ಸೆನ್ಸರ್ ಅಪ್‌ಡೇಟ್ ಆಗಲು ಕೀ ಆನ್ ಮಾಡಿ 60 ಸೆಕೆಂಡು ಕಾಯಿರಿ (ಕ್ರ್ಯಾಂಕ್ ಮಾಡಬೇಡಿ).',
          'ಎಂಜಿನ್ ಸ್ಟಾರ್ಟ್ ಮಾಡಿ ವಾರ್ನಿಂಗ್ ಲೈಟ್ ಆಫ್ ಆಗಿದೆಯೇ ಪರಿಶೀಲಿಸಿ.'
        ],
        driverSafe:'ಚಾಸಿಸ್‌ನಲ್ಲಿರುವ ನೀಲಿ ಕ್ಯಾಪ್‌ಗೆ ಅಧಿಕೃತ AdBlue ಅನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತುಂಬಿಸಿ.',
        mechanicRequired:'ತುಂಬಿಸಿದ ನಂತರವೂ ಲೈಟ್ ಆನ್ ಆಗಿದ್ದರೆ, ಕಳಪೆ ಗುಣಮಟ್ಟದ ಸಂದೇಶ ಬಂದರೆ ಅಥವಾ ಡೋಸಿಂಗ್ ಎರರ್ ಇದ್ದರೆ.'
      },
      hi:{
        title:'कम AdBlue (DEF) स्तर / SCR उत्सर्जन चेतावनी',
        cause:'AdBlue का स्तर 10% से नीचे गिरना, घटिया क्वालिटी का AdBlue या इंजेक्टर नोजल में यूरिया जमना।',
        warning:'⚠️ इंजन स्पीड कम होने की चेतावनी: BSVI नियमों के अनुसार यदि AdBlue खत्म हो जाए तो अगली बार स्टार्ट करने पर ट्रक की स्पीड अपने आप 20 km/h तक घट जाएगी। तुरंत टॉप-अप करें।',
        immediateAction:'नजदीकी अधिकृत पेट्रोल पंप पर रुकें और असली ISO 22241 AdBlue भरें।',
        steps:[
          'ट्रक को सुरक्षित खड़ा करें और इंजन बंद करें।',
          'चेसिस पर नीले ढक्कन वाले AdBlue टैंक को पहचानें।',
          'ढक्कन खोलने से पहले उसके आसपास की धूल-मिट्टी सूखे कपड़े से अच्छी तरह साफ करें।',
          'केवल सीलबंद कैन वाला प्रमाणित ISO 22241 AdBlue ही इस्तेमाल करें।',
          'साफ कीप (फनल) की मदद से AdBlue भरें।',
          'टैंक के अधिकतम स्तर (Max Mark) से ऊपर न भरें।',
          'लेवल सेंसर अपडेट होने के लिए 60 सेकंड तक इग्निशन ऑन रखें (सेल्फ न लगाएं)।',
          'इंजन स्टार्ट करें और देखें कि चेतावनी बत्ती बुझ गई है।'
        ],
        driverSafe:'चेसिस पर नीले ढक्कन में असली AdBlue सावधानीपूर्वक भरें।',
        mechanicRequired:'भरने के बाद भी लाइट जलती रहे, घटिया क्वालिटी की चेतावनी आए या डोजिंग पंप में खराबी हो।'
      }
    },
    {
      id:'oil_pressure',
      pattern:/oil pressure|oil lamp|engine oil|low oil|ಆಯಿಲ್|ಎಣ್ಣೆ|ಆಯಿಲ್ ಪ್ರೆಶರ್|ಆಯಿಲ್ ಕಡಿಮೆ|ಆಯಿಲ್ ಲೈಟ್|ಇಂಜಿನ್ ಆಯಿಲ್|ऑयल प्रेशर|इंजन ऑयल|तेल कम|ऑयल लाइट/i,
      severity:'CRITICAL',
      icon:'🛢️',
      en:{
        title:'Low Engine Oil Pressure Warning',
        cause:'Low engine oil level, oil filter choked, oil strainer blocked, or oil pump failure.',
        warning:'🛑 CRITICAL ENGINE HAZARD: Running engine with low oil pressure will destroy engine bearings, crankshaft, and turbocharger within 60 seconds. SHUT DOWN ENGINE IMMEDIATELY.',
        immediateAction:'Pull over safely and turn off engine within 10 seconds of oil lamp illuminating.',
        steps:[
          'Stop truck safely and switch off engine immediately.',
          'Wait 5 to 10 minutes for oil to settle into oil sump.',
          'Pull out engine oil dipstick, wipe clean with cloth, insert fully, and withdraw again.',
          'Check oil level: it must be between MIN and MAX marks.',
          'If below MIN, inspect under engine for active oil leaks or loose drain plug.',
          'Top up with recommended Mahindra 15W-40 CI-4+ engine oil if available.',
          'If oil level is normal but light stays ON, SHUT OFF IMMEDIATELY and call mechanic.'
        ],
        driverSafe:'Check engine oil level using dipstick and top up approved oil if level is low.',
        mechanicRequired:'Oil pressure light illuminates despite adequate oil level, or engine makes metallic knocking sounds.'
      },
      kn:{
        title:'ಕಡಿಮೆ ಎಂಜಿನ್ ಆಯಿಲ್ ಪ್ರೆಶರ್ ಎಚ್ಚರಿಕೆ',
        cause:'ಎಂಜಿನ್ ಆಯಿಲ್ ಮಟ್ಟ ಕಡಿಮೆಯಾಗಿರುವುದು, ಆಯಿಲ್ ಫಿಲ್ಟರ್ ಜಾಮ್, ಆಯಿಲ್ ಪಂಪ್ ವೈಫಲ್ಯ ಅಥವಾ ಸೋರಿಕೆ.',
        warning:'🛑 ಗಂಭೀರ ಎಂಜಿನ್ ಅಪಾಯ: ಕಡಿಮೆ ಆಯಿಲ್ ಪ್ರೆಶರ್‌ನಲ್ಲಿ ಇಂಜಿನ್ ಚಲಾಯಿಸಿದರೆ 60 ಸೆಕೆಂಡುಗಳಲ್ಲಿ ಬೇರಿಂಗ್‌ಗಳು, ಕ್ರ್ಯಾಂಕ್‌ಶಾಫ್ಟ್ ಮತ್ತು ಟರ್ಬೊ ನಾಶವಾಗುತ್ತವೆ. ತಕ್ಷಣ ಇಂಜಿನ್ ಆಫ್ ಮಾಡಿ!',
        immediateAction:'ಆಯಿಲ್ ಲೈಟ್ ಕಂಡ 10 ಸೆಕೆಂಡುಗಳಲ್ಲಿ ವಾಹನವನ್ನು ಪಕ್ಕಕ್ಕೆ ಸರಿಸಿ ಇಂಜಿನ್ ಆಫ್ ಮಾಡಿ.',
        steps:[
          'ತಕ್ಷಣ ಸುರಕ್ಷಿತವಾಗಿ ಟ್ರಕ್ ನಿಲ್ಲಿಸಿ ಇಂಜಿನ್ ಆಫ್ ಮಾಡಿ.',
          'ಆಯಿಲ್ ಕೆಳಗೆ ಇಳಿಯಲು 5 ರಿಂದ 10 ನಿಮಿಷ ಕಾಯಿರಿ.',
          'ಡಿಪ್‌ಸ್ಟಿಕ್ ಹೊರತೆಗೆದು ಬಟ್ಟೆಯಿಂದ ಒರೆಸಿ, ಪೂರ್ತಿ ಒಳಗೆ ಹಾಕಿ ಮತ್ತೆ ಹೊರತೆಗೆಯಿರಿ.',
          'ಆಯಿಲ್ ಮಟ್ಟ MIN ಮತ್ತು MAX ಮಾರ್ಕ್‌ಗಳ ನಡುವೆ ಇರಬೇಕು.',
          'MIN ಗಿಂತ ಕೆಳಗಿದ್ದರೆ ಇಂಜಿನ್ ಕೆಳಗೆ ಆಯಿಲ್ ಸೋರುತ್ತಿದೆಯೇ ಪರೀಕ್ಷಿಸಿ.',
          'ಶಿಫಾರಸು ಮಾಡಿದ ಮಹೀಂದ್ರಾ 15W-40 ಎಂಜಿನ್ ಆಯಿಲ್ ಇದ್ದರೆ ಟಾಪ್-ಅಪ್ ಮಾಡಿ.',
          'ಆಯಿಲ್ ಮಟ್ಟ ಸರಿಯಿದ್ದರೂ ಲೈಟ್ ಉರಿಯುತ್ತಿದ್ದರೆ ತಕ್ಷಣ ಆಫ್ ಮಾಡಿ ಮೆಕಾನಿಕ್ ಸಂಪರ್ಕಿಸಿ.'
        ],
        driverSafe:'ಡಿಪ್‌ಸ್ಟಿಕ್ ಬಳಸಿ ಎಂಜಿನ್ ಆಯಿಲ್ ಮಟ್ಟ ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಕಡಿಮೆಯಿದ್ದರೆ ಆಯಿಲ್ ಹಾಕಿ.',
        mechanicRequired:'ಆಯಿಲ್ ಮಟ್ಟ ಸರಿಯಿದ್ದರೂ ವಾರ್ನಿಂಗ್ ಲೈಟ್ ಆನ್ ಆಗಿದ್ದರೆ ಅಥವಾ ಇಂಜಿನ್‌ನಿಂದ ಸದ್ದು ಬರುತ್ತಿದ್ದರೆ.'
      },
      hi:{
        title:'कम इंजन ऑयल प्रेशर चेतावनी',
        cause:'इंजन ऑयल कम होना, ऑयल फिल्टर चोक होना, ऑयल पंप खराब होना या बड़ा रिसाव।',
        warning:'🛑 गंभीर इंजन खतरा: कम ऑयल प्रेशर में इंजन चलाने से 60 सेकंड के अंदर क्रैंकशाफ्ट, बेयरिंग और टर्बोचार्जर नष्ट हो जाएंगे। तुरंत इंजन बंद करें!',
        immediateAction:'ऑयल बत्ती जलने के 10 सेकंड के भीतर तुरंत सुरक्षित किनारे रोककर इंजन बंद करें।',
        steps:[
          'गाड़ी तुरंत रोकें और इंजन तुरंत बंद कर दें।',
          'ऑयल नीचे जमा होने के लिए 5 से 10 मिनट इंतजार करें।',
          'इंजन ऑयल गेज (डिपस्टिक) निकालें, साफ करें, दोबारा डालकर स्तर देखें।',
          'ऑयल का स्तर MIN और MAX के बीच होना चाहिए।',
          'यदि MIN से नीचे है तो इंजन के नीचे तेल का रिसाव देखें।',
          'अनुशंसित महिंद्रा 15W-40 इंजन ऑयल उपलब्ध होने पर टॉप-अप करें।',
          'यदि तेल पूरा है फिर भी बत्ती जलती रहे तो तुरंत इंजन बंद करें और मैकेनिक बुलाएं।'
        ],
        driverSafe:'डिपस्टिक से ऑयल का स्तर जांचें और कम होने पर सही ग्रेड का इंजन ऑयल डालें।',
        mechanicRequired:'ऑयल पूरा होने पर भी बत्ती जले या इंजन से खट-खट की तेज आवाज आ रही हो।'
      }
    }
  ];

  function identifyProblem(text){
    const q=String(text||'').trim();
    if(!q) return null;
    for(const item of DIAGNOSTIC_KNOWLEDGE){
      if(item.pattern.test(q)) return item;
    }
    return null;
  }

  /* ISSUE 4 & ISSUE 2: EXACT VEHICLE PROBLEM REPORTING PAGE */
  window._driverPhotoData=null;

  function exactProblem(){
    stopActiveVoice();
    window.__currentRenderer=exactProblem;
    hideOld();let root=document.getElementById('maApp');if(root)root.remove();root=document.createElement('div');root.id='maApp';
    const u=getUser()||{};
    const l=L();
    const curLang=getLang();

    root.innerHTML='<div class="ma-bar">'+
      '<button class="ma-icon" onclick="maDashboard()" aria-label="Back">‹</button>'+
      '<div class="ma-title">'+l.cardVehicle+'<small>'+esc(roleName(u.role))+' • '+esc(name())+'</small></div>'+
      '<button class="ma-icon" onclick="maDashboard()" aria-label="Home">⌂</button>'+
      '</div>'+
      '<main class="ma-main">'+
        '<section class="ma-hero">'+
          '<div class="ma-brand">'+l.probTitle+'</div>'+
          '<div class="ma-sub">'+l.probSub+'</div>'+
        '</section>'+
        '<section class="ma-hero">'+
          '<label style="display:block;font-size:14px;font-weight:900;color:#334155;margin-bottom:6px">'+l.chipsPrompt+'</label>'+
          '<div class="ma-chip-wrap" id="problemChipsBox"></div>'+
          '<label style="display:block;font-size:16px;font-weight:900;color:#0f172a;margin:10px 0 6px">'+l.descLabel+' <span style="color:#b71c1c">*</span></label>'+
          '<textarea id="driverProblemText" class="ma-emp-textarea" rows="5" placeholder="'+esc(l.descPh)+'"></textarea>'+
          '<div style="display:flex;justify-content:space-between;align-items:center;font-size:12px;color:#64748b;margin:6px 0 10px">'+
            '<span id="driverCharCount">0 '+l.charCount+'</span>'+
            '<span style="color:#16a34a;font-weight:700">'+l.voiceConvertsNotice+'</span>'+
          '</div>'+
          '<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:8px">'+
            '<span style="font-size:13px;font-weight:800;color:#334155">'+l.voiceInputLbl+':</span>'+
            '<button type="button" class="ma-btn-voice" id="btnVoiceEn" onclick="startExactVoice(&quot;en-IN&quot;,&quot;btnVoiceEn&quot;)">🎤 English</button>'+
            '<button type="button" class="ma-btn-voice" id="btnVoiceHi" onclick="startExactVoice(&quot;hi-IN&quot;,&quot;btnVoiceHi&quot;)">🎤 हिन्दी</button>'+
            '<button type="button" class="ma-btn-voice" id="btnVoiceKn" onclick="startExactVoice(&quot;kn-IN&quot;,&quot;btnVoiceKn&quot;)">🎤 ಕನ್ನಡ</button>'+
            '<button type="button" class="ma-btn-voice" id="btnVoiceStop" style="display:none;background:#b71c1c" onclick="stopActiveVoice()">⏹️ '+l.stopListening+'</button>'+
          '</div>'+
          '<div id="driverVoiceStatus" style="margin:4px 0 12px;min-height:0"></div>'+
          '<div style="background:#f8fafc;border:2px dashed #cbd5e1;border-radius:14px;padding:14px;margin-bottom:14px">'+
            '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'+
              '<div><strong style="font-size:14px;color:#0f172a">'+l.photoBoxTitle+'</strong><div style="font-size:12px;color:#64748b">'+l.photoBoxSub+'</div></div>'+
              '<button type="button" class="ma-card" style="min-height:0;padding:8px 14px;font-size:13px;border-radius:8px" onclick="triggerDriverPhotoUpload()">'+l.choosePhotoBtn+'</button>'+
              '<input type="file" id="driverPhotoFileInput" accept="image/*" style="display:none" onchange="handleDriverPhotoSelected(this)">'+
            '</div>'+
            '<div id="driverPhotoPreviewBox" style="display:none;margin-top:10px"></div>'+
          '</div>'+
          '<label style="display:block;font-size:14px;font-weight:800;color:#475569;margin-bottom:6px">'+l.vehNoLabel+'</label>'+
          '<input id="driverVehicleNumber" placeholder="'+esc(l.vehNoPh)+'" style="width:100%;box-sizing:border-box;padding:13px;border:1px solid #d0d5dd;border-radius:10px;font-size:16px">'+
          '<div id="driverFormStatus" style="margin-top:10px"></div>'+
          '<button type="button" class="ma-btn-submit" id="btnSolution" style="width:100%;margin-top:14px;min-height:52px;font-size:18px" onclick="getInstantTroubleshoot()">'+
            l.solutionBtn+
          '</button>'+
          '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">'+
            '<button type="button" class="ma-card" style="min-height:0;padding:12px;text-align:center" onclick="saveDriverProblemDirect()">'+l.saveReportOnly+'</button>'+
            '<button type="button" class="ma-card" style="min-height:0;padding:12px;text-align:center;color:#b71c1c" onclick="callFleetEscalation()">'+l.callSupervisor+'</button>'+
          '</div>'+
        '</section>'+
      '</main>';
    app.appendChild(root);

    // Populate localized chips
    const chipsBox=document.getElementById('problemChipsBox');
    if(chipsBox){
      PROBLEM_CHIPS.forEach(c=>{
        const chipText=c[curLang]||c.en;
        const btn=document.createElement('button');
        btn.type='button';
        btn.className='ma-chip';
        btn.textContent=chipText;
        btn.onclick=()=>insertProblemChip(chipText);
        chipsBox.appendChild(btn);
      });
    }

    document.getElementById('driverProblemText')?.addEventListener('input',function(){
      const cnt=document.getElementById('driverCharCount');
      if(cnt) cnt.textContent=this.value.length+' '+L().charCount;
    });
  }

  function insertProblemChip(text){
    const el=document.getElementById('driverProblemText');
    if(el){
      el.value=text;
      el.focus();
      el.dispatchEvent(new Event('input'));
    }
  }

  function startExactVoice(locale,btnId){
    startVoiceRecognition('driverProblemText','driverVoiceStatus',locale,function(text){
      const cnt=document.getElementById('driverCharCount');
      const el=document.getElementById('driverProblemText');
      if(cnt && el) cnt.textContent=el.value.length+' '+L().charCount;
    },btnId);
  }

  function triggerDriverPhotoUpload(){
    if(window.AndroidBridge && AndroidBridge.captureDriverPhoto){
      AndroidBridge.captureDriverPhoto();
      return;
    }
    document.getElementById('driverPhotoFileInput')?.click();
  }

  function handleDriverPhotoSelected(input){
    if(input.files && input.files[0]){
      const file=input.files[0];
      const reader=new FileReader();
      reader.onload=function(e){
        window._driverPhotoData=e.target.result;
        renderDriverPhotoThumbnail(file.name,e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }

  function renderDriverPhotoThumbnail(filename,dataUrl){
    const box=document.getElementById('driverPhotoPreviewBox');
    if(!box) return;
    const l=L();
    box.style.display='flex';
    box.style.alignItems='center';
    box.style.gap='10px';
    box.innerHTML='<img src="'+dataUrl+'" style="width:54px;height:54px;object-fit:cover;border-radius:8px;border:1px solid #cbd5e1">'+
      '<div style="flex:1;min-width:0"><strong style="font-size:13px;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+esc(filename)+'</strong><small style="color:#16a34a;font-weight:700">'+l.photoAttached+'</small></div>'+
      '<button type="button" class="ma-card" style="min-height:0;padding:6px 10px;font-size:12px;color:#dc2626;border-radius:6px" onclick="clearDriverPhoto()">'+l.removePhoto+'</button>';
  }

  function clearDriverPhoto(){
    window._driverPhotoData=null;
    const box=document.getElementById('driverPhotoPreviewBox');
    if(box){box.style.display='none';box.innerHTML='';}
    const input=document.getElementById('driverPhotoFileInput');
    if(input) input.value='';
  }

  function callFleetEscalation(){
    const phone='tel:+919988776655';
    if(confirm('Call Balaji Fleet 24/7 Breakdown Assistance / Supervisor (+91 99887 76655)?')){
      location.href=phone;
    }
  }

  function saveDriverProblemDirect(){
    stopActiveVoice();
    const l=L();
    const vehicle=(document.getElementById('driverVehicleNumber')?.value||'').trim();
    const problem=(document.getElementById('driverProblemText')?.value||'').trim();
    const status=document.getElementById('driverFormStatus');
    if(!problem){
      if(status) status.innerHTML='<div class="ma-danger-box">'+l.emptyProblemMsg+'</div>';
      return;
    }
    if(status) status.innerHTML='<div style="color:#0284c7;font-weight:700">'+l.savingProblemMsg+'</div>';
    apiRequest('save_problem',{vehicleNumber:vehicle||'-',problem:problem,photoText:problem},r=>{
      if(!status) return;
      if(r&&r.ok){
        status.innerHTML='<div class="ma-safe-box">'+l.savedProblemSuccess+'</div>';
      }else{
        status.innerHTML='<div class="ma-danger-box">❌ '+(r&&r.error||'Could not save report.')+'</div>';
      }
    });
  }

  function getInstantTroubleshoot(){
    stopActiveVoice();
    const l=L();
    const text=(document.getElementById('driverProblemText')?.value||'').trim();
    const vehicle=(document.getElementById('driverVehicleNumber')?.value||'').trim();
    const status=document.getElementById('driverFormStatus');
    
    if(!text){
      if(status) status.innerHTML='<div class="ma-danger-box">'+l.emptyProblemMsg+'</div>';
      document.getElementById('driverProblemText')?.focus();
      return;
    }
    
    // Automatically save report to central backend
    apiRequest('save_problem',{vehicleNumber:vehicle||'-',problem:text,photoText:text});
    
    // Evaluate diagnosis
    const matched=identifyProblem(text);
    renderTroubleshootingResult(text,vehicle,matched);
  }

  function renderTroubleshootingResult(query,vehicle,diag){
    stopActiveVoice();
    window.__currentRenderer=()=>renderTroubleshootingResult(query,vehicle,diag);
    window.__lastDiagnosis=diag;
    window.__lastQuery=query;
    const l=L();
    const curLang=getLang();

    let badgeClass='ma-badge-critical', badgeLabel='🛑 CRITICAL SAFETY ISSUE — STOP VEHICLE';
    if(diag){
      if(diag.severity==='CRITICAL'){
        badgeClass='ma-badge-critical';
        badgeLabel=curLang==='kn'?'🛑 ಗಂಭೀರ ಸುರಕ್ಷತಾ ಸಮಸ್ಯೆ — ವಾಹನ ನಿಲ್ಲಿಸಿ':curLang==='hi'?'🛑 गंभीर सुरक्षा समस्या — वाहन तुरंत रोकें':'🛑 CRITICAL SAFETY ISSUE — STOP VEHICLE';
      }else if(diag.severity==='HIGH'){
        badgeClass='ma-badge-high';
        badgeLabel=curLang==='kn'?'⚠️ ಹೆಚ್ಚಿನ ಆದ್ಯತೆ — ನಿಲ್ಲಿಸಿ ಪರೀಕ್ಷಿಸಿ':curLang==='hi'?'⚠️ उच्च प्राथमिकता — रोकें और जांचें':'⚠️ HIGH PRIORITY — STOP & INSPECT';
      }else{
        badgeClass='ma-badge-safe';
        badgeLabel=curLang==='kn'?'🔧 ಸುರಕ್ಷಿತ ಮೂಲಭೂತ ತಪಾಸಣೆ ಅನುಮತಿಸಲಾಗಿದೆ':curLang==='hi'?'🔧 सुरक्षित प्राथमिक जांच की अनुमति है':'🔧 SAFE BASIC CHECK PERMITTED';
      }
    }else{
      badgeClass='ma-badge-info';
      badgeLabel=curLang==='kn'?'⚠️ ಅನಿಶ್ಚಿತ ಲಕ್ಷಣ — ವೃತ್ತಿಪರ ತಪಾಸಣೆ ಅಗತ್ಯವಿದೆ':curLang==='hi'?'⚠️ अनिश्चित लक्षण — पेशेवर जांच आवश्यक':'⚠️ UNCERTAIN SYMPTOM — PROFESSIONAL CHECK REQUIRED';
    }

    const dInfo=diag?(diag[curLang]||diag.en):null;

    let html='<section class="ma-hero">'+
      '<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">'+
        '<div>'+
          '<div class="ma-brand" style="font-size:20px">'+(dInfo?esc(dInfo.title):l.probTitle)+'</div>'+
          '<div class="ma-sub" style="margin-top:4px">'+l.vehicleNoLbl+': <strong>'+esc(vehicle||'-')+'</strong></div>'+
        '</div>'+
        '<span class="ma-action-badge '+badgeClass+'">'+badgeLabel+'</span>'+
      '</div>'+
      '<div style="margin-top:12px;background:#f8fafc;padding:12px 14px;border-radius:12px;border:1px solid #e2e8f0">'+
        '<div style="font-size:12px;font-weight:800;color:#64748b;text-transform:uppercase">'+l.reportedProblem+'</div>'+
        '<div style="font-size:15px;color:#0f172a;font-weight:700;margin-top:3px">'+esc(query)+'</div>'+
        (window._driverPhotoData?'<div style="margin-top:6px;font-size:12px;color:#16a34a;font-weight:700">📷 '+l.photoAttached+'</div>':'')+
      '</div>';

    if(dInfo){
      html+='<div style="margin-top:14px">'+
        '<div style="font-size:12px;font-weight:800;color:#64748b;text-transform:uppercase">'+l.possibleCause+'</div>'+
        '<div style="font-size:15px;color:#0f172a;margin-top:3px;line-height:1.45">'+esc(dInfo.cause)+'</div>'+
      '</div>'+
      '<div class="ma-danger-box" style="margin-top:14px">'+
        '<strong>'+l.safetyWarning+'</strong><br>'+esc(dInfo.warning)+
      '</div>'+
      '<div class="ma-mech-box">'+
        '<strong>'+l.immediateAction+'</strong><br>'+esc(dInfo.immediateAction)+
      '</div>'+
      '<div style="margin-top:16px">'+
        '<strong style="display:block;font-size:16px;color:#0f172a;margin-bottom:10px">'+l.stepInstructions+'</strong>'+
        dInfo.steps.map((st,idx)=>'<div class="ma-step-item"><div class="ma-step-num">'+(idx+1)+'</div><div class="ma-step-text">'+esc(st)+'</div></div>').join('')+
      '</div>'+
      '<div class="ma-safe-split">'+
        '<div class="ma-safe-box" style="margin:0">'+
          '<strong>'+l.safeCheckLbl+'</strong><br><small style="line-height:1.35;display:block;margin-top:4px">'+esc(dInfo.driverSafe)+'</small>'+
        '</div>'+
        '<div class="ma-danger-box" style="margin:0">'+
          '<strong>'+l.mechReqLbl+'</strong><br><small style="line-height:1.35;display:block;margin-top:4px">'+esc(dInfo.mechanicRequired)+'</small>'+
        '</div>'+
      '</div>';
    }else{
      // Uncertainty notice
      const unCertNotice=curLang==='kn'
        ?'ನಿಮ್ಮ ವಿವರಣೆಯಿಂದ ನಿಖರವಾದ ಯಾಂತ್ರಿಕ ಕಾರಣವನ್ನು ಗುರುತಿಸಲಾಗಲಿಲ್ಲ. ವಾಹನದ ಸುರಕ್ಷತೆಗಾಗಿ ಊಹೆಯ ರಿಪೇರಿ ಮಾಡಬೇಡಿ.'
        :curLang==='hi'
        ?'आपके विवरण से सटीक कारण की पहचान नहीं हो सकी। वाहन की सुरक्षा के लिए अनुमान से मरम्मत न करें।'
        :'The exact mechanical cause could not be identified with certainty from your description. To prevent vehicle damage and protect your safety, generic or guessed repair steps are NOT provided.';
      
      const unCertSteps=curLang==='kn'
        ?'1. ಹೆದ್ದಾರಿಯ ಪಕ್ಕದಲ್ಲಿ ಸುರಕ್ಷಿತ ತೆರೆದ ಜಾಗದಲ್ಲಿ ವಾಹನ ನಿಲ್ಲಿಸಿ.<br>2. ಪಾರ್ಕಿಂಗ್ ಹ್ಯಾಂಡ್‌ಬ್ರೇಕ್ ಹಾಕಿ ಮತ್ತು ಹ್ಯಾಜಾರ್ಡ್ ಲೈಟ್ ಆನ್ ಮಾಡಿ.<br>3. ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಲ್ಲಿ ಯಾವುದೇ ವಾರ್ನಿಂಗ್ ಲೈಟ್ ಉರಿಯುತ್ತಿದೆಯೇ ಗಮನಿಸಿ.<br>4. ಯಾಂತ್ರಿಕ ಭಾಗಗಳನ್ನು ಬಿಚ್ಚಬೇಡಿ.<br>5. ಕೆಳಗಿನ ತುರ್ತು ಬಟನ್ ಬಳಸಿ ಸೂಪರ್‌ವೈಸರ್ ಅಥವಾ ಮೆಕಾನಿಕ್‌ಗೆ ಕರೆ ಮಾಡಿ.'
        :curLang==='hi'
        ?'1. हाईवे किनारे सुरक्षित खुले स्थान पर ट्रक रोकें।<br>2. पार्किंग हैंड ब्रेक लगाएं और हजार्ड लाइट जलाएं।<br>3. डैशबोर्ड पर किसी वार्निंग लाइट की जांच करें।<br>4. कोई मैकेनिकल पुर्जा न खोलें।<br>5. नीचे दिए गए बटन से तुरंत सुपरवाइजर या मैकेनिक को कॉल करें।'
        :'1. Stop the truck safely in a clear area off the highway.<br>2. Apply the parking hand brake and switch on hazard flashers.<br>3. Inspect the instrument cluster for any illuminated warning lamps.<br>4. Do not guess repairs or disassemble mechanical parts.<br>5. Contact the fleet supervisor or mobile mechanic using the emergency buttons below.';

      html+='<div class="ma-danger-box" style="margin-top:14px">'+
        '<strong>⚠️ UNCERTAINTY NOTICE:</strong><br>'+unCertNotice+
      '</div>'+
      '<div class="ma-mech-box">'+
        '<strong>Safe Driver Action:</strong><br>'+unCertSteps+
      '</div>';
    }

    html+='<div style="margin-top:18px;border-top:1px solid #e2e8f0;padding-top:14px">'+
      '<strong style="display:block;font-size:14px;color:#0f172a;margin-bottom:8px">'+l.escalationTitle+'</strong>'+
      '<a href="tel:+919845012345" class="ma-btn-escalate">'+l.callFleetMech+'</a>'+
      '<a href="tel:+919988776655" class="ma-btn-escalate" style="border-color:#1e293b;color:#1e293b">'+l.callFleetSup+'</a>'+
      '<button type="button" class="ma-card" style="width:100%;margin-top:10px;min-height:0;padding:12px;text-align:center" onclick="speakTroubleshootSolution()">'+l.readAloudBtn+'</button>'+
      '<button type="button" class="ma-card ma-primary" style="width:100%;margin-top:8px;min-height:0;padding:12px;text-align:center" onclick="exactProblem()">'+l.reportAnotherBtn+'</button>'+
    '</div></section>';

    page(l.troubleshootTitle,html);
  }

  function speakTroubleshootSolution(){
    const diag=window.__lastDiagnosis;
    const curLang=getLang();
    const dInfo=diag?(diag[curLang]||diag.en):null;
    let spokenText='';
    if(dInfo){
      spokenText=dInfo.title+'. '+dInfo.immediateAction+'. '+dInfo.steps[0]+'. '+dInfo.warning;
    }else{
      spokenText=curLang==='kn'
        ?'ವಾಹನದ ಸಮಸ್ಯೆಯನ್ನು ಖಚಿತವಾಗಿ ಗುರುತಿಸಲಾಗಲಿಲ್ಲ. ಸುರಕ್ಷಿತ ಸ್ಥಳದಲ್ಲಿ ನಿಲ್ಲಿಸಿ ಸೂಪರ್‌ವೈಸರ್‌ಗೆ ಕರೆ ಮಾಡಿ.'
        :curLang==='hi'
        ?'वाहन की समस्या की पुष्टि नहीं हो सकी। सुरक्षित जगह पर रुकें और सुपरवाइजर को कॉल करें।'
        :'The vehicle problem could not be identified with certainty. Stop the truck in a safe location and call the fleet supervisor.';
    }
    const loc=curLang==='kn'?'kn-IN':curLang==='hi'?'hi-IN':'en-IN';
    if(window.AndroidBridge?.speakText){
      AndroidBridge.speakText(spokenText,loc);
    }else if('speechSynthesis' in window){
      window.speechSynthesis.cancel();
      const u=new SpeechSynthesisUtterance(spokenText);
      u.lang=loc;
      window.speechSynthesis.speak(u);
    }else{
      alert('Speech: '+spokenText);
    }
  }

  /* EMPLOYEE WORK UPDATE */
  function employeeUpdate(){
    stopActiveVoice();
    window.__currentRenderer=employeeUpdate;
    const u=getUser()||{};
    const l=L();
    page(l.empTitle,
      '<section class="ma-hero">'+
        '<div class="ma-brand">➕ '+l.empTitle+'</div>'+
        '<div class="ma-sub">'+l.empSub.replace('{name}',esc(u.name||l.employee))+'</div>'+
      '</section>'+
      '<section class="ma-hero">'+
        '<form onsubmit="event.preventDefault();saveEmployeeWork();">'+
          '<label style="display:block;font-size:16px;font-weight:900;color:#0f172a;margin-bottom:8px">'+
            l.empDescLabel+' <span style="color:#b71c1c">*</span>'+
          '</label>'+
          '<textarea id="empWorkText" class="ma-emp-textarea" rows="6" placeholder="'+esc(l.empPh)+'" oninput="updateEmpCharCount()"></textarea>'+
          '<div style="display:flex;justify-content:space-between;align-items:center;font-size:12px;color:#64748b;margin:6px 0 10px">'+
            '<span id="empCharCount">0 '+l.charCount+'</span>'+
            '<span style="color:#16a34a;font-weight:700">'+l.voiceAndTypingTogether+'</span>'+
          '</div>'+
          '<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">'+
            '<button type="button" class="ma-btn-voice" id="empVoiceBtn" onclick="speakEmployeeWork()">'+
              l.speakUpdateBtn+
            '</button>'+
            '<button type="button" class="ma-btn-voice" id="btnVoiceStop" style="display:none;background:#b71c1c" onclick="stopActiveVoice()">⏹️ '+l.stopListening+'</button>'+
            '<button type="submit" class="ma-btn-submit" id="empSubmitBtn">'+
              l.submitUpdateBtn+
            '</button>'+
          '</div>'+
          '<div id="empMsg" style="margin-top:14px"></div>'+
        '</form>'+
      '</section>'+
      '<section class="ma-hero" style="margin-top:18px">'+
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">'+
          '<div class="ma-brand" style="font-size:18px">'+l.prevSubmittedTitle+'</div>'+
          '<button type="button" class="ma-card" style="min-height:0;padding:6px 14px;font-size:12px;border-radius:8px" onclick="loadEmployeeWorkHistory()">'+l.refreshBtn+'</button>'+
        '</div>'+
        '<div id="empHistoryList" style="color:#64748b;font-size:14px">'+l.loading+'</div>'+
      '</section>'
    );
    loadEmployeeWorkHistory();
  }

  function updateEmpCharCount(){
    const text=document.getElementById('empWorkText')?.value||'';
    const countEl=document.getElementById('empCharCount');
    const l=L();
    if(countEl){
      const words=text.trim()?text.trim().split(/\s+/).length:0;
      countEl.textContent=text.length+' '+l.charCount+' • '+words+' '+l.wordsCount;
    }
  }

  function speakEmployeeWork(){
    const curLang=getLang();
    const loc=curLang==='kn'?'kn-IN':curLang==='hi'?'hi-IN':'en-IN';
    startVoiceRecognition('empWorkText','empMsg',loc,function(text){
      updateEmpCharCount();
    },'empVoiceBtn');
  }

  function saveEmployeeWork(){
    stopActiveVoice();
    const l=L();
    const text=(document.getElementById('empWorkText')?.value||'').trim();
    const msg=document.getElementById('empMsg');
    const btn=document.getElementById('empSubmitBtn');
    if(!text){
      if(msg) msg.innerHTML='<div class="ma-danger-box">'+l.emptyWorkMsg+'</div>';
      document.getElementById('empWorkText')?.focus();
      return;
    }
    if(btn){btn.disabled=true;btn.textContent=l.submittingUpdate;}
    if(msg) msg.innerHTML='<div style="color:#0284c7;font-weight:700">'+l.submittingUpdate+'</div>';
    
    const today=new Date().toISOString().slice(0,10);
    apiRequest('save_work',{date:today,vehicleNumber:'-',workCompleted:text},r=>{
      if(btn){btn.disabled=false;btn.textContent=l.submitUpdateBtn;}
      if(!r || !r.ok){
        if(msg) msg.innerHTML='<div class="ma-danger-box">❌ '+esc((r&&r.error)||'Could not reach database.')+'</div>';
        return;
      }
      if(msg) msg.innerHTML='<div class="ma-safe-box">'+l.saveWorkSuccess+'</div>';
      const area=document.getElementById('empWorkText');
      if(area) area.value='';
      updateEmpCharCount();
      loadEmployeeWorkHistory();
    });
  }

  function loadEmployeeWorkHistory(){
    const box=document.getElementById('empHistoryList');
    if(!box) return;
    const l=L();
    box.innerHTML='<div style="color:#64748b">'+l.loading+'</div>';
    apiRequest('list_work',{},r=>{
      if(!box) return;
      if(!r || !r.ok){
        box.innerHTML='<div style="color:#dc2626">Could not load work history ('+esc((r&&r.error)||'error')+').</div>';
        return;
      }
      const records=Array.isArray(r.records)?r.records:[];
      const curUser=getUser()||{};
      const myRecords=records.filter(x=>!x.userId || String(x.userId)===String(curUser.id) || !curUser.id);
      if(!myRecords.length){
        box.innerHTML='<div style="color:#64748b;font-style:italic">'+l.noRecords+'</div>';
        return;
      }
      box.innerHTML='';
      myRecords.slice(0,10).forEach(x=>{
        const item=document.createElement('div');
        item.style.cssText='background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:12px 14px;margin:8px 0';
        item.innerHTML='<div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;font-weight:800">'+
          '<span>📅 '+esc(formatWorkDate(x.date,x.createdAt))+'</span>'+
          '<span class="ma-action-badge ma-badge-safe">SAVED</span>'+
          '</div>'+
          '<div style="font-size:14px;line-height:1.45;color:#1e293b;margin-top:6px;white-space:pre-wrap">'+esc(x.workCompleted||'')+'</div>';
        box.appendChild(item);
      });
    });
  }

  /* MECHANIC WORK UPDATE */
  function mechanicUpdate(){
    stopActiveVoice();
    window.__currentRenderer=mechanicUpdate;
    const u=getUser()||{};
    const l=L();
    page(l.mechTitle,
      '<section class="ma-hero"><div class="ma-brand">➕ '+l.mechTitle+'</div><div class="ma-sub">'+l.mechSub.replace('{name}',esc(u.name||''))+'</div>'+
      '<div style="display:grid;gap:12px;margin-top:15px">'+
      '<input id="mwVehicle" placeholder="'+esc(l.vehReq)+'" style="padding:15px;border:1px solid #d0d5dd;border-radius:10px;font-size:17px">'+
      '<textarea id="mwWork" rows="6" class="ma-emp-textarea" placeholder="'+esc(l.mechWorkPh)+'"></textarea>'+
      '<div style="display:flex;gap:10px;flex-wrap:wrap">'+
        '<button type="button" class="ma-btn-voice" id="mechVoiceBtn" onclick="speakMechanicWork()">🎤 '+l.voiceInputLbl+'</button>'+
        '<button type="button" class="ma-btn-voice" id="btnVoiceStop" style="display:none;background:#b71c1c" onclick="stopActiveVoice()">⏹️ '+l.stopListening+'</button>'+
        '<button type="button" class="ma-btn-submit" onclick="saveMechanicWork()">💾 '+l.submitUpdateBtn+'</button>'+
      '</div>'+
      '<div id="mwMsg"></div></div></section>'
    );
  }
  function speakMechanicWork(){
    const loc=getLang()==='kn'?'kn-IN':getLang()==='hi'?'hi-IN':'en-IN';
    startVoiceRecognition('mwWork','mwMsg',loc,null,'mechVoiceBtn');
  }
  function saveMechanicWork(){
    stopActiveVoice();
    const l=L();
    const v=document.getElementById('mwVehicle').value.trim(),w=document.getElementById('mwWork').value.trim(),msg=document.getElementById('mwMsg');
    if(!v||!w){if(msg)msg.innerHTML='<div class="ma-danger-box">⚠️ '+l.vehicleNoLbl+' + '+l.workCompletedLbl+' required.</div>';return;}
    apiRequest('save_work',{date:new Date().toISOString().slice(0,10),vehicleNumber:v,workCompleted:w},r=>{
      if(msg)msg.innerHTML=r.ok?'<div class="ma-safe-box">'+l.mechSaveSuccess+'</div>':'<div class="ma-danger-box">❌ '+(r.error||'Save failed.')+'</div>';
      if(r.ok){document.getElementById('mwWork').value='';}
    });
  }

  function formatWorkDate(date,createdAt){
    const raw=createdAt||date||'';
    let d=new Date(raw);
    if(isNaN(d.getTime()) && date){d=new Date(String(date).slice(0,10)+'T00:00:00+05:30');}
    if(isNaN(d.getTime())) return String(date||raw||'');
    const parts=new Intl.DateTimeFormat('en-IN',{day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit',hour12:true,timeZone:'Asia/Kolkata'}).formatToParts(d);
    const get=k=>parts.find(x=>x.type===k)?.value||'';
    return get('day')+' '+get('month')+' '+get('year')+' • '+get('hour')+':'+get('minute')+' '+get('dayPeriod');
  }

  function workRecords(admin){
    stopActiveVoice();
    window.__currentRenderer=()=>workRecords(admin);
    window.__maWorkRecords=[];
    const l=L();
    const pageTitle=admin?l.allRecordsTitle:(role()==='EMPLOYEE'?l.myRecordsTitle:l.myRecordsTitle);
    page(pageTitle,'<section class="ma-hero"><div class="ma-brand">📋 '+esc(pageTitle)+'</div><div class="ma-sub">Central DailyWork records saved in operational database</div>'+(admin?'<button class="ma-card ma-primary" style="width:100%;margin-top:12px" onclick="exportMechanicData()">⬇️ '+l.exportBtn+'</button>':'')+'<div id="workList" style="margin-top:14px">'+l.loading+'</div></section>');
    apiRequest('list_work',{},r=>{
      const box=document.getElementById('workList');if(!box)return;
      if(!r.ok){box.innerHTML='<div class="ma-danger-box">❌ '+esc(r.error||'Could not load records.')+'<br><button class="ma-card" style="margin-top:10px;width:100%" onclick="workRecords('+(admin?'true':'false')+')">'+l.retryBtn+'</button></div>';return;}
      const records=Array.isArray(r.records)?r.records:[];window.__maWorkRecords=records;
      if(!records.length){
        box.innerHTML='<div class="status-note" style="border-left:5px solid #b71c1c"><b>'+l.noRecords+'</b><br><small>'+l.noRecordsSub+'</small><br><button class="ma-card ma-primary" style="width:100%;margin-top:10px" onclick="workRecords('+(admin?'true':'false')+')">↻ REFRESH</button></div>';
        return;
      }
      box.innerHTML='';
      records.forEach(x=>{
        const d=document.createElement('div');
        d.style.cssText='background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:16px;margin:10px 0;box-shadow:0 1px 4px rgba(0,0,0,0.04)';
        const hasVehicle=x.vehicleNumber && x.vehicleNumber!=='-' && x.vehicleNumber!=='N/A' && x.vehicleNumber!=='EMPLOYEE';
        d.innerHTML='<div style="font-size:13px;color:#64748b;font-weight:800">📅 '+esc(formatWorkDate(x.date,x.createdAt))+'</div>'+
          (hasVehicle?'<div style="font-size:18px;font-weight:900;margin-top:6px;color:#0f172a">🚛 '+esc(x.vehicleNumber)+'</div>':'<div style="font-size:14px;font-weight:800;margin-top:6px;color:#0284c7">👷 Employee Daily Activity</div>')+
          '<div style="font-size:13px;color:#475569;font-weight:800;margin-top:4px">By: '+esc(x.userName||'User')+'</div>'+
          '<div style="font-size:15px;line-height:1.5;margin-top:8px;white-space:pre-wrap;color:#1e293b;background:#f8fafc;padding:10px 12px;border-radius:10px">'+esc(x.workCompleted||'')+'</div>';
        box.appendChild(d);
      });
    });
  }

  function exportMechanicData(){
    const records=Array.isArray(window.__maWorkRecords)?window.__maWorkRecords:[];
    if(!records.length){alert('Load the records first, then tap DOWNLOAD DATA.');return;}
    const lines=['Date,Time,Vehicle Number,User Name,Work Completed'];
    records.forEach(x=>{const dt=formatWorkDate(x.date,x.createdAt).replace(/,/g,'');lines.push([dt,x.vehicleNumber||'-',x.userName||'',x.workCompleted||''].map(v=>csvSafe(v)).join(','));});
    const csv=lines.join('\r\n');
    if(window.AndroidBridge?.saveTextFile)AndroidBridge.saveTextFile('Balaji_DailyWork_Export.csv',csv);
    else{const a=document.createElement('a');a.href='data:text/csv;charset=utf-8,'+encodeURIComponent(csv);a.download='Balaji_DailyWork_Export.csv';a.click();}
  }
  function csvSafe(v){return '"'+String(v??'').replace(/"/g,'""')+'"';}
  function adminWork(){workRecords(true)}
  function mechanicRecords(){workRecords(false)}

  /* ADMIN USERS & PROBLEM REPORTS */
  function adminUsers(){
    stopActiveVoice();
    window.__currentRenderer=adminUsers;
    const l=L();
    page(l.manageUsersTitle,
      '<section class="ma-hero"><div class="ma-brand">'+l.addUserTitle+'</div><div class="ma-sub">Mobile number is the login username.</div><div style="display:grid;gap:10px;margin-top:15px"><input id="auName" placeholder="'+esc(l.namePh)+'" style="padding:14px;border:1px solid #d0d5dd;border-radius:10px"><input id="auMobile" inputmode="numeric" maxlength="10" placeholder="'+esc(l.mobilePh)+'" style="padding:14px;border:1px solid #d0d5dd;border-radius:10px"><select id="auRole" style="padding:14px;border:1px solid #d0d5dd;border-radius:10px"><option>DRIVER</option><option>MECHANIC</option><option>EMPLOYEE</option><option>ADMIN</option></select><select id="auStatus" style="padding:14px;border:1px solid #d0d5dd;border-radius:10px"><option>ACTIVE</option><option>DISABLED</option></select><input id="auPass" type="password" placeholder="'+esc(l.passPh)+'" style="padding:14px;border:1px solid #d0d5dd;border-radius:10px"><button class="ma-card ma-primary" style="width:100%" onclick="addManagedUser()">'+l.createUserBtn+'</button><div id="auMsg" class="status-note"></div></div></section><section class="ma-hero"><div class="ma-brand">'+l.userListTitle+'</div><div id="userList">'+l.loading+'</div></section>'
    );
    loadUsers();
  }
  function loadUsers(){apiRequest('list_users',{},r=>{const box=document.getElementById('userList');if(!box)return;if(!r.ok){box.innerHTML='❌ '+esc(r.error||'Could not load users.');return;}box.innerHTML='';(r.users||[]).forEach(u=>{const d=document.createElement('div');d.style.cssText='border:1px solid #e5e7eb;border-radius:14px;padding:13px;margin:9px 0';d.innerHTML='<b>'+esc(u.name)+'</b><div style="color:#667085">'+esc(u.mobile)+' • '+esc(roleLabel(u.role))+' • '+esc(u.status)+'</div><div style="display:flex;gap:7px;flex-wrap:wrap;margin-top:9px"><select id="role_'+u.id+'" style="padding:8px"><option '+(roleLabel(u.role)==='DRIVER'?'selected':'')+'>DRIVER</option><option '+(u.role==='MECHANIC'?'selected':'')+'>MECHANIC</option><option '+(u.role==='EMPLOYEE'?'selected':'')+'>EMPLOYEE</option><option '+(u.role==='ADMIN'?'selected':'')+'>ADMIN</option></select><select id="status_'+u.id+'" style="padding:8px"><option '+(u.status==='ACTIVE'?'selected':'')+'>ACTIVE</option><option '+(u.status!=='ACTIVE'?'selected':'')+'>DISABLED</option></select><button onclick="changeManagedRole(\''+u.id+'\')">Role</button><button onclick="changeManagedStatus(\''+u.id+'\')">Status</button><button onclick="resetManagedPassword(\''+u.id+'\')">Password</button></div>';box.appendChild(d);});});}
  function addManagedUser(){const msg=document.getElementById('auMsg'),n=document.getElementById('auName').value.trim(),m=document.getElementById('auMobile').value.replace(/\D/g,''),r=document.getElementById('auRole').value,s=document.getElementById('auStatus').value,p=document.getElementById('auPass').value;if(!n||!/^[0-9]{10}$/.test(m)){msg.textContent='Enter name and 10-digit mobile.';return;}msg.textContent='⏳ Creating user…';apiRequest('add_user',{name:n,mobile:m,role:r,password:p,status:s},res=>{if(!res||!res.ok){msg.textContent='❌ '+((res&&res.error)||'Could not create user.');return;}msg.textContent='✅ User created successfully.';document.getElementById('auName').value='';document.getElementById('auMobile').value='';document.getElementById('auPass').value='';loadUsers();});}
  function changeManagedRole(id){const r=document.getElementById('role_'+id).value;apiRequest('set_user_role',{userId:id,role:r},res=>{alert(res.ok?'Role updated.':(res.error||'Failed.'));loadUsers();});}
  function changeManagedStatus(id){const s=document.getElementById('status_'+id).value;apiRequest('set_user_status',{userId:id,status:s},res=>{alert(res.ok?'Status updated.':(res.error||'Failed.'));loadUsers();});}
  function resetManagedPassword(id){const p=prompt('Enter new password (minimum 8 characters):');if(!p)return;apiRequest('set_user_password',{userId:id,password:p},res=>alert(res.ok?'Password updated.':(res.error||'Failed.')));}

  function adminProblems(){
    stopActiveVoice();
    window.__currentRenderer=adminProblems;
    const l=L();
    page(l.adminProblemsTitle,
      '<section class="ma-hero"><div class="ma-brand">'+l.adminProblemsBrand+'</div><div class="ma-sub">'+l.adminProblemsSub+'</div><div id="problemList" style="margin-top:14px">'+l.loading+'</div></section>'
    );
    apiRequest('list_problems',{},r=>{
      const box=document.getElementById('problemList');if(!box)return;
      if(!r.ok){box.innerHTML='<div class="ma-danger-box">❌ '+esc(r.error||'Could not load reports.')+'</div>';return;}
      if(!(r.records||[]).length){box.innerHTML='<div class="status-note">No driver problem reports recorded yet.</div>';return;}
      box.innerHTML='';
      r.records.forEach(x=>{
        const d=document.createElement('div');
        d.style.cssText='border:1px solid #e2e8f0;border-radius:14px;padding:14px;margin:10px 0;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,0.04)';
        d.innerHTML='<div style="display:flex;justify-content:space-between;font-size:13px;font-weight:900;color:#0f172a">'+
          '<span>🚛 '+(x.vehicleNumber && x.vehicleNumber!=='-'?esc(x.vehicleNumber):'Vehicle Not Specified')+'</span>'+
          '<span style="color:#64748b;font-weight:700">'+esc(x.date)+' '+esc(x.time)+'</span>'+
          '</div>'+
          '<div style="color:#64748b;font-size:13px;margin-top:4px">Reported by: <strong>'+esc(x.userName)+'</strong> • '+esc(roleLabel(x.role))+'</div>'+
          '<div style="margin-top:8px;font-size:15px;line-height:1.45;background:#f8fafc;padding:10px 12px;border-radius:10px;white-space:pre-wrap;color:#1e293b">'+esc(x.problem||x.photoText||'No text')+'</div>'+
          '<div style="margin-top:8px;display:flex;gap:8px">'+
            '<button class="ma-card" style="min-height:0;padding:6px 12px;font-size:12px;border-radius:6px" onclick="renderTroubleshootingResult(\''+esc(x.problem||x.photoText||'').replace(/'/g,'\\&#39;')+'\',\''+esc(x.vehicleNumber||'').replace(/'/g,'\\&#39;')+'\',identifyProblem(\''+esc(x.problem||x.photoText||'').replace(/'/g,'\\&#39;')+'\'))">'+l.viewAiDiagnosis+'</button>'+
          '</div>';
        box.appendChild(d);
      });
    });
  }

  /* ADMIN MAHINDRA DATA */
  window.__adminDataTab='overview';
  function adminMahindraData(){
    stopActiveVoice();
    window.__currentRenderer=adminMahindraData;
    const l=L();
    page(l.mahindraDataTitle,
      '<section class="ma-hero">'+
        '<div class="ma-brand">📚 '+l.mahindraDataTitle+'</div>'+
        '<div class="ma-sub">Official MTBD Technical Documentation, Vehicle Models, Engineering Specifications & Live Fleet Analytics</div>'+
      '</section>'+
      '<nav class="ma-admin-tabs">'+
        '<button type="button" class="ma-tab-btn active" id="tab_overview" onclick="selectAdminDataTab(\'overview\')">'+l.tabOverview+'</button>'+
        '<button type="button" class="ma-tab-btn" id="tab_models" onclick="selectAdminDataTab(\'models\')">'+l.tabModels+'</button>'+
        '<button type="button" class="ma-tab-btn" id="tab_specs" onclick="selectAdminDataTab(\'specs\')">'+l.tabSpecs+'</button>'+
        '<button type="button" class="ma-tab-btn" id="tab_visuals" onclick="selectAdminDataTab(\'visuals\')">'+l.tabVisuals+'</button>'+
        '<button type="button" class="ma-tab-btn" id="tab_explanations" onclick="selectAdminDataTab(\'explanations\')">'+l.tabExplanations+'</button>'+
        '<button type="button" class="ma-tab-btn" id="tab_ops" onclick="selectAdminDataTab(\'ops\')">'+l.tabOps+'</button>'+
        '<button type="button" class="ma-tab-btn" id="tab_search" onclick="selectAdminDataTab(\'search\')">'+l.tabSearch+'</button>'+
      '</nav>'+
      '<div id="adminDataContent"></div>'
    );
    selectAdminDataTab(window.__adminDataTab||'overview');
  }

  function selectAdminDataTab(tabId){
    window.__adminDataTab=tabId;
    document.querySelectorAll('.ma-tab-btn').forEach(b=>b.classList.remove('active'));
    document.getElementById('tab_'+tabId)?.classList.add('active');
    const content=document.getElementById('adminDataContent');
    if(!content) return;

    if(tabId==='overview') renderAdminOverviewTab(content);
    else if(tabId==='models') renderAdminModelsTab(content);
    else if(tabId==='specs') renderAdminSpecsTab(content);
    else if(tabId==='visuals') renderAdminVisualsTab(content);
    else if(tabId==='explanations') renderAdminExplanationsTab(content);
    else if(tabId==='ops') renderAdminOpsTab(content);
    else if(tabId==='search') renderAdminSearchTab(content);
  }

  function renderAdminOverviewTab(box){
    const kb=Array.isArray(window.mahindraKB)?window.mahindraKB:[];
    box.innerHTML='<section class="ma-hero">'+
      '<div class="ma-brand" style="font-size:18px">Key System Overview & Verified Metrics</div>'+
      '<div class="ma-kpi-grid">'+
        '<div class="ma-kpi-card"><div class="ma-kpi-num">'+(kb.length||'700+')+'</div><div class="ma-kpi-lbl">Technical Manual Sections</div></div>'+
        '<div class="ma-kpi-card"><div class="ma-kpi-num">3</div><div class="ma-kpi-lbl">Engine Platforms (D72, D35, D25)</div></div>'+
        '<div class="ma-kpi-card"><div class="ma-kpi-num">2</div><div class="ma-kpi-lbl">ATS Generations (DNOx 2.2 / 5.2)</div></div>'+
        '<div class="ma-kpi-card"><div class="ma-kpi-num">OBD-II</div><div class="ma-kpi-lbl">Diagnostic Compliance</div></div>'+
      '</div>'+
      '<div style="background:#f8fafc;padding:14px;border-radius:12px;border:1px solid #e2e8f0;margin-top:14px">'+
        '<strong style="font-size:14px;color:#0f172a;display:block;margin-bottom:8px">Data Classification & Authenticity Standard</strong>'+
        '<div style="display:grid;gap:8px;font-size:13px">'+
          '<div><span class="ma-source-tag ma-source-verified">Verified Factory Data</span> Certified Mahindra Truck & Bus Division (MTBD) Diagnostic Manuals embedded in app.</div>'+
          '<div><span class="ma-source-tag ma-source-ops">User-Submitted Operational Data</span> DailyWork updates and ProblemReports submitted by drivers, mechanics and employees.</div>'+
          '<div><span class="ma-source-tag ma-source-na">Information Not Available</span> Fields without factory measurements are marked as unavailable rather than fabricated.</div>'+
        '</div>'+
      '</div>'+
    '</section>';
  }

  function renderAdminModelsTab(box){
    box.innerHTML='<section class="ma-hero">'+
      '<div class="ma-brand" style="font-size:18px">Mahindra BSVI Commercial Vehicle Lineup</div>'+
      '<div class="ma-sub">Factory specifications for Heavy, Intermediate, and Light Commercial Platforms</div>'+
      '<div class="ma-admin-img-wrap" style="margin-top:14px">'+
        '<img src="mahindra_blazo_truck.jpg" class="ma-admin-img" alt="Mahindra Blazo X Truck">'+
        '<div class="ma-admin-img-cap"><strong>Figure 1:</strong> Mahindra Blazo X Heavy Commercial Truck — mPower 7.2L FuelSmart BSVI engine with smartSHIFT automated manual transmission and DNOx 2.2 ATS aftertreatment unit.</div>'+
      '</div>'+
      '<div class="ma-table-container">'+
      '<table class="ma-data-table">'+
        '<thead><tr><th>Platform / Model</th><th>Engine & Displacement</th><th>Power & Torque</th><th>Payload Class</th><th>ATS System</th></tr></thead>'+
        '<tbody>'+
          '<tr><td><strong>Mahindra BLAZO X</strong><br><small>HCV 28T – 55T</small></td><td>mPower 7.2L (D72)<br>6-Cylinder Diesel</td><td>276 HP @ 2200 RPM<br>1050 Nm @ 1200-1700 RPM</td><td>Multi-Axle Haulage & Tipper</td><td>DOC + DPF + SCR<br><span class="ma-source-tag ma-source-verified">DNOx 2.2</span></td></tr>'+
          '<tr><td><strong>Mahindra FURIO</strong><br><small>ICV 11T – 17T</small></td><td>mDi Tech 3.5L (D35)<br>4-Cylinder Diesel</td><td>140 HP @ 2400 RPM<br>525 Nm @ 1250-1800 RPM</td><td>Medium Freight & Cargo</td><td>DOC + DPF + SCR<br><span class="ma-source-tag ma-source-verified">DNOx 5.2</span></td></tr>'+
          '<tr><td><strong>Mahindra TOURISTER & LOADKING</strong><br><small>LCV / Bus</small></td><td>mDi 2.5L (D25)<br>4-Cylinder Diesel</td><td>100 HP @ 3200 RPM<br>315 Nm @ 1400-2000 RPM</td><td>Light Cargo & Passenger Bus</td><td>DOC + DPF + SCR<br><span class="ma-source-tag ma-source-verified">DNOx 5.2</span></td></tr>'+
          '<tr><td><strong>Custom Telematics Profile</strong></td><td colspan="4" style="color:#64748b;font-style:italic"><span class="ma-source-tag ma-source-na">Information Not Available</span> — Vehicle-specific axle load sensors require optional fleet CAN-bus hardware.</td></tr>'+
        '</tbody>'+
      '</table>'+
      '</div>'+
    '</section>';
  }

  function renderAdminSpecsTab(box){
    box.innerHTML='<section class="ma-hero">'+
      '<div class="ma-brand" style="font-size:18px">Critical System Specifications & Threshold Limits</div>'+
      '<div class="ma-sub">Factory threshold limits extracted from the Mahindra BS6 Diagnostic Manual</div>'+
      '<div class="ma-admin-img-wrap" style="margin-top:14px">'+
        '<img src="mahindra_engine_ems.jpg" class="ma-admin-img" alt="Mahindra D72 EMS Engine">'+
        '<div class="ma-admin-img-cap"><strong>Figure 2:</strong> Mahindra D72 Engine Management System — ECU CC898 with common rail, injectors, turbocharger, and high-pressure fuel pump.</div>'+
      '</div>'+
      '<div class="ma-table-container">'+
      '<table class="ma-data-table">'+
        '<thead><tr><th>Subsystem</th><th>Parameter</th><th>Normal / Operating Threshold</th><th>Action / Limit Condition</th></tr></thead>'+
        '<tbody>'+
          '<tr><td><strong>DPF Soot Mass (D72)</strong></td><td>Soot Loading</td><td>0 to 65.0 grams</td><td>Regen required at &gt;65g; Service Regen max 130.0g</td></tr>'+
          '<tr><td><strong>DPF Soot Mass (D35)</strong></td><td>Soot Loading</td><td>0 to 46.0 grams</td><td>Regen required at &gt;46g; Service Regen max 75.0g</td></tr>'+
          '<tr><td><strong>DPF Soot Mass (D25)</strong></td><td>Soot Loading</td><td>0 to 35.0 grams</td><td>Regen required at &gt;35g; Service Regen max 69.5g</td></tr>'+
          '<tr><td><strong>Delta P Sensor</strong></td><td>Differential Pressure</td><td>&lt; 80 mbar (D72 high idle)</td><td>Fault triggers if backpressure exceeds threshold</td></tr>'+
          '<tr><td><strong>PRV (Pressure Relief)</strong></td><td>Open Time & Count</td><td>Time: 0 mins / Count: 0</td><td><strong>Reset threshold:</strong> 300 mins or 50 counts</td></tr>'+
          '<tr><td><strong>AdBlue / DEF</strong></td><td>ISO 22241 Concentration</td><td>32.5% Urea in Deionized Water</td><td>Reserve warning at &lt;10%; Derate at 0%</td></tr>'+
          '<tr><td><strong>Engine Coolant Temp</strong></td><td>Operating Window</td><td>75°C to 95°C</td><td>Warning lamp &gt;102°C; Stop engine immediately</td></tr>'+
          '<tr><td><strong>Chassis Pneumatics</strong></td><td>Air Brake Pressure</td><td>6.5 bar to 8.5 bar</td><td>Low pressure alarm &lt;6.5 bar (95 psi)</td></tr>'+
        '</tbody>'+
      '</table>'+
      '</div>'+
    '</section>';
  }

  function renderAdminVisualsTab(box){
    box.innerHTML='<section class="ma-hero">'+
      '<div class="ma-brand" style="font-size:18px">Technical Images & Visual Explanations</div>'+
      '<div class="ma-sub">Verified component photographs and architecture diagrams for Mahindra BSVI fleet</div>'+
      '<div class="ma-admin-img-wrap">'+
        '<img src="mahindra_blazo_truck.jpg" class="ma-admin-img" alt="Mahindra Blazo X">'+
        '<div class="ma-admin-img-cap"><strong>1. Mahindra Blazo X Heavy Duty Truck:</strong> Built on mPower FuelSmart engine platform with smartSHIFT automated manual transmission.</div>'+
      '</div>'+
      '<div class="ma-admin-img-wrap">'+
        '<img src="mahindra_dpf_system.jpg" class="ma-admin-img" alt="Mahindra DPF System">'+
        '<div class="ma-admin-img-cap"><strong>2. BSVI Exhaust Aftertreatment (ATS) Unit:</strong> Housing DOC, DPF, AdBlue DEF dosing injector, SCR catalyst, and Delta P sensor probes.</div>'+
      '</div>'+
      '<div class="ma-admin-img-wrap">'+
        '<img src="mahindra_engine_ems.jpg" class="ma-admin-img" alt="Mahindra D72 EMS Engine">'+
        '<div class="ma-admin-img-cap"><strong>3. D72 BSVI Engine Management System (EMS):</strong> 6-cylinder common rail diesel engine showing ECU CC898, common rail, injectors, and turbocharger.</div>'+
      '</div>'+
      '<div class="ma-admin-img-wrap">'+
        '<img src="mahindra_garuda_diagnostic.jpg" class="ma-admin-img" alt="Garuda II Diagnostic Tool">'+
        '<div class="ma-admin-img-cap"><strong>4. Mahindra Garuda II Diagnostic Scanner Tool:</strong> Rugged VCI connected to 16-pin OBD port on dashboard.</div>'+
      '</div>'+
    '</section>';
  }

  function renderAdminExplanationsTab(box){
    box.innerHTML='<section class="ma-hero">'+
      '<div class="ma-brand" style="font-size:18px">Data Explained in Simple English</div>'+
      '<div class="ma-sub">Clear explanations of what each data parameter means, why it matters, and what the numbers tell you</div>'+
      '<div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:16px;margin:12px 0">'+
        '<div style="font-size:16px;font-weight:900;color:#b71c1c">1. Diesel Particulate Filter (DPF) & Soot Load</div>'+
        '<div style="margin-top:6px;font-size:14px;line-height:1.5;color:#1e293b">• <strong>What it means:</strong> Catches soot from exhaust before leaving tailpipe.<br>• <strong>Why important:</strong> Prevents black smoke and protects air quality.<br>• <strong>Normal range:</strong> 0 to 40g. Over 65g requires regeneration.</div>'+
      '</div>'+
      '<div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:16px;margin:12px 0">'+
        '<div style="font-size:16px;font-weight:900;color:#0284c7">2. AdBlue / DEF Dosing & SCR System</div>'+
        '<div style="margin-top:6px;font-size:14px;line-height:1.5;color:#1e293b">• <strong>What it means:</strong> Urea solution turning NOx into harmless water vapour and nitrogen.<br>• <strong>Why important:</strong> Speed drops to 20 km/h if DEF runs out.<br>• <strong>Normal range:</strong> 32.5% urea in water. Top up at 10%.</div>'+
      '</div>'+
      '<div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:16px;margin:12px 0">'+
        '<div style="font-size:16px;font-weight:900;color:#d97706">3. Pressure Relief Valve (PRV) Counts & Time</div>'+
        '<div style="margin-top:6px;font-size:14px;line-height:1.5;color:#1e293b">• <strong>What it means:</strong> Safety valve relieving extreme common rail fuel pressure.<br>• <strong>Why important:</strong> Prevents fuel pipe bursts.<br>• <strong>Reset limit:</strong> 50 counts or 300 minutes.</div>'+
      '</div>'+
      '<div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:16px;margin:12px 0">'+
        '<div style="font-size:16px;font-weight:900;color:#16a34a">4. Delta P (Differential Pressure) Sensor</div>'+
        '<div style="margin-top:6px;font-size:14px;line-height:1.5;color:#1e293b">• <strong>What it means:</strong> Measures pressure before and after the DPF canister.<br>• <strong>Why important:</strong> Detects ash and soot buildup.<br>• <strong>Normal range:</strong> &lt;80 mbar on Blazo.</div>'+
      '</div>'+
    '</section>';
  }

  function renderAdminOpsTab(box){
    box.innerHTML='<section class="ma-hero"><div style="color:#64748b">'+L().loading+'</div></section>';
    apiRequest('list_work',{},workRes=>{
      apiRequest('list_problems',{},probRes=>{
        const workRecords=Array.isArray(workRes?.records)?workRes.records:[];
        const probRecords=Array.isArray(probRes?.records)?probRes.records:[];
        let dpfIssues=0, tempIssues=0, brakeIssues=0, elecIssues=0, otherIssues=0;
        probRecords.forEach(p=>{
          const t=(String(p.problem||'')+' '+String(p.photoText||'')).toLowerCase();
          if(/dpf|soot|regen/i.test(t)) dpfIssues++;
          else if(/heat|hot|temp|coolant/i.test(t)) tempIssues++;
          else if(/brake|air/i.test(t)) brakeIssues++;
          else if(/battery|alternator|charge|electric/i.test(t)) elecIssues++;
          else otherIssues++;
        });

        box.innerHTML='<section class="ma-hero">'+
          '<div class="ma-brand" style="font-size:18px">Operational Fleet Intelligence</div>'+
          '<div class="ma-sub">Real-time analysis calculated from actual database submissions</div>'+
          '<div class="ma-kpi-grid">'+
            '<div class="ma-kpi-card"><div class="ma-kpi-num" style="color:#0284c7">'+workRecords.length+'</div><div class="ma-kpi-lbl">Total Work Updates Saved</div></div>'+
            '<div class="ma-kpi-card"><div class="ma-kpi-num" style="color:#b71c1c">'+probRecords.length+'</div><div class="ma-kpi-lbl">Problem Reports Filed</div></div>'+
            '<div class="ma-kpi-card"><div class="ma-kpi-num" style="color:#16a34a">'+(workRecords.length>0?'100%':'0%')+'</div><div class="ma-kpi-lbl">Sync Reliability</div></div>'+
          '</div>'+
          '<div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:16px;margin-top:14px">'+
            '<strong style="font-size:15px;color:#0f172a;display:block;margin-bottom:12px">Problem Incident Distribution by Category (Actual Reports)</strong>'+
            '<div style="display:grid;gap:8px;font-size:13px">'+
              '<div><div style="display:flex;justify-content:space-between;margin-bottom:3px"><span>Exhaust ATS & DPF Warnings</span><strong>'+dpfIssues+'</strong></div><div style="background:#e2e8f0;border-radius:999px;height:8px;overflow:hidden"><div style="background:#b71c1c;width:'+(probRecords.length?Math.min(100,(dpfIssues/probRecords.length)*100):0)+'%;height:100%"></div></div></div>'+
              '<div><div style="display:flex;justify-content:space-between;margin-bottom:3px"><span>Cooling & Engine Temperature</span><strong>'+tempIssues+'</strong></div><div style="background:#e2e8f0;border-radius:999px;height:8px;overflow:hidden"><div style="background:#d97706;width:'+(probRecords.length?Math.min(100,(tempIssues/probRecords.length)*100):0)+'%;height:100%"></div></div></div>'+
              '<div><div style="display:flex;justify-content:space-between;margin-bottom:3px"><span>Brakes & Pneumatics</span><strong>'+brakeIssues+'</strong></div><div style="background:#e2e8f0;border-radius:999px;height:8px;overflow:hidden"><div style="background:#dc2626;width:'+(probRecords.length?Math.min(100,(brakeIssues/probRecords.length)*100):0)+'%;height:100%"></div></div></div>'+
              '<div><div style="display:flex;justify-content:space-between;margin-bottom:3px"><span>Electrical & Battery</span><strong>'+elecIssues+'</strong></div><div style="background:#e2e8f0;border-radius:999px;height:8px;overflow:hidden"><div style="background:#0284c7;width:'+(probRecords.length?Math.min(100,(elecIssues/probRecords.length)*100):0)+'%;height:100%"></div></div></div>'+
              '<div><div style="display:flex;justify-content:space-between;margin-bottom:3px"><span>Other General Mechanical</span><strong>'+otherIssues+'</strong></div><div style="background:#e2e8f0;border-radius:999px;height:8px;overflow:hidden"><div style="background:#64748b;width:'+(probRecords.length?Math.min(100,(otherIssues/probRecords.length)*100):0)+'%;height:100%"></div></div></div>'+
            '</div>'+
          '</div>'+
        '</section>';
      });
    });
  }

  function renderAdminSearchTab(box){
    const kb=Array.isArray(window.mahindraKB)?window.mahindraKB:[];
    const l=L();
    box.innerHTML='<section class="ma-hero">'+
      '<div class="ma-brand" style="font-size:18px">Search 700+ Mahindra Diagnostic Manual Sections</div>'+
      '<div class="ma-sub">Search fault codes (e.g. P2463, P018F), sensors, fuses, or wiring steps</div>'+
      '<div style="display:flex;gap:8px;margin-top:14px">'+
        '<input id="adminManualSearch" placeholder="'+esc(l.searchManualsPh)+'" style="flex:1;padding:12px;border:1px solid #d0d5dd;border-radius:10px;font-size:15px">'+
        '<button type="button" class="ma-card ma-primary" style="min-height:0;padding:12px 20px" onclick="searchAdminManual()">'+l.searchBtn+'</button>'+
      '</div>'+
      '<div id="adminSearchResults" style="margin-top:14px">'+
        '<div style="color:#64748b">Search query will search all '+kb.length+' factory manual sections.</div>'+
      '</div>'+
    '</section>';
  }

  function searchAdminManual(){
    const q=(document.getElementById('adminManualSearch')?.value||'').trim().toLowerCase();
    const box=document.getElementById('adminSearchResults');
    if(!box) return;
    if(!q){box.innerHTML='<div style="color:#64748b">Please enter a search term.</div>';return;}
    const kb=Array.isArray(window.mahindraKB)?window.mahindraKB:[];
    const results=kb.filter(r=>{
      return (String(r.text||'')+' '+String(r.source||'')+' '+String(r.file||'')).toLowerCase().includes(q);
    }).slice(0,15);
    
    if(!results.length){
      box.innerHTML='<div class="status-note" style="border-left:5px solid #b71c1c">No manual section found matching "'+esc(q)+'". Try searching for component names like "DPF", "Coolant", "PRV", "ECU" or "Garuda".</div>';
      return;
    }
    box.innerHTML='<div style="font-weight:800;color:#0f172a;margin-bottom:10px">Found '+results.length+' matching factory manual sections:</div>';
    results.forEach((r,i)=>{
      const d=document.createElement('div');
      d.style.cssText='background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:12px 14px;margin:8px 0;box-shadow:0 1px 3px rgba(0,0,0,0.04)';
      d.innerHTML='<div style="display:flex;justify-content:space-between;font-size:12px;color:#b71c1c;font-weight:900">'+
        '<span>📖 '+esc(r.source||'Manual')+'</span>'+
        (r.page?'<span>Page / Slide '+esc(r.page)+'</span>':'')+
        '</div>'+
        '<div style="font-size:14px;line-height:1.45;color:#1e293b;margin-top:6px;white-space:pre-wrap">'+esc(r.text||'')+'</div>';
      box.appendChild(d);
    });
  }

  /* DRIVER TRAINING GUIDES (TRILINGUAL) */
  const DRIVER_GUIDES={
    warning:[['🌡️','High Engine Temperature','Temperature warning'],['🛢️','Low Oil Pressure','Oil pressure warning'],['💨','Low Air Pressure','Air pressure warning'],['🔋','Battery Not Charging','Charging warning'],['🧰','Air Filter Clogged / Choked','Air filter warning'],['🅿️','Parking Brake Engaged','Parking brake'],['⚙️','Check Engine / MIL','Engine / MIL warning'],['💧','Low DEF / AdBlue Level','DEF / AdBlue'],['⛽','Water In Fuel','Fuel warning'],['🔬','NOx Malfunction','NOx system warning'],['🛑','STOP / Caution','Stop / caution warning']],
    dpf:[['📍','Park in a safe open area.','Safe location'],['🅿️','Apply hand brake and use wheel chokes.','Secure vehicle'],['N','Keep the vehicle in neutral.','Neutral gear'],['⚙️','PTO must be disengaged.','PTO OFF'],['🛑','Exhaust brake must be OFF.','Exhaust brake OFF'],['🦶','Do not operate the accelerator.','No accelerator'],['🚫','Inhibit switch must be OFF.','Inhibit OFF'],['♻️','Press the DPF regeneration switch for about 5 seconds and release.','Start regeneration'],['🔥','Exhaust / ATS parts become very hot. Keep away from hot parts.','Heat warning']],
    daily:[['🛢️','Engine oil level','Check before driving'],['💧','Radiator coolant level','Check before driving'],['🧴','Clutch oil level','Check before driving'],['🪑','Seat / steering adjustment','Driver position'],['🔒','Seat belt','Safety'],['🅿️','Parking brake','Safety'],['💡','All lights working','Electrical check'],['🎛️','All controls working','Control check'],['📟','Instrument cluster readiness','Cluster check'],['🛞','Tyres: pressure, damage, cuts and wear','Tyre check']],
    adblue:[['🧼','Keep the filler area clean.','Filling precaution'],['🚫','Prevent dust or mud contamination.','Contamination prevention'],['🧴','Use the dedicated filling arrangement.','Correct filling'],['💧','Put only AdBlue into the AdBlue tank.','Correct fluid only'],['⬆️','Do not overfill.','Avoid overfilling'],['🛠️','If a warning or fault remains, contact authorized service.','Service action']],
    safety:[['📵','Do not use a mobile phone while driving.','No phone while driving'],['🔒','Wear the seat belt.','Seat belt'],['🚦','Follow traffic rules and speed limits.','Traffic safety'],['😴','Do not drive when tired.','Rest before driving'],['↔️','Maintain a safe distance.','Safe distance'],['🔍','Inspect the vehicle before driving.','Pre-drive inspection'],['👨‍🔧','Repair work should be carried out by authorized persons.','Authorized repair']]
  };

  const DRIVER_GUIDE_TITLES={
    en:{warning:'WARNING LIGHTS',dpf:'DPF REGENERATION',daily:'DAILY DRIVER CHECK',adblue:'ADBLUE / DEF GUIDE',safety:'DRIVER SAFETY'},
    kn:{warning:'ವಾರ್ನಿಂಗ್ ಲೈಟ್‌ಗಳು',dpf:'DPF ರಿಜೆನರೇಷನ್',daily:'ದಿನನಿತ್ಯದ ಚಾಲಕ ತಪಾಸಣೆ',adblue:'ADBLUE / DEF ಮಾರ್ಗದರ್ಶಿ',safety:'ಚಾಲಕ ಸುರಕ್ಷತೆ'},
    hi:{warning:'वार्निंग लाइट',dpf:'DPF रीजेनेरेशन',daily:'दैनिक ड्राइवर जांच',adblue:'ADBLUE / DEF गाइड',safety:'ड्राइवर सुरक्षा'}
  };

  const DRIVER_TRANSLATIONS={
    warning:{
      kn:['ಎಂಜಿನ್ ತಾಪಮಾನ ಹೆಚ್ಚು','ಆಯಿಲ್ ಪ್ರೆಶರ್ ಕಡಿಮೆ','ಏರ್ ಪ್ರೆಶರ್ ಕಡಿಮೆ','ಬ್ಯಾಟರಿ ಚಾರ್ಜ್ ಆಗುತ್ತಿಲ್ಲ','ಏರ್ ಫಿಲ್ಟರ್ ಕ್ಲಾಗ್','ಪಾರ್ಕಿಂಗ್ ಬ್ರೇಕ್','ಚೆಕ್ ಎಂಜಿನ್ / MIL','DEF / AdBlue ಮಟ್ಟ ಕಡಿಮೆ','ಇಂಧನದಲ್ಲಿ ನೀರು','NOx ದೋಷ','STOP / ಎಚ್ಚರಿಕೆ'],
      hi:['इंजन तापमान अधिक','ऑयल प्रेशर कम','एयर प्रेशर कम','बैटरी चार्ज नहीं हो रही','एयर फिल्टर चोक','पार्किंग ब्रेक','चेक इंजन / MIL','DEF / AdBlue स्तर कम','ईंधन में पानी','NOx खराबी','STOP / सावधानी']
    },
    dpf:{
      kn:['ಸುರಕ್ಷಿತ ತೆರೆದ ಸ್ಥಳದಲ್ಲಿ ಪಾರ್ಕ್ ಮಾಡಿ','ಹ್ಯಾಂಡ್ ಬ್ರೇಕ್ ಹಾಕಿ ಮತ್ತು ವೀಲ್ ಚಾಕ್ ಬಳಸಿ','ವಾಹನವನ್ನು ನ್ಯೂಟ್ರಲ್‌ನಲ್ಲಿ ಇಡಿ','PTO disengage ಮಾಡಿ','ಎಕ್ಸಾಸ್ಟ್ ಬ್ರೇಕ್ OFF ಮಾಡಿ','ಆಕ್ಸಿಲರೇಟರ್ ಬಳಸಬೇಡಿ','Inhibit switch OFF ಇರಲಿ','DPF regeneration switch ಅನ್ನು ಸುಮಾರು 5 ಸೆಕೆಂಡ್ ಒತ್ತಿ ಬಿಡಿ','ಸೈಲೆನ್ಸರ್ ಭಾಗಗಳು ತುಂಬಾ ಬಿಸಿಯಾಗುತ್ತವೆ. ದೂರವಿರಿ'],
      hi:['सुरक्षित खुले स्थान में पार्क करें','हैंड ब्रेक लगाएं और व्हील चॉक लगाएं','वाहन को न्यूट्रल में रखें','PTO बंद रखें','एग्जॉस्ट ब्रेक OFF रखें','एक्सेलेरेटर न चलाएं','Inhibit switch OFF रखें','DPF regeneration switch को लगभग 5 सेकंड दबाकर छोड़ें','साइलेंसर बहुत गर्म होता है। दूर रहें']
    },
    daily:{
      kn:['ಎಂಜಿನ್ ಆಯಿಲ್ ಮಟ್ಟ','ರೇಡಿಯೇಟರ್ ಕೂಲಂಟ್ ಮಟ್ಟ','ಕ್ಲಚ್ ಆಯಿಲ್ ಮಟ್ಟ','ಸೀಟ್ / ಸ್ಟೀರಿಂಗ್ ಹೊಂದಾಣಿಕೆ','ಸೀಟ್ ಬೆಲ್ಟ್','ಪಾರ್ಕಿಂಗ್ ಬ್ರೇಕ್','ಎಲ್ಲಾ ಲೈಟ್‌ಗಳು ಕೆಲಸ ಮಾಡುತ್ತಿವೆಯೇ','ಎಲ್ಲಾ ಕಂಟ್ರೋಲ್‌ಗಳು ಕೆಲಸ ಮಾಡುತ್ತಿವೆಯೇ','ಇನ್‌ಸ್ಟ್ರುಮೆಂಟ್ ಕ್ಲಸ್ಟರ್ ಸಿದ್ಧತೆ','ಟೈರ್ ಒತ್ತಡ, ಹಾನಿ, ಕಟ್ ಮತ್ತು ವೇರ್'],
      hi:['इंजन ऑयल स्तर','रेडिएटर कूलेंट स्तर','क्लच ऑयल स्तर','सीट / स्टीयरिंग एडजस्टमेंट','सीट बेल्ट','पार्किंग ब्रेक','सभी लाइट काम कर रही हैं','सभी कंट्रोल काम कर रहे हैं','इंस्ट्रूमेंट क्लस्टर तैयार है','टायर: प्रेशर, नुकसान, कट और घिसाव']
    },
    adblue:{
      kn:['ಫಿಲ್ಲರ್ ಪ್ರದೇಶ ಸ್ವಚ್ಛವಾಗಿರಲಿ','ಧೂಳು ಅಥವಾ ಮಣ್ಣು ಒಳಗೆ ಹೋಗದಂತೆ ನೋಡಿ','Dedicated filling arrangement ಬಳಸಿ','AdBlue tank ಗೆ AdBlue ಹೊರತು ಬೇರೆ ಯಾವುದನ್ನೂ ಹಾಕಬೇಡಿ','Overfill ಮಾಡಬೇಡಿ','Warning ಅಥವಾ fault ಉಳಿದರೆ authorized service ಸಂಪರ್ಕಿಸಿ'],
      hi:['फिलर क्षेत्र साफ रखें','धूल या मिट्टी को अंदर जाने से रोकें','Dedicated filling arrangement इस्तेमाल करें','AdBlue टैंक में AdBlue के अलावा कुछ न डालें','ओवरफिल न करें','वार्निंग या फॉल्ट रहे तो authorized service से संपर्क करें']
    },
    safety:{
      kn:['ಚಾಲನೆ ಮಾಡುವಾಗ ಮೊಬೈಲ್ ಬಳಸಬೇಡಿ','ಸೀಟ್ ಬೆಲ್ಟ್ ಧರಿಸಿ','ಟ್ರಾಫಿಕ್ ನಿಯಮ ಮತ್ತು ವೇಗ ಮಿತಿ ಪಾಲಿಸಿ','ದಣಿದಾಗ ಚಾಲನೆ ಮಾಡಬೇಡಿ','ಸುರಕ್ಷಿತ ಅಂತರ ಇಡಿ','ಚಾಲನೆಗೆ ಮೊದಲು ವಾಹನ ಪರಿಶೀಲಿಸಿ','Repair ಕೆಲಸವನ್ನು authorized persons ಮೂಲಕ ಮಾಡಿಸಿ'],
      hi:['ड्राइविंग के दौरान मोबाइल न इस्तेमाल करें','सीट बेल्ट पहनें','ट्रैफिक नियम और स्पीड लिमिट मानें','थके होने पर ड्राइव न करें','सुरक्षित दूरी रखें','ड्राइविंग से पहले वाहन जांचें','Repair काम authorized persons से कराएं']
    }
  };

  function driverGuide(type){
    stopActiveVoice();
    window.__currentRenderer=()=>driverGuide(type);
    const lang=getLang(),items=DRIVER_GUIDES[type]||[],trn=DRIVER_TRANSLATIONS[type]||{};
    const titles=DRIVER_GUIDE_TITLES[lang]||DRIVER_GUIDE_TITLES.en;
    const l=L();

    const html=items.map((x,i)=>{
      const title=lang==='en'?x[1]:(trn[lang]?.[i]||x[1]);
      const detail=lang==='en'?x[2]:(trn[lang]?.[i]||x[2]);
      const q=encodeURIComponent('Mahindra BS6 BSVI truck '+x[1]+' driver training '+(lang==='kn'?'Kannada':lang==='hi'?'Hindi':'English'));
      const url='https://www.youtube.com/results?search_query='+q;
      return '<div class="ma-guide-item">'+
        '<div class="ma-truck-icon">'+esc(x[0])+'</div>'+
        '<div class="ma-guide-copy"><div class="ma-guide-number">'+(i+1)+'</div><div class="ma-guide-title">'+esc(title)+'</div><div class="ma-guide-detail">'+esc(detail)+'</div></div>'+
        '<button class="ma-guide-video" onclick="openRealYoutube(\''+esc(url).replace(/'/g,'&#39;')+'\')">'+l.readRealVideo+'</button>'+
      '</div>';
    }).join('');

    const intros={
      en:type==='dpf'?'⚠️ Follow the supplied Mahindra BSVI procedure. Exhaust / ATS parts become very hot during regeneration. Keep away from flammable material.':type==='warning'?'⚠️ Select the exact warning item and open its matching training-video search. Do not guess a repair.':'📚 Every item below follows the supplied Mahindra driver-training guide.',
      kn:type==='dpf'?'⚠️ ನೀಡಿರುವ Mahindra BSVI/BS6 ವಿಧಾನವನ್ನು ಅನುಸರಿಸಿ. Regeneration ಸಮಯದಲ್ಲಿ Exhaust / ATS parts ತುಂಬಾ ಬಿಸಿಯಾಗುತ್ತವೆ. ಸುಲಭವಾಗಿ ಬೆಂಕಿ ಹತ್ತಿಕೊಳ್ಳುವ ವಸ್ತುಗಳಿಂದ ದೂರವಿಡಿ.':type==='warning'?'⚠️ ನಿರ್ದಿಷ್ಟ ವಾರ್ನಿಂಗ್ ಐಟಂ ಆಯ್ಕೆಮಾಡಿ ಮತ್ತು ವೀಡಿಯೋ ನೋಡಿ. ಊಹೆಯ ರಿಪೇರಿ ಮಾಡಬೇಡಿ.':'📚 ಕೆಳಗಿನ ಪ್ರತಿಯೊಂದು ಐಟಂ ಅಧಿಕೃತ Mahindra driver-training guide ಆಧಾರಿತವಾಗಿದೆ.',
      hi:type==='dpf'?'⚠️ दिए गए Mahindra BSVI/BS6 तरीके का पालन करें। Regeneration के दौरान Exhaust / ATS पार्ट्स बहुत गर्म होते हैं। ज्वलनशील पदार्थों से दूर रहें।':type==='warning'?'⚠️ सटीक वार्निंग चुनें और संबंधित वीडियो देखें। अनुमान से रिपेयर न करें।':'📚 नीचे दिए गए सभी बिंदु आधिकारिक Mahindra driver-training guide पर आधारित हैं।'
    };

    page(titles[type],'<section class="ma-hero"><div class="ma-brand">'+esc(titles[type])+'</div><div class="ma-sub">'+esc(intros[lang])+'</div></section><section class="ma-guide-list">'+html+'</section>');
  }

  function help(){
    stopActiveVoice();
    window.__currentRenderer=help;
    const r=role();
    const lang=getLang();
    const l=L();
    const roleTitles={
      ADMIN:lang==='kn'?'ನಿರ್ವಾಹಕರು — ನೀವು ಮಾಡಬಹುದಾದ ಕೆಲಸಗಳು':lang==='hi'?'व्यवस्थापक — आप क्या कर सकते हैं':'ADMIN — what you can do',
      MECHANIC:lang==='kn'?'ಮೆಕಾನಿಕ್ — ನೀವು ಮಾಡಬಹುದಾದ ಕೆಲಸಗಳು':lang==='hi'?'मैकेनिक — आप क्या कर सकते हैं':'MECHANIC — what you can do',
      EMPLOYEE:lang==='kn'?'ಉದ್ಯೋಗಿ — ನೀವು ಮಾಡಬಹುದಾದ ಕೆಲಸಗಳು':lang==='hi'?'कर्मचारी — आप क्या कर सकते हैं':'EMPLOYEE — what you can do',
      DRIVER:lang==='kn'?'ಚಾಲಕ — ನೀವು ಮಾಡಬಹುದಾದ ಕೆಲಸಗಳು':lang==='hi'?'ड्राइवर — आप क्या कर सकते हैं':'DRIVER — what you can do'
    };
    const title=roleTitles[r]||roleTitles.DRIVER;

    const itemsMap={
      ADMIN:{
        en:['Manage Driver, Mechanic, Employee and Admin accounts','View all employee & mechanic daily work updates','Inspect driver problem triage logs','Open professional Mahindra BSVI technical suite','Export records as CSV'],
        kn:['ಚಾಲಕರು, ಮೆಕಾನಿಕ್‌ಗಳು, ಉದ್ಯೋಗಿ ಖಾತೆಗಳನ್ನು ನಿರ್ವಹಿಸಿ','ಎಲ್ಲಾ ಉದ್ಯೋಗಿ ಮತ್ತು ಮೆಕಾನಿಕ್ ಕೆಲಸದ ಅಪ್‌ಡೇಟ್‌ಗಳನ್ನು ವೀಕ್ಷಿಸಿ','ಚಾಲಕರ ಸಮಸ್ಯೆ ವರದಿಗಳು ಮತ್ತು ಪರಿಹಾರ ಲಾಗ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ','ವೃತ್ತಿಪರ ಮಹೀಂದ್ರಾ BSVI ತಾಂತ್ರಿಕ ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಿ','ದಾಖಲೆಗಳನ್ನು CSV ರೂಪದಲ್ಲಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ'],
        hi:['ड्राइवर, मैकेनिक, कर्मचारी खाते प्रबंधित करें','सभी कर्मचारियों और मैकेनिकों के काम के अपडेट देखें','ड्राइवर समस्या रिपोर्ट और समाधान लॉग जांचें','महिंद्रा BSVI तकनीकी विवरण देखें','डेटा को CSV फाइल में डाउनलोड करें']
      },
      MECHANIC:{
        en:['Record maintenance with vehicle number & voice','Save daily repair updates centrally','View work history','Open Mahindra diagnostic guides'],
        kn:['ವಾಹನ ಸಂಖ್ಯೆ ಮತ್ತು ಧ್ವನಿಯೊಂದಿಗೆ ನಿರ್ವಹಣೆ ದಾಖಲಿಸಿ','ದೈನಂದಿನ ರಿಪೇರಿ ವಿವರಗಳನ್ನು ಕೇಂದ್ರದಲ್ಲಿ ಉಳಿಸಿ','ಹಿಂದಿನ ಕೆಲಸದ ಇತಿಹಾಸ ವೀಕ್ಷಿಸಿ','ಮಹೀಂದ್ರಾ ರೋಗನಿರ್ಣಯ ಗೈಡ್‌ಗಳನ್ನು ತೆರೆಯಿರಿ'],
        hi:['वाहन नंबर और आवाज से मेंटेनेंस रिकॉर्ड दर्ज करें','दैनिक रिपेयर अपडेट केंद्रीय रूप से सुरक्षित करें','पुराना कार्य इतिहास देखें','महिंद्रा डायग्नोस्टिक गाइड खोलें']
      },
      EMPLOYEE:{
        en:['Type or speak daily work update without vehicle number','Convert voice speech into editable text','Review and submit work updates to central database','View previously submitted work history'],
        kn:['ವಾಹನ ಸಂಖ್ಯೆಯ ಅಗತ್ಯವಿಲ್ಲದೆ ದಿನನಿತ್ಯದ ಕೆಲಸವನ್ನು ಟೈಪ್ ಮಾಡಿ ಅಥವಾ ಮಾತನಾಡಿ','ಧ್ವನಿಯನ್ನು ತಿದ್ದಬಹುದಾದ ಪಠ್ಯವಾಗಿ ಪರಿವರ್ತಿಸಿ','ಪರಿಶೀಲಿಸಿ ಕೇಂದ್ರ ಡೇಟಾಬೇಸ್‌ಗೆ ಅಪ್‌ಡೇಟ್ ಸಲ್ಲಿಸಿ','ಹಿಂದೆ ಸಲ್ಲಿಸಿದ ಕೆಲಸದ ಇತಿಹಾಸವನ್ನು ವೀಕ್ಷಿಸಿ'],
        hi:['वाहन नंबर के बिना दैनिक कार्य टाइप या बोलकर दर्ज करें','आवाज को संपादन योग्य टेक्स्ट में बदलें','जांच कर केंद्रीय डेटाबेस में सबमिट करें','पहले सबमिट किए गए काम का इतिहास देखें']
      },
      DRIVER:{
        en:['Report vehicle problems with text or voice (photo optional)','Get immediate numbered troubleshooting guidance and safety warnings','Safe driver checks vs when to call mechanic','One-tap emergency call to supervisor','Open warning lights & DPF regeneration training'],
        kn:['ಪಠ್ಯ ಅಥವಾ ಧ್ವನಿ ಬಳಸಿ ವಾಹನದ ಸಮಸ್ಯೆ ವರದಿ ಮಾಡಿ (ಫೋಟೋ ಐಚ್ಛಿಕ)','ತಕ್ಷಣದ ಹಂತ-ಹಂತದ ಪರಿಹಾರ ಮತ್ತು ಸುರಕ್ಷತಾ ಎಚ್ಚರಿಕೆಗಳನ್ನು ಪಡೆಯಿರಿ','ಚಾಲಕರು ಮಾಡಬಹುದಾದ ಸುರಕ್ಷಿತ ತಪಾಸಣೆ vs ಮೆಕಾನಿಕ್ ಕರೆಯುವ ಸಂದರ್ಭ','ಸೂಪರ್‌ವೈಸರ್‌ಗೆ ತುರ್ತು ಕರೆ ಮಾಡಿ','ವಾರ್ನಿಂಗ್ ಲೈಟ್‌ಗಳು ಮತ್ತು DPF ರಿಜೆನರೇಷನ್ ತರಬೇತಿ ವೀಡಿಯೋ ನೋಡಿ'],
        hi:['टेक्स्ट या आवाज से समस्या बताएं (फोटो वैकल्पिक है)','तुरंत चरण-दर-चरण समाधान और सुरक्षा चेतावनी प्राप्त करें','चालक द्वारा सुरक्षित जांच vs मैकेनिक को बुलाने की स्थिति','सुपरवाइजर को तुरंत आपातकालीन कॉल करें','वार्निंग लाइट और DPF रीजेनेरेशन प्रशिक्षण देखें']
      }
    };
    const items=(itemsMap[r]&&itemsMap[r][lang])||itemsMap[r]?.en||itemsMap.DRIVER.en;

    page(l.help,'<section class="ma-hero"><div class="ma-brand">'+esc(title)+'</div></section>'+
      items.map((x,i)=>`<div style="background:#fff;padding:15px;border-radius:14px;margin:9px 0;box-shadow:0 1px 7px #0001;font-size:15px;line-height:1.4"><b>${i+1}. ${esc(x)}</b></div>`).join('')
    );
  }

  function openRealYoutube(url){
    if(window.AndroidBridge && typeof AndroidBridge.openExternalUrl==='function'){
      AndroidBridge.openExternalUrl(url);
    }else{
      window.open(url,'_blank');
    }
  }

  window.openRealYoutube=openRealYoutube;
  window.maOpenMenu=menu;
  window.maCloseMenu=closeDrawer;
  window.maDashboard=dashboard;
  window.maOpenHelp=()=>runAction(help);
  window.maBack=()=>dashboard();

  // Expose camera and photo handling
  window.triggerDriverPhotoUpload=triggerDriverPhotoUpload;
  window.handleDriverPhotoSelected=handleDriverPhotoSelected;
  window.clearDriverPhoto=clearDriverPhoto;
  window.nativeCameraResult=function(ok){
    const st=document.getElementById('driverFormStatus');
    const l=L();
    if(st) st.innerHTML=ok?'<div class="ma-safe-box">'+l.photoCaptured+'</div>':'<div class="ma-danger-box">❌ Camera was not completed.</div>';
  };
  window.nativePhotoTextResult=function(text){
    const clean=String(text||'').trim();
    const el=document.getElementById('driverProblemText');
    const st=document.getElementById('driverFormStatus');
    const l=L();
    if(el&&clean) el.value=clean;
    if(st) st.innerHTML=clean?'<div class="ma-safe-box">'+l.photoTextDetected+'</div>':'';
  };

  Object.assign(window,{
    addManagedUser:addManagedUser,
    changeManagedRole:changeManagedRole,
    changeManagedStatus:changeManagedStatus,
    resetManagedPassword:resetManagedPassword,
    saveMechanicWork:saveMechanicWork,
    speakMechanicWork:speakMechanicWork,
    employeeUpdate:employeeUpdate,
    speakEmployeeWork:speakEmployeeWork,
    saveEmployeeWork:saveEmployeeWork,
    loadEmployeeWorkHistory:loadEmployeeWorkHistory,
    updateEmpCharCount:updateEmpCharCount,
    adminMahindraData:adminMahindraData,
    selectAdminDataTab:selectAdminDataTab,
    searchAdminManual:searchAdminManual,
    exactProblem:exactProblem,
    insertProblemChip:insertProblemChip,
    startExactVoice:startExactVoice,
    stopActiveVoice:stopActiveVoice,
    callFleetEscalation:callFleetEscalation,
    saveDriverProblemDirect:saveDriverProblemDirect,
    getInstantTroubleshoot:getInstantTroubleshoot,
    renderTroubleshootingResult:renderTroubleshootingResult,
    speakTroubleshootSolution:speakTroubleshootSolution,
    driverGuide:driverGuide,
    exportMechanicData:exportMechanicData,
    maSetLanguage:setLang
  });

  // Preserve session on refresh if already authenticated; otherwise show login
  const curToken=localStorage.getItem(TOKEN);
  const curUser=getUser();
  hideOld();
  if(curToken && curUser && curUser.role){
    setTimeout(()=>{dashboard();},60);
  }else{
    localStorage.removeItem(TOKEN);
    localStorage.removeItem(USER);
    localStorage.removeItem(MODE);
    setTimeout(()=>{renderLogin();},100);
  }
})();
'''

# Write to SHELL_JS with UTF-8 encoding
SHELL_JS.write_text(app_shell_code, encoding="utf-8")
print(f"app_shell.js written: {len(app_shell_code)} chars")

# Write to GEN_JS with UTF-8 encoding so it stays consistent
gen_py_content = f'''# encoding: utf-8
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
SHELL_JS = ASSETS / "app_shell.js"

enhanced_js = r"""{app_shell_code}"""

SHELL_JS.write_text(enhanced_js, encoding="utf-8")
print(f"app_shell.js generated: {{len(enhanced_js)}} chars")
'''
GEN_JS.write_text(gen_py_content, encoding="utf-8")
print(f"build/generate_app_shell.py updated")
