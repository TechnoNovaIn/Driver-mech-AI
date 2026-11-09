/**************************************************************
 MAHINDRA BSVI DRIVER & MECHANIC GUIDE — SECURE BACKEND
 Google Apps Script Web App backend.

 IMPORTANT:
 - The APK never receives spreadsheet/database credentials.
 - Passwords are salted + SHA-256 hashed.
 - Session tokens are server-side and expire.
 - Every protected action validates the session and role.
 - USER cannot become ADMIN by changing client-side state.

 ONE-TIME SETUP:
 1. Create/open a Google Apps Script project.
 2. Paste this entire file.
 3. In setBootstrapConfig(), temporarily enter the first admin
    name, 10-digit mobile and a strong admin password.
 4. Run initializeBackend().
 5. Run setBootstrapConfig().
 6. Run setupFirstAdmin().
 7. Remove the temporary bootstrap values/function contents.
 8. Deploy as Web app, Execute as you, access as anyone with the
    deployment URL required by your organization's policy.
 9. Update the existing deployment rather than creating a new URL
    if the APK is already compiled against its current endpoint.
**************************************************************/

const CFG = {
  SESSION_TTL_SECONDS: 8 * 60 * 60,
  USERS_SHEET: 'Users',
  WORK_SHEET: 'DailyWork',
  AUDIT_SHEET: 'AuditLog',
  PROBLEM_SHEET: 'ProblemReports',
  ROLES_SHEET: 'Roles'
};

function setBootstrapConfig() {
  // TEMPORARY ONE-TIME SETUP ONLY.
  // Put values here, run once, then REMOVE them and redeploy.
  PropertiesService.getScriptProperties().setProperties({
    BOOTSTRAP_ADMIN_NAME: 'CHANGE_ME',
    BOOTSTRAP_ADMIN_MOBILE: '0000000000',
    BOOTSTRAP_ADMIN_PASSWORD: 'CHANGE_THIS_TO_A_STRONG_PASSWORD'
  }, false);
}

function initializeBackend() {
  const props = PropertiesService.getScriptProperties();
  let spreadsheetId = props.getProperty('RBAC_SPREADSHEET_ID') || props.getProperty('SPREADSHEET_ID');
  let ss;
  if (spreadsheetId) {
    ss = SpreadsheetApp.openById(spreadsheetId);
  } else {
    ss = SpreadsheetApp.create('MAHINDRA BSVI — Secure Operational Database');
    spreadsheetId = ss.getId();
    props.setProperty('RBAC_SPREADSHEET_ID', spreadsheetId);
    props.setProperty('SPREADSHEET_ID', spreadsheetId);
  }

  ensureSheet_(ss, CFG.USERS_SHEET, [
    'User ID','Name','Mobile','Role','Status','Password Hash','Password Salt',
    'Created At','Updated At'
  ]);
  ensureSheet_(ss, CFG.WORK_SHEET, [
    'Record ID','Date','Vehicle Number','User ID','User Name','Work Completed',
    'Created At'
  ]);
  ensureSheet_(ss, CFG.AUDIT_SHEET, [
    'Timestamp','User ID','Action','Target','Result'
  ]);
  ensureSheet_(ss, CFG.PROBLEM_SHEET, [
    'Report ID','Date','Time','User ID','User Name','Role','Vehicle Number','Problem','Photo Text','Created At'
  ]);
  const rolesSh = ensureSheet_(ss, CFG.ROLES_SHEET, [
    'Role ID', 'Role Name', 'Description', 'Permissions', 'Sort Order', 'Created At', 'Updated At'
  ]);
  seedDefaultRoles_(rolesSh);
  return 'Backend initialized. RBAC spreadsheet ID: ' + spreadsheetId;
}

function doGet(e) {
  return json_({ ok: true, service: 'MAHINDRA BSVI secure backend', status: 'online' });
}

function doPost(e) {
  try {
    const req = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const action = String(req.action || '').trim();

    if (action === 'login') return json_(login_(req));
    if (action === 'logout') return json_(logout_(req));
    if (action === 'me') { const s = requireSession_(req); return json_(s.ok ? {ok:true,code:200,user:publicUser_(s.internalUser)} : s); }

    const session = requireSession_(req);
    if (!session.ok) return json_(session);

    switch (action) {
      case 'save_work':
        return json_(saveWork_(req, session.internalUser));
      case 'list_work':
        return json_(listWork_(req, session.internalUser));
      case 'export_work':
        return json_(exportWork_(req, session.internalUser));
      case 'list_users':
        return json_(listUsers_(req, session.internalUser));
      case 'add_user':
        return json_(addUser_(req, session.internalUser));
      case 'update_user':
        return json_(updateUser_(req, session.internalUser));
      case 'set_user_status':
        return json_(setUserStatus_(req, session.internalUser));
      case 'set_user_role':
        return json_(setUserRole_(req, session.internalUser));
      case 'set_user_password':
        return json_(setUserPassword_(req, session.internalUser));
      case 'list_roles':
        return json_(listRoles_(req, session.internalUser));
      case 'create_role':
        return json_(createRole_(req, session.internalUser));
      case 'update_role':
        return json_(updateRole_(req, session.internalUser));
      case 'delete_role':
        return json_(deleteRole_(req, session.internalUser));
      case 'save_role_permissions':
        return json_(saveRolePermissions_(req, session.internalUser));
      case 'reorder_roles':
        return json_(reorderRoles_(req, session.internalUser));
      case 'sync':
        return json_(sync_(req, session.internalUser));
      case 'save_problem':
        return json_(saveProblem_(req, session.internalUser));
      case 'list_problems':
        return json_(listProblems_(req, session.internalUser));
      default:
        return json_({ ok:false, code:400, error:'Unknown action.' });
    }
  } catch (err) {
    return json_({ ok:false, code:500, error:'Server error.' });
  }
}

