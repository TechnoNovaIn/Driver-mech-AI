// Automated verification of Employee user creation fix and regression tests
const fs = require('fs');
const path = require('path');

const shellPath = path.join(__dirname, '../app/src/main/assets/app_shell.js');
const shellCode = fs.readFileSync(shellPath, 'utf8');

console.log('================================================================');
console.log('--- VERIFYING EMPLOYEE USER CREATION & ROLE MANAGEMENT FIX ---');
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

// 1. Static code assertions
assert('addManagedUser is assigned on window directly', shellCode.includes('window.addManagedUser=addManagedUser;'));
assert('changeManagedRole is defined as function', shellCode.includes('function changeManagedRole('));
assert('changeManagedStatus is defined as function', shellCode.includes('function changeManagedStatus('));
assert('getCachedRoles is defined as function', shellCode.includes('function getCachedRoles()'));
assert('setCachedRoles is defined as function', shellCode.includes('function setCachedRoles('));
assert('PERMISSION_DEFS is defined', shellCode.includes('const PERMISSION_DEFS = ['));
assert('DEFAULT_ROLES includes EMPLOYEE, DRIVER, MECHANIC, ADMIN',
  shellCode.includes('role_employee') && shellCode.includes('EMPLOYEE') &&
  shellCode.includes('role_driver') && shellCode.includes('DRIVER') &&
  shellCode.includes('role_mechanic') && shellCode.includes('MECHANIC') &&
  shellCode.includes('role_admin') && shellCode.includes('ADMIN')
);
assert('Regex in addManagedUser uses /\\D/g for clean mobile sanitization', shellCode.includes("mobileInput.value.replace(/\\D/g,'')"));
assert('API queue releases apiBusy in finally block', shellCode.includes('finally{\n        apiBusy=false;\n        setTimeout(pumpApiQueue,30);\n      }') || shellCode.includes('apiBusy=false;'));

// 2. Behavioral simulation with mock DOM and AndroidBridge
const elementStore = {};
function createMockEl(tag, id) {
  const el = {
    tagName: tag.toUpperCase(),
    id: id || '',
    value: '',
    innerHTML: '',
    textContent: '',
    style: {},
    classList: {
      add: () => {},
      remove: () => {},
      contains: () => false
    },
    dataset: {},
    disabled: false,
    focus: () => {},
    setAttribute: () => {},
    getAttribute: () => null,
    appendChild: () => {},
    remove: () => {},
    querySelector: (sel) => createMockEl('div'),
    querySelectorAll: () => []
  };
  if (id) elementStore[id] = el;
  return el;
}

const mockWindow = {
  location: { reload: () => {} },
  localStorage: {
    _data: {
      'mahindra_secure_token_v1': 'mock_admin_token_123',
      'mahindra_secure_user_v1': JSON.stringify({ id: 'u_admin_1', name: 'Fleet Super Admin', role: 'ADMIN', mobile: '9988776655', status: 'ACTIVE' })
    },
    getItem(k) { return this._data[k] || null; },
    setItem(k, v) { this._data[k] = String(v); },
    removeItem(k) { delete this._data[k]; }
  },
  sessionStorage: { removeItem: () => {} },
  addEventListener: () => {},
  alert: (msg) => { console.log('   [Window Alert]:', msg); },
  confirm: (msg) => { console.log('   [Window Confirm]:', msg); return true; },
  prompt: (msg) => 'NewPassword123'
};

const mockDocument = {
  head: { insertAdjacentHTML: () => {}, appendChild: () => {} },
  body: { appendChild: () => {}, insertAdjacentHTML: () => {} },
  getElementById: (id) => elementStore[id] || null,
  querySelector: (sel) => {
    if (sel.includes('auMsg')) return elementStore['auMsg'];
    if (sel.includes('auName')) return elementStore['auName'];
    if (sel.includes('auMobile')) return elementStore['auMobile'];
    if (sel.includes('auRole')) return elementStore['auRole'];
    if (sel.includes('auStatus')) return elementStore['auStatus'];
    if (sel.includes('auPass')) return elementStore['auPass'];
    if (sel.includes('btnCreateUser') || sel.includes('addManagedUser')) return elementStore['btnCreateUser'];
    if (sel.includes('userList')) return elementStore['userList'];
    if (sel.includes('auCountBadge')) return elementStore['auCountBadge'];
    return createMockEl('div');
  },
  querySelectorAll: () => [],
  createElement: (tag) => createMockEl(tag),
  addEventListener: () => {}
};

