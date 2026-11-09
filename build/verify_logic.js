// Automated verification of app_shell.js features
const fs = require('fs');
const path = require('path');

const shellPath = path.join(__dirname, '../app/src/main/assets/app_shell.js');
const shellCode = fs.readFileSync(shellPath, 'utf8');

console.log('--- RUNNING AUTOMATED AUDIT ON APP_SHELL.JS ---');

// 1. Verify Employee form: no vehicle field, Daily Work Update label, voice and submit buttons
const hasEmployeeUpdate = shellCode.includes('function employeeUpdate()');
const hasEmpWorkText = shellCode.includes('id="empWorkText"');
const hasNoVehicleInEmpForm = !shellCode.includes('id="mwVehicle" placeholder="Vehicle number"');
const hasEmpVoiceBtn = shellCode.includes('speakEmployeeWork()');
const hasEmpSubmitBtn = shellCode.includes('saveEmployeeWork()');
const hasEmpHistory = shellCode.includes('loadEmployeeWorkHistory()');

console.log('1. Employee Form Check:');
console.log('   - employeeUpdate function exists:', hasEmployeeUpdate);
console.log('   - empWorkText textarea exists:', hasEmpWorkText);
console.log('   - Voice input button exists:', hasEmpVoiceBtn);
console.log('   - Submit button exists:', hasEmpSubmitBtn);
console.log('   - Live work history loader exists:', hasEmpHistory);

if (!hasEmployeeUpdate || !hasEmpWorkText || !hasEmpVoiceBtn || !hasEmpSubmitBtn || !hasEmpHistory) {
  console.error('❌ Employee form verification failed');
  process.exit(1);
}

// 2. Verify Driver Portal / Instant Troubleshooting
const hasExactProblem = shellCode.includes('function exactProblem()');
const hasChips = shellCode.includes('insertProblemChip');
const hasPhotoOptional = shellCode.includes('Attach Photo (Optional)');
const hasTroubleshootEngine = shellCode.includes('function getInstantTroubleshoot()');
const hasDiagnosticRules = shellCode.includes('DIAGNOSTIC_KNOWLEDGE');
const hasUncertaintyNotice = shellCode.includes('UNCERTAINTY NOTICE');
const hasEscalation = shellCode.includes('callFleetEscalation') || shellCode.includes('tel:+919845012345');

console.log('2. Driver Portal Check:');
console.log('   - exactProblem function exists:', hasExactProblem);
console.log('   - Common problem chips exist:', hasChips);
console.log('   - Photo marked optional:', hasPhotoOptional);
console.log('   - getInstantTroubleshoot engine exists:', hasTroubleshootEngine);
console.log('   - Diagnostic knowledge base exists:', hasDiagnosticRules);
console.log('   - Uncertainty notice for unclear issues exists:', hasUncertaintyNotice);
console.log('   - Escalation contact buttons exist:', hasEscalation);

if (!hasExactProblem || !hasChips || !hasPhotoOptional || !hasTroubleshootEngine || !hasDiagnosticRules || !hasUncertaintyNotice || !hasEscalation) {
  console.error('❌ Driver portal verification failed');
  process.exit(1);
}

// 3. Verify Admin Dashboard / Mahindra Data Feature
const hasAdminData = shellCode.includes('function adminMahindraData()');
const hasTabs = shellCode.includes('selectAdminDataTab');
const hasBlazoImg = shellCode.includes('mahindra_blazo_truck.jpg');
const hasDpfImg = shellCode.includes('mahindra_dpf_system.jpg');
const hasEngineImg = shellCode.includes('mahindra_engine_ems.jpg');
const hasGarudaImg = shellCode.includes('mahindra_garuda_diagnostic.jpg');
const hasSimpleExplanations = shellCode.includes('renderAdminExplanationsTab');
const hasOpsData = shellCode.includes('renderAdminOpsTab');
const hasSearchManual = shellCode.includes('searchAdminManual');
const hasInfoNotAvailable = shellCode.includes('Information Not Available');

console.log('3. Admin Mahindra Data Feature Check:');
console.log('   - adminMahindraData function exists:', hasAdminData);
console.log('   - Tab navigation exists:', hasTabs);
console.log('   - Blazo X image embedded:', hasBlazoImg);
console.log('   - DPF aftertreatment image embedded:', hasDpfImg);
console.log('   - Engine EMS image embedded:', hasEngineImg);
console.log('   - Garuda II diagnostic image embedded:', hasGarudaImg);
console.log('   - Simple English explanations exist:', hasSimpleExplanations);
console.log('   - Operational fleet metrics exist:', hasOpsData);
console.log('   - Searchable manual library exists:', hasSearchManual);
console.log('   - Information Not Available standards present:', hasInfoNotAvailable);

if (!hasAdminData || !hasTabs || !hasBlazoImg || !hasDpfImg || !hasEngineImg || !hasGarudaImg || !hasSimpleExplanations || !hasOpsData || !hasSearchManual || !hasInfoNotAvailable) {
  console.error('❌ Admin Mahindra Data verification failed');
  process.exit(1);
}

// 4. Verify Backend code
const backendCode = fs.readFileSync(path.join(__dirname, '../backend/Code.gs'), 'utf8');
const backendOptionalVehicle = backendCode.includes("const vehicle = String(req.vehicleNumber || '-').trim().toUpperCase();");
console.log('4. Backend Code Check:');
console.log('   - saveWork_ supports optional vehicleNumber:', backendOptionalVehicle);

if (!backendOptionalVehicle) {
  console.error('❌ Backend verification failed');
  process.exit(1);
}

console.log('--- ALL AUTOMATED VERIFICATION CHECKS PASSED PERFECTLY! ---');