function json_(obj) {
  // Apps Script ContentService is the supported way to return raw JSON.
  // Google may redirect the response to script.googleusercontent.com;
  // the Android client explicitly follows that redirect and preserves
  // the Apps Script session cookie / gsessionid.
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function ensureSheet_(ss, name, headers) {
  let sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);
  if (sh.getLastRow() === 0) sh.appendRow(headers);
  return sh;
}

function db_() {
  const id = PropertiesService.getScriptProperties().getProperty('RBAC_SPREADSHEET_ID');
  if (!id) throw new Error('Backend not initialized.');
  return SpreadsheetApp.openById(id);
}

function users_() { return db_().getSheetByName(CFG.USERS_SHEET); }
function work_() { return db_().getSheetByName(CFG.WORK_SHEET); }
function audit_() { return db_().getSheetByName(CFG.AUDIT_SHEET); }

function now_() {
  return new Date().toISOString();
}

function uuid_() {
  return Utilities.getUuid();
}

function normalizeMobile_(v) {
  return String(v || '').replace(/\D/g, '');
}

function validMobile_(v) {
  return /^\d{10}$/.test(String(v || ''));
}

function bytesToHex_(bytes) {
  return bytes.map(function(b) {
    const n = b < 0 ? b + 256 : b;
    return ('0' + n.toString(16)).slice(-2);
  }).join('');
}

function hashPassword_(password, salt) {
  const raw = String(salt) + ':' + String(password);
  return bytesToHex_(Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256, raw, Utilities.Charset.UTF_8
  ));
}

function randomToken_() {
  const seed = Utilities.getUuid() + ':' + new Date().getTime() + ':' + Math.random();
  return bytesToHex_(Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256, seed, Utilities.Charset.UTF_8
  )) + Utilities.getUuid().replace(/-/g,'');
}

function tokenHash_(token) {
  return bytesToHex_(Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256, String(token), Utilities.Charset.UTF_8
  ));
}

function findUserByMobile_(mobile) {
  const sh = users_();
  const values = sh.getDataRange().getValues();
  const cleanM = normalizeMobile_(mobile);
  for (let i = 1; i < values.length; i++) {
    if (normalizeMobile_(values[i][2]) === cleanM) {
      return { row: i + 1, data: values[i] };
    }
  }
  return null;
}

function findUserById_(id) {
  const sh = users_();
  const values = sh.getDataRange().getValues();
  const cleanId = String(id || '').trim();
  for (let i = 1; i < values.length; i++) {
    if (String(values[i][0]).trim() === cleanId) {
      return { row: i + 1, data: values[i] };
    }
  }
  return null;
}

function publicUser_(u) {
  return {
    id: String(u.data[0]),
    name: String(u.data[1]),
    mobile: normalizeMobile_(u.data[2]),
    role: String(u.data[3]).trim().toUpperCase(),
    status: String(u.data[4]).trim().toUpperCase()
  };
}

function addSession_(user) {
  const token = randomToken_();
  const key = 'SESSION_' + tokenHash_(token);
  const payload = {
    userId: String(user.data[0]),
    expiresAt: Date.now() + CFG.SESSION_TTL_SECONDS * 1000
  };
  const pr = PropertiesService.getScriptProperties();
  try {
    const all = pr.getProperties(), nowMs = Date.now();
    for (const k in all) {
      if (k.indexOf('SESSION_') === 0) {
        try { const parsed = JSON.parse(all[k]); if (nowMs >= Number(parsed.expiresAt)) pr.deleteProperty(k); } catch(e) { pr.deleteProperty(k); }
      }
    }
  } catch(e) {}
  pr.setProperty(key, JSON.stringify(payload));
  return { token: token, expiresAt: payload.expiresAt };
}

function requireSession_(req) {
  const token = String(req.token || '');
  if (!token) return { ok:false, code:401, error:'Authentication required.' };

  const key = 'SESSION_' + tokenHash_(token);
  const props = PropertiesService.getScriptProperties();
  const raw = props.getProperty(key);
  if (!raw) return { ok:false, code:401, error:'Session expired or invalid.' };

  let session;
  try { session = JSON.parse(raw); } catch (_) {
    props.deleteProperty(key);
    return { ok:false, code:401, error:'Invalid session.' };
  }

  if (!session.expiresAt || Date.now() >= Number(session.expiresAt)) {
    props.deleteProperty(key);
    return { ok:false, code:401, error:'Session expired.' };
  }

  const found = findUserById_(session.userId);
  if (!found || String(found.data[4]) !== 'ACTIVE') {
    props.deleteProperty(key);
    return { ok:false, code:403, error:'Account disabled or unavailable.' };
  }

  return { ok:true, code:200, user:publicUser_(found), internalUser:found };
}