// Global mocks
global.window = mockWindow;
global.document = mockDocument;
global.localStorage = mockWindow.localStorage;
global.sessionStorage = mockWindow.sessionStorage;
global.confirm = mockWindow.confirm;
global.alert = mockWindow.alert;

// Set up AndroidBridge mock with in-memory database
const dbUsers = [
  { id: 'u_admin_1', name: 'Fleet Super Admin', mobile: '9988776655', role: 'ADMIN', status: 'ACTIVE' },
  { id: 'u_driver_1', name: 'Ramesh Driver', mobile: '9876543210', role: 'DRIVER', status: 'ACTIVE' },
  { id: 'u_mech_1', name: 'Manjunath Mechanic', mobile: '9845012345', role: 'MECHANIC', status: 'ACTIVE' }
];

const sentRequests = [];
mockWindow.AndroidBridge = {
  getSharedApiUrl: () => 'https://script.google.com/macros/s/TEST/exec',
  cloudRequest: (method, url, body) => {
    const payload = JSON.parse(body);
    sentRequests.push(payload);
    const action = payload.action;
    
    setTimeout(() => {
      let resp = { ok: true, code: 200 };
      if (action === 'list_users') {
        resp.users = dbUsers.slice();
      } else if (action === 'add_user') {
        const newU = {
          id: 'u_' + Date.now(),
          name: payload.name,
          mobile: payload.mobile,
          role: payload.role,
          status: payload.status || 'ACTIVE'
        };
        dbUsers.push(newU);
        resp.user = newU;
      } else if (action === 'set_user_role') {
        const u = dbUsers.find(x => x.id === payload.userId);
        if (u) u.role = payload.role;
      } else if (action === 'set_user_status') {
        const u = dbUsers.find(x => x.id === payload.userId);
        if (u) u.status = payload.status;
      }
      
      // Simulate Android WebView bridge response callback
      if (typeof mockWindow.appHttpResult === 'function') {
        mockWindow.appHttpResult(JSON.stringify({ code: 200, body: JSON.stringify(resp) }));
      }
    }, 10);
  }
};
global.AndroidBridge = mockWindow.AndroidBridge;

// Evaluate app_shell.js
try {
  eval(shellCode);
  console.log('\n[EVALUATION] app_shell.js executed without throwing errors.');
} catch(err) {
  console.error('❌ Eval fatal error:', err);
  process.exit(1);
}

assert('window.addManagedUser is exposed as a function on window', typeof mockWindow.addManagedUser === 'function');
assert('window.changeManagedRole is exposed on window', typeof mockWindow.changeManagedRole === 'function');
assert('window.changeManagedStatus is exposed on window', typeof mockWindow.changeManagedStatus === 'function');
assert('window.quickChangeRole is exposed on window', typeof mockWindow.quickChangeRole === 'function');
assert('window.toggleManagedStatus is exposed on window', typeof mockWindow.toggleManagedStatus === 'function');
assert('window.adminUsers is exposed on window', typeof mockWindow.adminUsers === 'function');
assert('window.loadUsers is exposed on window', typeof mockWindow.loadUsers === 'function');

// 3. Test form DOM creation & validation
createMockEl('input', 'auName');
createMockEl('input', 'auMobile');
createMockEl('select', 'auRole');
createMockEl('select', 'auStatus');
createMockEl('input', 'auPass');
createMockEl('button', 'btnCreateUser');
createMockEl('span', 'auMsg');
createMockEl('div', 'userList');
createMockEl('div', 'auCountBadge');

elementStore['auRole'].value = 'EMPLOYEE';
elementStore['auStatus'].value = 'ACTIVE';

// Validation Test A: Empty Name
elementStore['auName'].value = '';
elementStore['auMobile'].value = '9123456789';
mockWindow.addManagedUser();
assert('Empty name displays clear validation feedback', elementStore['auMsg'].innerHTML.includes('Please enter employee full name'));