function requireAdmin_(user) {
  if (!user) return { ok:false, code:401, error:'Authentication required.' };
  if (String(user.data[3]).toUpperCase() === 'ADMIN') return { ok:true };
  return { ok:false, code:403, error:'Administrator permission required.' };
}

function requirePermission_(user, permissionKey) {
  if (!user) return { ok:false, code:401, error:'Authentication required.' };
  const roleName = String(user.data[3]).toUpperCase();
  if (roleName === 'ADMIN') return { ok:true }; // Administrator has unrestricted permissions
  
  const perms = getPermissionsForRole_(roleName);
  if (perms && perms.indexOf(permissionKey) !== -1) {
    return { ok:true };
  }
  return { ok:false, code:403, error:'Access denied: requires permission ' + permissionKey };
}

function login_(req) {
  const mobile = normalizeMobile_(req.username);
  const password = String(req.password || '');

  if (!validMobile_(mobile) || !password) {
    return { ok:false, code:401, error:'Mobile number or password is incorrect.' };
  }

  const found = findUserByMobile_(mobile);
  if (!found) return { ok:false, code:401, error:'Mobile number or password is incorrect.' };

  const u = found.data;
  if (String(u[4]) !== 'ACTIVE') {
    return { ok:false, code:403, error:'This account is disabled.' };
  }

  const expected = hashPassword_(password, String(u[6]));
  if (expected !== String(u[5])) {
    audit_().appendRow([now_(), String(u[0]), 'LOGIN', 'AUTH', 'FAILED']);
    return { ok:false, code:401, error:'Mobile number or password is incorrect.' };
  }

  const session = addSession_(found);
  audit_().appendRow([now_(), String(u[0]), 'LOGIN', 'AUTH', 'SUCCESS']);
  return {
    ok:true, code:200,
    token:session.token,
    expiresAt:session.expiresAt,
    user:publicUser_(found)
  };
}

function logout_(req) {
  const token = String(req.token || '');
  if (token) {
    PropertiesService.getScriptProperties().deleteProperty('SESSION_' + tokenHash_(token));
  }
  return { ok:true, code:200 };
}

function saveWork_(req, sessionUser) {
  const date = String(req.date || '').trim();
  const vehicle = String(req.vehicleNumber || '-').trim().toUpperCase();
  const work = String(req.workCompleted || '').trim();

  if (!date || !work) {
    return { ok:false, code:400, error:'Date and work details are required.' };
  }

  const recordId = uuid_();
  work_().appendRow([
    recordId,
    date,
    vehicle,
    String(sessionUser.data[0]),
    String(sessionUser.data[1]),
    work,
    now_()
  ]);

  audit_().appendRow([
    now_(), String(sessionUser.data[0]), 'SAVE_WORK', recordId, 'SUCCESS'
  ]);

  return { ok:true, code:200, recordId:recordId };
}

function listWork_(req, sessionUser) {
  const admin = String(sessionUser.data[3]) === 'ADMIN';
  const sh = work_();
  const values = sh.getDataRange().getValues();
  const filters = req.filters || {};
  const out = [];

  for (let i = 1; i < values.length; i++) {
    const r = values[i];
    if (!r[0]) continue;

    if (!admin && String(r[3]) !== String(sessionUser.data[0])) continue;
    if (filters.date && String(r[1]) !== String(filters.date)) continue;
    if (filters.vehicle && String(r[2]).indexOf(String(filters.vehicle).toUpperCase()) === -1) continue;
    if (filters.userId && String(r[3]) !== String(filters.userId)) continue;
    if (filters.mechanic && String(r[4]).toLowerCase().indexOf(String(filters.mechanic).toLowerCase()) === -1) continue;

    out.push({
      id:String(r[0]),
      date:sheetDate_(r[1]),
      vehicleNumber:String(r[2]),
      userId:String(r[3]),
      userName:String(r[4]),
      workCompleted:String(r[5]),
      createdAt:String(r[6])
    });
  }

  out.reverse();
  return { ok:true, code:200, records:out };
}

function sheetDate_(v) {
  if (Object.prototype.toString.call(v) === '[object Date]' && !isNaN(v.getTime())) {
    return Utilities.formatDate(v, Session.getScriptTimeZone() || 'Asia/Kolkata', 'yyyy-MM-dd');
  }
  const text = String(v == null ? '' : v).trim();
  const m = text.match(/^(\d{4})-(\d{2})-(\d{2})/);
  return m ? m[0] : text;
}

function exportWork_(req, sessionUser) {
  const gate = requireAdmin_(sessionUser);
  if (!gate.ok) return gate;

  const result = listWork_(req, sessionUser);
  if (!result.ok) return result;

  const lines = [
    'Date,Vehicle Number,User ID,User Name,Work Completed,Created At'
  ];
  result.records.forEach(function(r) {
    lines.push([
      r.date, r.vehicleNumber, r.userId, r.userName, r.workCompleted, r.createdAt
    ].map(csv_).join(','));
  });

  audit_().appendRow([now_(), String(sessionUser.data[0]), 'EXPORT_WORK', 'ALL', 'SUCCESS']);
  return { ok:true, code:200, csv:lines.join('\r\n') };
}