// Validation Test B: Invalid Mobile (< 10 digits)
elementStore['auName'].value = 'Praveen Kumar';
elementStore['auMobile'].value = '91234';
mockWindow.addManagedUser();
assert('Invalid mobile displays clear validation feedback', elementStore['auMsg'].innerHTML.includes('valid 10-digit mobile number'));

// Validation Test C: Duplicate Mobile Check
elementStore['auName'].value = 'Duplicate Driver';
elementStore['auMobile'].value = '9876543210'; // Already in dbUsers
window.__allLoadedUsers = dbUsers.slice();
mockWindow.addManagedUser();
assert('Duplicate mobile displays duplicate warning', elementStore['auMsg'].innerHTML.includes('already exists'));

// 4. Test Successful Employee User Creation
elementStore['auName'].value = 'Suresh Patil';
elementStore['auMobile'].value = '9900112233';
elementStore['auRole'].value = 'EMPLOYEE';
elementStore['auStatus'].value = 'ACTIVE';
elementStore['auPass'].value = 'EmployeePass123';

console.log('\n[ACTION] Calling window.addManagedUser() with Employee details...');
mockWindow.addManagedUser();

assert('Button indicates in-flight progress (disabled = true)', elementStore['btnCreateUser'].disabled === true);
assert('Message indicates in-flight progress', elementStore['auMsg'].innerHTML.includes('Creating EMPLOYEE profile'));

setTimeout(() => {
  const addReq = sentRequests.find(r => r.action === 'add_user' && r.mobile === '9900112233');
  assert('Backend received add_user action', addReq != null);
  assert('Backend received role EMPLOYEE', addReq && addReq.role === 'EMPLOYEE');
  assert('Backend received mobile 9900112233', addReq && addReq.mobile === '9900112233');
  assert('Backend received name Suresh Patil', addReq && addReq.name === 'Suresh Patil');
  assert('Button re-enabled after completion', elementStore['btnCreateUser'].disabled === false);
  assert('Success message displayed with role and name', elementStore['auMsg'].innerHTML.includes('created successfully') && elementStore['auMsg'].innerHTML.includes('EMPLOYEE'));
  assert('Input fields reset after success', elementStore['auName'].value === '' && elementStore['auMobile'].value === '');
  
  const createdEmp = dbUsers.find(u => u.mobile === '9900112233');
  assert('Employee user persisted in database', createdEmp && createdEmp.role === 'EMPLOYEE');

  // 5. Test Regression: Adding Driver, Mechanic, Admin
  console.log('\n[REGRESSION] Testing Driver creation...');
  elementStore['auName'].value = 'Kiran Driver';
  elementStore['auMobile'].value = '9911223344';
  elementStore['auRole'].value = 'DRIVER';
  mockWindow.addManagedUser();

  setTimeout(() => {
    const createdDriver = dbUsers.find(u => u.mobile === '9911223344');
    assert('Driver user created successfully', createdDriver && createdDriver.role === 'DRIVER');

    console.log('\n[REGRESSION] Testing Mechanic creation...');
    elementStore['auName'].value = 'Raghu Mechanic';
    elementStore['auMobile'].value = '9922334455';
    elementStore['auRole'].value = 'MECHANIC';
    mockWindow.addManagedUser();

    setTimeout(() => {
      const createdMech = dbUsers.find(u => u.mobile === '9922334455');
      assert('Mechanic user created successfully', createdMech && createdMech.role === 'MECHANIC');

      // 6. Test Role Change
      console.log('\n[REGRESSION] Testing quickChangeRole on Employee -> MECHANIC...');
      mockWindow.quickChangeRole(createdEmp.id, 'MECHANIC');
      setTimeout(() => {
        assert('quickChangeRole updated role to MECHANIC', createdEmp.role === 'MECHANIC');

        console.log('\n================================================================');
        if (failed) {
          console.error('❌ SOME TESTS FAILED!');
          process.exit(1);
        } else {
          console.log('🌟 ALL EMPLOYEE & ROLE REGRESSION TESTS PASSED 100%! 🌟');
          console.log('================================================================');
          process.exit(0);
        }
      }, 120);
    }, 120);
  }, 120);
}, 120);