function csv_(v) {
  return '"' + String(v == null ? '' : v).replace(/"/g, '""') + '"';
}

function listUsers_(req, sessionUser) {
  const gate = requireAdmin_(sessionUser);
  if (!gate.ok) return gate;

  const sh = users_();
  const values = sh.getDataRange().getValues();
  const q = String(req.query || '').toLowerCase().trim();
  const out = [];

  for (let i = 1; i < values.length; i++) {
    if (!values[i][0]) continue;
    const pub = publicUser_({data:values[i]});
    const hay = (pub.name + ' ' + pub.mobile + ' ' + pub.role + ' ' + pub.status).toLowerCase();
    if (q && hay.indexOf(q) === -1) continue;
    out.push(pub);
  }

  return { ok:true, code:200, users:out };
}

function roles_() {
  const ss = db_();
  let sh = ss.getSheetByName(CFG.ROLES_SHEET);
  if (!sh) {
    sh = ensureSheet_(ss, CFG.ROLES_SHEET, [
      'Role ID', 'Role Name', 'Description', 'Permissions', 'Sort Order', 'Created At', 'Updated At'
    ]);
    seedDefaultRoles_(sh);
  }
  return sh;
}

function seedDefaultRoles_(sh) {
  if (sh.getLastRow() > 1) return;
  const ts = now_();
  const defaults = [
    [
      'role_admin', 'ADMIN',
      'System Administrator with complete access to all dashboards, user accounts, and system configurations.',
      JSON.stringify(['manage_employees','create_edit_roles','assign_roles','manage_permissions','view_admin_dashboard','view_employee_dashboard','submit_work_updates','view_vehicle_info']),
      1, ts, ts
    ],
    [
      'role_mechanic', 'MECHANIC',
      'Service technician handling vehicle repairs, work logs, parts replacement, and diagnostics.',
      JSON.stringify(['view_employee_dashboard','submit_work_updates','view_vehicle_info']),
      2, ts, ts
    ],
    [
      'role_employee', 'EMPLOYEE',
      'Fleet operations employee submitting daily task updates and attendance.',
      JSON.stringify(['view_employee_dashboard','submit_work_updates']),
      3, ts, ts
    ],
    [
      'role_driver', 'DRIVER',
      'Commercial vehicle driver reporting problems, viewing guides, and requesting assistance.',
      JSON.stringify(['view_vehicle_info']),
      4, ts, ts
    ]
  ];
  defaults.forEach(function(r) { sh.appendRow(r); });
}

function getAllRoles_() {
  const sh = roles_();
  const rows = sh.getDataRange().getValues();
  const userCounts = {};
  try {
    const uRows = users_().getDataRange().getValues();
    for (let j = 1; j < uRows.length; j++) {
      const r = String(uRows[j][3]).trim().toUpperCase();
      userCounts[r] = (userCounts[r] || 0) + 1;
    }
  } catch(e) {}

  const roles = [];
  for (let i = 1; i < rows.length; i++) {
    const r = rows[i];
    if (!r[0]) continue;
    let perms = [];
    try { perms = JSON.parse(r[3] || '[]'); } catch(_) { perms = []; }
    const roleName = String(r[1]).trim().toUpperCase();
    roles.push({
      id: String(r[0]),
      name: roleName,
      description: String(r[2] || ''),
      permissions: perms,
      sortOrder: Number(r[4] || i),
      userCount: userCounts[roleName] || 0,
      isSystemRole: ['ADMIN', 'MECHANIC', 'EMPLOYEE', 'DRIVER'].indexOf(roleName) !== -1,
      createdAt: String(r[5] || ''),
      updatedAt: String(r[6] || '')
    });
  }
  roles.sort(function(a,b) { return (a.sortOrder || 0) - (b.sortOrder || 0); });
  return roles;
}

function getPermissionsForRole_(roleName) {
  try {
    const sh = roles_();
    const rows = sh.getDataRange().getValues();
    const norm = String(roleName || '').trim().toUpperCase();
    for (let i = 1; i < rows.length; i++) {
      if (String(rows[i][1]).trim().toUpperCase() === norm) {
        let p = [];
        try { p = JSON.parse(rows[i][3] || '[]'); } catch(_) { p = []; }
        return p;
      }
    }
  } catch(e) {}
  const norm = String(roleName || '').trim().toUpperCase();
  if (norm === 'ADMIN') return ['manage_employees','create_edit_roles','assign_roles','manage_permissions','view_admin_dashboard','view_employee_dashboard','submit_work_updates','view_vehicle_info'];
  if (norm === 'MECHANIC') return ['view_employee_dashboard','submit_work_updates','view_vehicle_info'];
  if (norm === 'EMPLOYEE') return ['view_employee_dashboard','submit_work_updates'];
  if (norm === 'DRIVER') return ['view_vehicle_info'];
  return [];
}

function listRoles_(req, sessionUser) {
  const gate = requirePermission_(sessionUser, 'manage_permissions');
  if (!gate.ok && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') {
    const fallbackGate = requirePermission_(sessionUser, 'manage_employees');
    if (!fallbackGate.ok && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') return gate;
  }
  return { ok: true, code: 200, roles: getAllRoles_() };
}

function createRole_(req, sessionUser) {
  const gate = requirePermission_(sessionUser, 'create_edit_roles');
  if (!gate.ok && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') return gate;

  const name = String(req.name || '').trim().toUpperCase();
  const desc = String(req.description || '').trim();
  let permissions = req.permissions;
  if (!Array.isArray(permissions)) permissions = [];

  if (!name || name.length < 2) {
    return { ok: false, code: 400, error: 'Role name must be at least 2 characters.' };
  }
  if (!/^[A-Z0-9_\-\s]+$/.test(name)) {
    return { ok: false, code: 400, error: 'Role name can only contain letters, numbers, spaces, underscores, or hyphens.' };
  }

  const existing = getAllRoles_();
  for (let i = 0; i < existing.length; i++) {
    if (existing[i].name.toUpperCase() === name) {
      return { ok: false, code: 409, error: 'A role with this name already exists.' };
    }
  }

  const sh = roles_();
  const roleId = 'role_' + Utilities.getUuid().slice(0, 8);
  let maxOrder = 0;
  for (let j = 0; j < existing.length; j++) {
    if ((existing[j].sortOrder || 0) > maxOrder) maxOrder = existing[j].sortOrder;
  }
  const ts = now_();

  sh.appendRow([
    roleId, name, desc, JSON.stringify(permissions), maxOrder + 1, ts, ts
  ]);

  audit_().appendRow([ts, String(sessionUser.data[0]), 'CREATE_ROLE', roleId, name]);

  return {
    ok: true,
    code: 200,
    role: { id: roleId, name: name, description: desc, permissions: permissions, sortOrder: maxOrder + 1, userCount: 0 }
  };
}

function updateRole_(req, sessionUser) {
  const gate = requirePermission_(sessionUser, 'create_edit_roles');
  if (!gate.ok && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') return gate;

  const roleId = String(req.roleId || '').trim();
  const newName = String(req.name || '').trim().toUpperCase();
  const desc = String(req.description || '').trim();
  let permissions = req.permissions;
  if (!Array.isArray(permissions)) permissions = null;

  if (!roleId) return { ok: false, code: 400, error: 'Role ID is required.' };
  if (!newName || newName.length < 2) return { ok: false, code: 400, error: 'Role name must be at least 2 characters.' };

  const sh = roles_();
  const rows = sh.getDataRange().getValues();
  let targetRow = -1;
  let oldRoleName = '';
  for (let i = 1; i < rows.length; i++) {
    if (String(rows[i][0]) === roleId) {
      targetRow = i + 1;
      oldRoleName = String(rows[i][1]).trim().toUpperCase();
      break;
    }
  }

  if (targetRow === -1) return { ok: false, code: 404, error: 'Role not found.' };

  if (oldRoleName === 'ADMIN' && newName !== 'ADMIN') {
    return { ok: false, code: 400, error: 'The ADMIN system role cannot be renamed.' };
  }

  if (newName !== oldRoleName) {
    for (let i = 1; i < rows.length; i++) {
      if (i + 1 !== targetRow && String(rows[i][1]).trim().toUpperCase() === newName) {
        return { ok: false, code: 409, error: 'Another role with this name already exists.' };
      }
    }
  }

  const ts = now_();
  sh.getRange(targetRow, 2).setValue(newName);
  sh.getRange(targetRow, 3).setValue(desc);
  if (permissions !== null) {
    if (newName === 'ADMIN') {
      const required = ['manage_employees','create_edit_roles','assign_roles','manage_permissions','view_admin_dashboard'];
      for (let k = 0; k < required.length; k++) {
        if (permissions.indexOf(required[k]) === -1) permissions.push(required[k]);
      }
    }
    sh.getRange(targetRow, 4).setValue(JSON.stringify(permissions));
  }
  sh.getRange(targetRow, 7).setValue(ts);

  if (newName !== oldRoleName) {
    const uSh = users_();
    const uRows = uSh.getDataRange().getValues();
    for (let j = 1; j < uRows.length; j++) {
      if (String(uRows[j][3]).trim().toUpperCase() === oldRoleName) {
        uSh.getRange(j + 1, 4).setValue(newName);
        uSh.getRange(j + 1, 9).setValue(ts);
      }
    }
  }

  audit_().appendRow([ts, String(sessionUser.data[0]), 'UPDATE_ROLE', roleId, newName]);
  return { ok: true, code: 200 };
}

function saveRolePermissions_(req, sessionUser) {
  const gate = requirePermission_(sessionUser, 'manage_permissions');
  if (!gate.ok && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') return gate;

  const roleId = String(req.roleId || '').trim();
  let permissions = req.permissions;
  if (!Array.isArray(permissions)) permissions = [];

  const sh = roles_();
  const rows = sh.getDataRange().getValues();
  let targetRow = -1;
  let roleName = '';
  for (let i = 1; i < rows.length; i++) {
    if (String(rows[i][0]) === roleId) {
      targetRow = i + 1;
      roleName = String(rows[i][1]).trim().toUpperCase();
      break;
    }
  }
  if (targetRow === -1) return { ok: false, code: 404, error: 'Role not found.' };

  if (roleName === 'ADMIN') {
    const required = ['manage_employees','create_edit_roles','assign_roles','manage_permissions','view_admin_dashboard'];
    for (let k = 0; k < required.length; k++) {
      if (permissions.indexOf(required[k]) === -1) permissions.push(required[k]);
    }
  }

  const ts = now_();
  sh.getRange(targetRow, 4).setValue(JSON.stringify(permissions));
  sh.getRange(targetRow, 7).setValue(ts);

  audit_().appendRow([ts, String(sessionUser.data[0]), 'SAVE_ROLE_PERMS', roleId, JSON.stringify(permissions)]);
  return { ok: true, code: 200 };
}

function reorderRoles_(req, sessionUser) {
  const gate = requirePermission_(sessionUser, 'manage_permissions');
  if (!gate.ok && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') return gate;

  const orderedIds = req.orderedIds;
  if (!Array.isArray(orderedIds) || !orderedIds.length) {
    return { ok: false, code: 400, error: 'orderedIds array required.' };
  }

  const sh = roles_();
  const rows = sh.getDataRange().getValues();
  const idToRow = {};
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0]) idToRow[String(rows[i][0])] = i + 1;
  }

  for (let idx = 0; idx < orderedIds.length; idx++) {
    const id = orderedIds[idx];
    const row = idToRow[String(id)];
    if (row) {
      sh.getRange(row, 5).setValue(idx + 1);
    }
  }

  return { ok: true, code: 200 };
}

function deleteRole_(req, sessionUser) {
  const gate = requireAdmin_(sessionUser);
  if (!gate.ok) return gate;

  const roleId = String(req.roleId || '').trim();
  const sh = roles_();
  const rows = sh.getDataRange().getValues();
  let targetRow = -1;
  let roleName = '';
  for (let i = 1; i < rows.length; i++) {
    if (String(rows[i][0]) === roleId) {
      targetRow = i + 1;
      roleName = String(rows[i][1]).trim().toUpperCase();
      break;
    }
  }
  if (targetRow === -1) return { ok: false, code: 404, error: 'Role not found.' };

  if (['ADMIN', 'DRIVER', 'MECHANIC', 'EMPLOYEE'].indexOf(roleName) !== -1) {
    return { ok: false, code: 400, error: 'System roles cannot be deleted.' };
  }

  const uSh = users_();
  const uRows = uSh.getDataRange().getValues();
  for (let j = 1; j < uRows.length; j++) {
    if (String(uRows[j][3]).trim().toUpperCase() === roleName) {
      return { ok: false, code: 400, error: 'Cannot delete role "' + roleName + '" because employees are currently assigned to it. Re-assign them first.' };
    }
  }

  sh.deleteRow(targetRow);
  audit_().appendRow([now_(), String(sessionUser.data[0]), 'DELETE_ROLE', roleId, roleName]);
  return { ok: true, code: 200 };
}

function addUser_(req, sessionUser) {
  const gate = requirePermission_(sessionUser, 'manage_employees');
  if (!gate.ok && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') return gate;

  const name = String(req.name || '').trim();
  const mobile = normalizeMobile_(req.mobile);
  const role = String(req.role || 'DRIVER').toUpperCase();
  const requestedPassword = String(req.password || '').trim();
  const status = String(req.status || 'ACTIVE').toUpperCase() === 'DISABLED' ? 'DISABLED' : 'ACTIVE';

  if (!name || !validMobile_(mobile)) {
    return { ok:false, code:400, error:'Enter a name and a valid 10-digit mobile number.' };
  }

  const existingRoles = getAllRoles_().map(function(r) { return r.name.toUpperCase(); });
  existingRoles.push('ADMIN', 'MECHANIC', 'EMPLOYEE', 'DRIVER', 'USER');
  if (existingRoles.indexOf(role) === -1) {
    return { ok:false, code:400, error:'Invalid role: ' + role };
  }

  if (findUserByMobile_(mobile)) {
    return { ok:false, code:409, error:'A user with this mobile number already exists.' };
  }

  // Prevent non-admin from creating an ADMIN account
  if (role === 'ADMIN' && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') {
    return { ok:false, code:403, error:'Only an administrator can create an ADMIN account.' };
  }

  const salt = randomToken_().slice(0,32);
  const initialPassword = requestedPassword || mobile.slice(-4);
  const userId = uuid_();
  const timestamp = now_();

  const sh = users_();
  sh.appendRow([
    userId, name, mobile, role, status,
    hashPassword_(initialPassword, salt), salt,
    timestamp, timestamp
  ]);
  try { sh.getRange(sh.getLastRow(), 3).setNumberFormat('@'); } catch(_) {}

  audit_().appendRow([timestamp, String(sessionUser.data[0]), 'ADD_USER', userId, 'SUCCESS']);

  return {
    ok:true, code:200,
    user:{id:userId, name:name, mobile:mobile, role:role, status:status},
    initialPasswordRule: requestedPassword ? 'Admin-set password' : 'Last 4 digits of mobile number'
  };
}

function updateUser_(req, sessionUser) {
  const gate = requirePermission_(sessionUser, 'manage_employees');
  if (!gate.ok && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') return gate;

  const userId = String(req.userId || '').trim();
  const name = String(req.name || '').trim();
  const mobile = normalizeMobile_(req.mobile);
  const role = String(req.role || '').trim().toUpperCase();
  const status = String(req.status || 'ACTIVE').trim().toUpperCase();

  if (!userId) return { ok: false, code: 400, error: 'User ID is required.' };
  if (!name || !validMobile_(mobile)) {
    return { ok: false, code: 400, error: 'Enter a valid name and 10-digit mobile number.' };
  }

  const found = findUserById_(userId);
  if (!found) return { ok: false, code: 404, error: 'User not found.' };

  const existingRoles = getAllRoles_().map(function(r) { return r.name.toUpperCase(); });
  existingRoles.push('ADMIN', 'MECHANIC', 'EMPLOYEE', 'DRIVER', 'USER');
  if (existingRoles.indexOf(role) === -1) {
    return { ok: false, code: 400, error: 'Invalid role: ' + role };
  }

  // Prevent non-admin from assigning ADMIN role
  if (role === 'ADMIN' && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') {
    return { ok: false, code: 403, error: 'Only an administrator can assign the ADMIN role.' };
  }

  // Check mobile uniqueness if changed
  if (mobile !== String(found.data[2])) {
    const existing = findUserByMobile_(mobile);
    if (existing && String(existing.data[0]) !== userId) {
      return { ok: false, code: 409, error: 'A user with this mobile number already exists.' };
    }
  }

  // Protect last active administrator from demotion or disablement
  const currentRole = String(found.data[3]).toUpperCase();
  if (currentRole === 'ADMIN' && (role !== 'ADMIN' || status !== 'ACTIVE')) {
    const all = users_().getDataRange().getValues();
    let activeAdminsCount = 0;
    for (let i = 1; i < all.length; i++) {
      if (String(all[i][3]).toUpperCase() === 'ADMIN' && String(all[i][4]).toUpperCase() === 'ACTIVE' && String(all[i][0]) !== userId) {
        activeAdminsCount++;
      }
    }
    if (activeAdminsCount === 0) {
      return { ok: false, code: 400, error: 'The last active administrator cannot be demoted or deactivated.' };
    }
  }

  // Prevent admin from removing their own admin role
  if (String(found.data[0]) === String(sessionUser.data[0]) && role !== 'ADMIN') {
    return { ok: false, code: 400, error: 'You cannot remove your own administrator role.' };
  }

  const ts = now_();
  users_().getRange(found.row, 2).setValue(name);
  users_().getRange(found.row, 3).setValue(mobile);
  users_().getRange(found.row, 4).setValue(role);
  users_().getRange(found.row, 5).setValue(status);
  users_().getRange(found.row, 9).setValue(ts);

  audit_().appendRow([ts, String(sessionUser.data[0]), 'UPDATE_USER', userId, 'SUCCESS']);

  return {
    ok: true,
    code: 200,
    user: { id: userId, name: name, mobile: mobile, role: role, status: status }
  };
}

function setUserStatus_(req, sessionUser) {
  const gate = requirePermission_(sessionUser, 'manage_employees');
  if (!gate.ok && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') return gate;

  const userId = String(req.userId || '');
  const status = String(req.status || '').toUpperCase();
  if (status !== 'ACTIVE' && status !== 'DISABLED') {
    return { ok:false, code:400, error:'Invalid status.' };
  }

  const found = findUserById_(userId);
  if (!found) return { ok:false, code:404, error:'User not found.' };

  // Prevent accidental lockout of the last active admin.
  if (status === 'DISABLED' && String(found.data[3]) === 'ADMIN') {
    const all = users_().getDataRange().getValues();
    let activeAdminsCount = 0;
    for (let i = 1; i < all.length; i++) {
      if (String(all[i][3]).toUpperCase() === 'ADMIN' && String(all[i][4]).toUpperCase() === 'ACTIVE') {
        activeAdminsCount++;
      }
    }
    if (activeAdminsCount <= 1) {
      return { ok:false, code:400, error:'The last active admin cannot be disabled.' };
    }
  }

  users_().getRange(found.row, 5).setValue(status);
  users_().getRange(found.row, 9).setValue(now_());

  audit_().appendRow([now_(), String(sessionUser.data[0]), 'SET_USER_STATUS', userId, status]);
  return { ok:true, code:200 };
}

function setUserRole_(req, sessionUser) {
  const gate = requirePermission_(sessionUser, 'assign_roles');
  if (!gate.ok && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') return gate;

  const userId = String(req.userId || '');
  const role = String(req.role || '').toUpperCase();

  const existingRoles = getAllRoles_().map(function(r) { return r.name.toUpperCase(); });
  existingRoles.push('ADMIN', 'MECHANIC', 'EMPLOYEE', 'DRIVER', 'USER');
  if (existingRoles.indexOf(role) === -1) {
    return { ok:false, code:400, error:'Invalid role: ' + role };
  }

  const found = findUserById_(userId);
  if (!found) return { ok:false, code:404, error:'User not found.' };

  // Prevent non-admin from assigning ADMIN role
  if (role === 'ADMIN' && String(sessionUser.data[3]).toUpperCase() !== 'ADMIN') {
    return { ok:false, code:403, error:'Only an administrator can assign the ADMIN role.' };
  }

  // Protect last active administrator from demotion
  if (String(found.data[3]).toUpperCase() === 'ADMIN' && role !== 'ADMIN') {
    const all = users_().getDataRange().getValues();
    let activeAdminsCount = 0;
    for (let i = 1; i < all.length; i++) {
      if (String(all[i][3]).toUpperCase() === 'ADMIN' && String(all[i][4]).toUpperCase() === 'ACTIVE' && String(all[i][0]) !== userId) {
        activeAdminsCount++;
      }
    }
    if (activeAdminsCount === 0) {
      return { ok:false, code:400, error:'The last active administrator cannot be demoted.' };
    }
  }

  if (String(found.data[0]) === String(sessionUser.data[0]) && role !== 'ADMIN') {
    return { ok:false, code:400, error:'The current admin cannot remove their own admin role.' };
  }

  users_().getRange(found.row, 4).setValue(role);
  users_().getRange(found.row, 9).setValue(now_());
  audit_().appendRow([now_(), String(sessionUser.data[0]), 'SET_USER_ROLE', userId, role]);

  return { ok:true, code:200 };
}

function sync_(req, sessionUser) {
  return listWork_(req, sessionUser);
}

function setUserPassword_(req, sessionUser) {
  const gate = requireAdmin_(sessionUser);
  if (!gate.ok) return gate;
  const userId = String(req.userId || '');
  const password = String(req.password || '');
  if (password.length < 8) return { ok:false, code:400, error:'Password must be at least 8 characters.' };
  const found = findUserById_(userId);
  if (!found) return { ok:false, code:404, error:'User not found.' };
  const salt = randomToken_().slice(0,32);
  users_().getRange(found.row, 6).setValue(hashPassword_(password, salt));
  users_().getRange(found.row, 7).setValue(salt);
  users_().getRange(found.row, 9).setValue(now_());
  audit_().appendRow([now_(), String(sessionUser.data[0]), 'SET_USER_PASSWORD', userId, 'SUCCESS']);
  return { ok:true, code:200 };
}

function saveProblem_(req, sessionUser) {
  const vehicle = String(req.vehicleNumber || '').trim().toUpperCase();
  const problem = String(req.problem || '').trim();
  const photoText = String(req.photoText || '').trim();
  if (!problem && !photoText) return { ok:false, code:400, error:'Problem details are required.' };
  const now = new Date();
  const reportId = uuid_();
  const date = Utilities.formatDate(now, Session.getScriptTimeZone(), 'yyyy-MM-dd');
  const time = Utilities.formatDate(now, Session.getScriptTimeZone(), 'HH:mm:ss');
  const u = sessionUser.data;
  db_().getSheetByName(CFG.PROBLEM_SHEET).appendRow([
    reportId,date,time,String(u[0]),String(u[1]),String(u[3]),vehicle,problem,photoText,now_()
  ]);
  audit_().appendRow([now_(), String(u[0]), 'SAVE_PROBLEM', reportId, 'SUCCESS']);
  return { ok:true, code:200, reportId:reportId };
}

function listProblems_(req, sessionUser) {
  const admin = String(sessionUser.data[3]) === 'ADMIN';
  const sh = db_().getSheetByName(CFG.PROBLEM_SHEET);
  const values = sh.getDataRange().getValues();
  const out = [];
  for (let i=1;i<values.length;i++) {
    const r=values[i]; if(!r[0]) continue;
    if(!admin && String(r[3]) !== String(sessionUser.data[0])) continue;
    out.push({
      id:String(r[0]),date:String(r[1]),time:String(r[2]),userId:String(r[3]),
      userName:String(r[4]),role:String(r[5]),vehicleNumber:String(r[6]),
      problem:String(r[7]),photoText:String(r[8]),createdAt:String(r[9])
    });
  }
  out.reverse();
  return { ok:true, code:200, records:out };
}

function setupFirstAdmin() {
  const props = PropertiesService.getScriptProperties();
  const name = String(props.getProperty('BOOTSTRAP_ADMIN_NAME') || '').trim();
  const mobile = normalizeMobile_(props.getProperty('BOOTSTRAP_ADMIN_MOBILE') || '');
  const password = String(props.getProperty('BOOTSTRAP_ADMIN_PASSWORD') || '');

  if (!name || !validMobile_(mobile) || !password || password.length < 8) {
    throw new Error('Set bootstrap admin name, 10-digit mobile and strong password first.');
  }

  const sh = users_();
  const values = sh.getDataRange().getValues();
  const activeAdminExists = values.slice(1).some(function(r) {
    return String(r[3]) === 'ADMIN' && String(r[4]) === 'ACTIVE';
  });
  if (activeAdminExists) throw new Error('An active admin already exists.');

  if (findUserByMobile_(mobile)) throw new Error('Bootstrap mobile already exists.');

  const salt = randomToken_().slice(0,32);
  const id = uuid_();
  const ts = now_();
  sh.appendRow([
    id, name, mobile, 'ADMIN', 'ACTIVE',
    hashPassword_(password, salt), salt, ts, ts
  ]);

  props.deleteProperty('BOOTSTRAP_ADMIN_NAME');
  props.deleteProperty('BOOTSTRAP_ADMIN_MOBILE');
  props.deleteProperty('BOOTSTRAP_ADMIN_PASSWORD');

  return 'First admin created. Bootstrap values removed from Script Properties.';
}
