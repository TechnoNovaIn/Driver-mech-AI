const CFG={SPREADSHEET_ID:'1kQ5k6i7NGFwswfnlquyDiBMtqpr9Pav7Ki4XFWSnJGE',TTL:8*60*60*1000,SHEETS:{USERS:'Users',WORK:'DailyWork',PROBLEMS:'ProblemReports',AUDIT:'AuditLog',ROLES:'Roles',MAHINDRA:'MahindraData'}};

function setupNewBackend(){
  const ss=SpreadsheetApp.openById(CFG.SPREADSHEET_ID);
  ensure_(ss,CFG.SHEETS.USERS,['User ID','Name','Mobile','Role','Status','Password Hash','Password Salt','Created At','Updated At']);
  ensure_(ss,CFG.SHEETS.WORK,['Record ID','Date','Vehicle Number','User ID','User Name','Work Completed','Created At']);
  ensure_(ss,CFG.SHEETS.PROBLEMS,['Report ID','Date','Time','User ID','User Name','Role','Vehicle Number','Problem','Photo Text','Created At']);
  ensure_(ss,CFG.SHEETS.AUDIT,['Timestamp','User ID','Action','Target','Result']);
  ensure_(ss,CFG.SHEETS.ROLES,['Role ID','Role Name','Description','Permissions','Sort Order','Created At','Updated At']);
  seedRoles_(ss);
  ensure_(ss,CFG.SHEETS.MAHINDRA,['ID','Category','Title','Content','Language','Source','Updated At']);
  const ui=SpreadsheetApp.getUi();
  const n=ui.prompt('ADMIN name','Enter admin name:',ui.ButtonSet.OK_CANCEL);
  if(n.getSelectedButton()!=ui.Button.OK) return;
  const m=ui.prompt('ADMIN mobile','Enter 10-digit mobile:',ui.ButtonSet.OK_CANCEL);
  if(m.getSelectedButton()!=ui.Button.OK) return;
  const p=ui.prompt('ADMIN password','Enter password (minimum 8 characters):',ui.ButtonSet.OK_CANCEL);
  if(p.getSelectedButton()!=ui.Button.OK) return;
  const name=n.getResponseText().trim(), mobile=norm(m.getResponseText()), pass=p.getResponseText();
  if(!/^\d{10}$/.test(mobile)||pass.length<8) throw new Error('Invalid admin details.');
  const sh=ss.getSheetByName(CFG.SHEETS.USERS);
  if(findUser(mobile)) throw new Error('This mobile already exists.');
  const salt=Utilities.getUuid().replace(/-/g,'').slice(0,32), id=Utilities.getUuid(), ts=now();
  sh.appendRow([id,name,mobile,'ADMIN','ACTIVE',hash(pass,salt),salt,ts,ts]);
  return 'READY — ADMIN created. Now deploy this script as a Web App.';
}
function ensure_(ss,name,headers){let s=ss.getSheetByName(name);if(!s)s=ss.insertSheet(name);if(s.getLastRow()===0)s.appendRow(headers);}
function ss_(){return SpreadsheetApp.openById(CFG.SPREADSHEET_ID);}
function sh_(n){return ss_().getSheetByName(n);}
function now(){return new Date().toISOString();}
function norm(v){return String(v||'').replace(/\D/g,'');}
function hash(p,s){return hex(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,String(s)+':'+String(p),Utilities.Charset.UTF_8));}
function hex(a){return a.map(b=>{b=b<0?b+256:b;return('0'+b.toString(16)).slice(-2)}).join('');}
function token(){return hex(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,Utilities.getUuid()+Date.now()+Math.random(),Utilities.Charset.UTF_8))+Utilities.getUuid().replace(/-/g,'');}
function json(o){return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);}
function findUser(m){const cleanM=norm(m),v=sh_(CFG.SHEETS.USERS).getDataRange().getValues();for(let i=1;i<v.length;i++)if(norm(v[i][2])===cleanM)return{row:i+1,data:v[i]};return null;}
function findId(id){const cleanId=String(id||'').trim(),v=sh_(CFG.SHEETS.USERS).getDataRange().getValues();for(let i=1;i<v.length;i++)if(String(v[i][0]).trim()===cleanId)return{row:i+1,data:v[i]};return null;}
function pub(u){return{id:String(u.data[0]),name:String(u.data[1]),mobile:norm(u.data[2]),role:String(u.data[3]).trim().toUpperCase(),status:String(u.data[4]).trim().toUpperCase()};}
function saveSession(u){
  const t=token(),exp=Date.now()+CFG.TTL;
  const pr=PropertiesService.getScriptProperties();
  try{
    const all=pr.getProperties(),nowMs=Date.now();
    for(const k in all){
      if(k.indexOf('S_')===0){
        try{const parsed=JSON.parse(all[k]);if(nowMs>=Number(parsed.exp))pr.deleteProperty(k);}catch(e){pr.deleteProperty(k);}
      }
    }
  }catch(e){}
  pr.setProperty('S_'+hex(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,t,Utilities.Charset.UTF_8)),JSON.stringify({id:String(u.data[0]),exp}));
  return{token:t,expiresAt:exp};
}
function session(req){const t=String(req.token||'');if(!t)return{ok:false,code:401,error:'Authentication required.'};const k='S_'+hex(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,t,Utilities.Charset.UTF_8)),pr=PropertiesService.getScriptProperties(),raw=pr.getProperty(k);if(!raw)return{ok:false,code:401,error:'Session expired or invalid.'};let s;try{s=JSON.parse(raw)}catch(e){pr.deleteProperty(k);return{ok:false,code:401,error:'Invalid session.'}}if(Date.now()>=Number(s.exp)){pr.deleteProperty(k);return{ok:false,code:401,error:'Session expired.'}}const u=findId(s.id);if(!u||String(u.data[4]).trim().toUpperCase()!=='ACTIVE'){pr.deleteProperty(k);return{ok:false,code:403,error:'Account disabled.'}}return{ok:true,user:u};}
function admin(u){return String(u.data[3]).trim().toUpperCase()==='ADMIN';}
function audit(u,a,t,r){sh_(CFG.SHEETS.AUDIT).appendRow([now(),String(u.data[0]),a,t,r]);}

function doGet(e){return json_({ok:true,service:'MAHINDRA BSVI secure backend v2',status:'online'});}
function doPost(e){
 try{
  const q=JSON.parse((e&&e.postData&&e.postData.contents)||'{}'),a=String(q.action||'');
  if(a==='login')return json_(login(q));
  if(a==='logout'){if(q.token)PropertiesService.getScriptProperties().deleteProperty('S_'+hex(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,String(q.token),Utilities.Charset.UTF_8)));return json_({ok:true,code:200});}
  const s=session(q);if(!s.ok)return json_(s);const u=s.user;
  if(a==='me')return json_({ok:true,code:200,user:pub(u)});
  if(a==='save_work')return json_(saveWork(q,u));
  if(a==='list_work'||a==='sync')return json_(listWork(q,u));
  if(a==='save_problem')return json_(saveProblem(q,u));
  if(a==='list_problems')return json_(listProblems(q,u));
  if(a==='list_users')return json_(listUsers(q,u));
  if(a==='add_user')return json_(addUser(q,u));
  if(a==='update_user')return json_(updateUser(q,u));
  if(a==='set_user_status')return json_(setStatus(q,u));
  if(a==='set_user_role')return json_(setRole(q,u));
  if(a==='set_user_password')return json_(setPassword(q,u));
  if(a==='list_roles')return json_(listRoles(q,u));
  if(a==='create_role')return json_(createRole(q,u));
  if(a==='update_role')return json_(updateRole(q,u));
  if(a==='delete_role')return json_(deleteRole(q,u));
  if(a==='save_role_permissions')return json_(saveRolePermissions(q,u));
  if(a==='reorder_roles')return json_(reorderRoles(q,u));
  if(a==='export_work')return json_(exportWork(q,u));
  return json_({ok:false,code:400,error:'Unknown action.'});
 }catch(e){return json_({ok:false,code:500,error:String(e.message||e)});}
}
function login(q){
 const m=norm(q.username),p=String(q.password||'');if(!/^\d{10}$/.test(m)||!p)return{ok:false,code:401,error:'Mobile number or password is incorrect.'};
 const u=findUser(m);if(!u||String(u.data[4]).trim().toUpperCase()!=='ACTIVE'||hash(p,String(u.data[6]))!==String(u.data[5])){if(u)audit(u,'LOGIN','AUTH','FAILED');return{ok:false,code:401,error:'Mobile number or password is incorrect.'}};
 const s=saveSession(u);audit(u,'LOGIN','AUTH','SUCCESS');return{ok:true,code:200,token:s.token,expiresAt:s.expiresAt,user:pub(u)};
}
function saveWork(q,u){if(!q.date||!q.workCompleted)return{ok:false,code:400,error:'Date and work details are required.'};const id=Utilities.getUuid();const vehicle=String(q.vehicleNumber||'-').toUpperCase();sh_(CFG.SHEETS.WORK).appendRow([id,String(q.date),vehicle,u.data[0],u.data[1],String(q.workCompleted),now()]);audit(u,'SAVE_WORK',id,'SUCCESS');return{ok:true,code:200,recordId:id};}
function listWork(q,u){const v=sh_(CFG.SHEETS.WORK).getDataRange().getValues(),out=[],isA=admin(u);for(let i=1;i<v.length;i++){const r=v[i];if(!r[0]||(!isA&&String(r[3])!==String(u.data[0])))continue;out.push({id:String(r[0]),date:String(r[1]),vehicleNumber:String(r[2]),userId:String(r[3]),userName:String(r[4]),workCompleted:String(r[5]),createdAt:String(r[6])});}out.reverse();return{ok:true,code:200,records:out};}
function saveProblem(q,u){if(!q.problem&&!q.photoText)return{ok:false,code:400,error:'Problem details are required.'};const d=new Date(),id=Utilities.getUuid(),date=Utilities.formatDate(d,Session.getScriptTimeZone(),'yyyy-MM-dd'),time=Utilities.formatDate(d,Session.getScriptTimeZone(),'HH:mm:ss');sh_(CFG.SHEETS.PROBLEMS).appendRow([id,date,time,u.data[0],u.data[1],u.data[3],String(q.vehicleNumber||'').toUpperCase(),String(q.problem||''),String(q.photoText||''),now()]);audit(u,'SAVE_PROBLEM',id,'SUCCESS');return{ok:true,code:200,reportId:id};}
function listProblems(q,u){const v=sh_(CFG.SHEETS.PROBLEMS).getDataRange().getValues(),out=[],isA=admin(u);for(let i=1;i<v.length;i++){const r=v[i];if(!r[0]||(!isA&&String(r[3])!==String(u.data[0])))continue;out.push({id:String(r[0]),date:String(r[1]),time:String(r[2]),userId:String(r[3]),userName:String(r[4]),role:String(r[5]),vehicleNumber:String(r[6]),problem:String(r[7]),photoText:String(r[8]),createdAt:String(r[9])});}out.reverse();return{ok:true,code:200,records:out};}
function listUsers(q,u){if(!admin(u))return{ok:false,code:403,error:'Admin permission required.'};const v=sh_(CFG.SHEETS.USERS).getDataRange().getValues(),out=[];for(let i=1;i<v.length;i++)if(v[i][0])out.push(pub({data:v[i]}));return{ok:true,code:200,users:out};}
function addUser(q,u){if(!hasPerm(u,'manage_employees')&&!admin(u))return{ok:false,code:403,error:'Admin or employee management permission required.'};const n=String(q.name||'').trim(),m=norm(q.mobile),r=String(q.role||'EMPLOYEE').toUpperCase(),p=String(q.password||''),st=String(q.status||'ACTIVE').toUpperCase()==='DISABLED'?'DISABLED':'ACTIVE';if(!n||!/^\d{10}$/.test(m))return{ok:false,code:400,error:'Enter a name and a valid 10-digit mobile number.'};if(findUser(m))return{ok:false,code:409,error:'A user with this mobile number already exists.'};const exRoles=getRolesList().map(x=>x.name);exRoles.push('ADMIN','MECHANIC','EMPLOYEE','DRIVER','USER');if(!exRoles.includes(r))return{ok:false,code:400,error:'Invalid role: '+r};if(r==='ADMIN'&&!admin(u))return{ok:false,code:403,error:'Only an administrator can create an ADMIN account.'};const salt=token().slice(0,32),pass=p||m.slice(-4),id=Utilities.getUuid(),ts=now(),sh=sh_(CFG.SHEETS.USERS);sh.appendRow([id,n,m,r,st,hash(pass,salt),salt,ts,ts]);try{sh.getRange(sh.getLastRow(),3).setNumberFormat('@');}catch(e){}audit(u,'ADD_USER',id,'SUCCESS');return{ok:true,code:200,user:{id,name:n,mobile:m,role:r,status:st}};}
function setStatus(q,u){if(!admin(u))return{ok:false,code:403,error:'Admin permission required.'};const f=findId(q.userId),st=String(q.status||'').toUpperCase();if(!f||!['ACTIVE','DISABLED'].includes(st))return{ok:false,code:400,error:'Invalid request.'};if(String(f.data[0])===String(u.data[0])&&st!=='ACTIVE')return{ok:false,code:400,error:'Cannot disable current admin.'};sh_(CFG.SHEETS.USERS).getRange(f.row,5).setValue(st);sh_(CFG.SHEETS.USERS).getRange(f.row,9).setValue(now());audit(u,'SET_USER_STATUS',q.userId,st);return{ok:true,code:200};}
function setRole(q,u){if(!admin(u))return{ok:false,code:403,error:'Admin permission required.'};const f=findId(q.userId),r=String(q.role||'').toUpperCase();if(!f||!['ADMIN','DRIVER','MECHANIC','EMPLOYEE','USER'].includes(r))return{ok:false,code:400,error:'Invalid request.'};if(String(f.data[0])===String(u.data[0])&&r!=='ADMIN')return{ok:false,code:400,error:'Cannot remove your admin role.'};sh_(CFG.SHEETS.USERS).getRange(f.row,4).setValue(r);sh_(CFG.SHEETS.USERS).getRange(f.row,9).setValue(now());audit(u,'SET_USER_ROLE',q.userId,r);return{ok:true,code:200};}
function setPassword(q,u){if(!admin(u))return{ok:false,code:403,error:'Admin permission required.'};const f=findId(q.userId),p=String(q.password||'');if(!f||p.length<8)return{ok:false,code:400,error:'User not found or password too short.'};const s=token().slice(0,32);sh_(CFG.SHEETS.USERS).getRange(f.row,6).setValue(hash(p,s));sh_(CFG.SHEETS.USERS).getRange(f.row,7).setValue(s);sh_(CFG.SHEETS.USERS).getRange(f.row,9).setValue(now());audit(u,'SET_USER_PASSWORD',q.userId,'SUCCESS');return{ok:true,code:200};}
function exportWork(q,u){if(!admin(u))return{ok:false,code:403,error:'Admin permission required.'};const r=listWork(q,u),lines=['Date,Vehicle Number,User ID,User Name,Work Completed,Created At'];r.records.forEach(x=>lines.push([x.date,x.vehicleNumber,x.userId,x.userName,x.workCompleted,x.createdAt].map(v=>'"'+String(v).replace(/"/g,'""')+'"').join(',')));return{ok:true,code:200,csv:lines.join('\\r\\n')};}

function seedRoles_(ss){
  let sh=ss.getSheetByName(CFG.SHEETS.ROLES);
  if(!sh){sh=ss.insertSheet(CFG.SHEETS.ROLES);sh.appendRow(['Role ID','Role Name','Description','Permissions','Sort Order','Created At','Updated At']);}
  if(sh.getLastRow()>1)return;
  const ts=now();
  const defs=[
    ['role_admin','ADMIN','System Administrator with full access to all features, fleet settings, and user management.',JSON.stringify(['manage_employees','create_edit_roles','assign_roles','manage_permissions','view_admin_dashboard','view_employee_dashboard','submit_work_updates','view_vehicle_info']),1,ts,ts],
    ['role_mechanic','MECHANIC','Service technician handling vehicle repairs, work logs, parts replacement, and diagnostics.',JSON.stringify(['view_employee_dashboard','submit_work_updates','view_vehicle_info']),2,ts,ts],
    ['role_employee','EMPLOYEE','Fleet operations employee submitting daily task updates and attendance.',JSON.stringify(['view_employee_dashboard','submit_work_updates']),3,ts,ts],
    ['role_driver','DRIVER','Commercial vehicle driver reporting problems, viewing guides, and requesting assistance.',JSON.stringify(['view_vehicle_info']),4,ts,ts]
  ];
  defs.forEach(r=>sh.appendRow(r));
}
function rolesSh_(){let sh=sh_(CFG.SHEETS.ROLES);if(!sh){seedRoles_(ss_());sh=sh_(CFG.SHEETS.ROLES);}return sh;}
function getRolesList(){
  const sh=rolesSh_(),rows=sh.getDataRange().getValues(),userCounts={};
  try{const uRows=sh_(CFG.SHEETS.USERS).getDataRange().getValues();for(let j=1;j<uRows.length;j++){const r=String(uRows[j][3]).toUpperCase();userCounts[r]=(userCounts[r]||0)+1;}}catch(e){}
  const list=[];
  for(let i=1;i<rows.length;i++){
    const r=rows[i];if(!r[0])continue;
    let perms=[];try{perms=JSON.parse(r[3]||'[]')}catch(e){perms=[]}
    const nm=String(r[1]).toUpperCase();
    list.push({id:String(r[0]),name:nm,description:String(r[2]||''),permissions:perms,sortOrder:Number(r[4]||i),userCount:userCounts[nm]||0,isSystemRole:['ADMIN','MECHANIC','EMPLOYEE','DRIVER'].includes(nm),createdAt:String(r[5]||''),updatedAt:String(r[6]||'')});
  }
  list.sort((a,b)=>(a.sortOrder||0)-(b.sortOrder||0));
  return list;
}
function getRolePerms(roleName){
  try{
    const rows=rolesSh_().getDataRange().getValues(),norm=String(roleName||'').toUpperCase();
    for(let i=1;i<rows.length;i++)if(String(rows[i][1]).toUpperCase()===norm){try{return JSON.parse(rows[i][3]||'[]')}catch(e){return[]}}
  }catch(e){}
  if(roleName==='ADMIN')return ['manage_employees','create_edit_roles','assign_roles','manage_permissions','view_admin_dashboard','view_employee_dashboard','submit_work_updates','view_vehicle_info'];
  if(roleName==='MECHANIC')return ['view_employee_dashboard','submit_work_updates','view_vehicle_info'];
  if(roleName==='EMPLOYEE')return ['view_employee_dashboard','submit_work_updates'];
  if(roleName==='DRIVER')return ['view_vehicle_info'];
  return [];
}
function hasPerm(u,p){if(!u)return false;if(admin(u))return true;return getRolePerms(String(u.data[3])).includes(p);}
function listRoles(q,u){if(!hasPerm(u,'manage_permissions')&&!hasPerm(u,'manage_employees'))return{ok:false,code:403,error:'Permission denied.'};return{ok:true,code:200,roles:getRolesList()};}
function createRole(q,u){
  if(!admin(u))return{ok:false,code:403,error:'Admin permission required.'};
  const nm=String(q.name||'').trim().toUpperCase(),desc=String(q.description||'').trim(),perms=Array.isArray(q.permissions)?q.permissions:[];
  if(!nm||nm.length<2||!/^[A-Z0-9_\-\s]+$/.test(nm))return{ok:false,code:400,error:'Valid role name required.'};
  const existing=getRolesList();if(existing.some(r=>r.name===nm))return{ok:false,code:409,error:'Role already exists.'};
  const id='role_'+Utilities.getUuid().slice(0,8),order=existing.reduce((m,r)=>Math.max(m,r.sortOrder||0),0)+1,ts=now();
  rolesSh_().appendRow([id,nm,desc,JSON.stringify(perms),order,ts,ts]);
  audit(u,'CREATE_ROLE',id,nm);
  return{ok:true,code:200,role:{id,name:nm,description:desc,permissions:perms,sortOrder:order,userCount:0}};
}
function updateRole(q,u){
  if(!admin(u))return{ok:false,code:403,error:'Admin permission required.'};
  const id=String(q.roleId||''),nm=String(q.name||'').trim().toUpperCase(),desc=String(q.description||'').trim(),perms=Array.isArray(q.permissions)?q.permissions:null;
  if(!id||!nm||nm.length<2)return{ok:false,code:400,error:'Valid role details required.'};
  const sh=rolesSh_(),rows=sh.getDataRange().getValues();let tRow=-1,oldNm='';
  for(let i=1;i<rows.length;i++)if(String(rows[i][0])===id){tRow=i+1;oldNm=String(rows[i][1]).toUpperCase();break;}
  if(tRow===-1)return{ok:false,code:404,error:'Role not found.'};
  if(oldNm==='ADMIN'&&nm!=='ADMIN')return{ok:false,code:400,error:'Cannot rename ADMIN role.'};
  if(nm!==oldNm&&rows.some((r,idx)=>idx>0&&idx+1!==tRow&&String(r[1]).toUpperCase()===nm))return{ok:false,code:409,error:'Role name taken.'};
  const ts=now();sh.getRange(tRow,2).setValue(nm);sh.getRange(tRow,3).setValue(desc);
  if(perms!==null){
    if(nm==='ADMIN'){const req=['manage_employees','create_edit_roles','assign_roles','manage_permissions','view_admin_dashboard'];req.forEach(p=>{if(!perms.includes(p))perms.push(p)});}
    sh.getRange(tRow,4).setValue(JSON.stringify(perms));
  }
  sh.getRange(tRow,7).setValue(ts);
  if(nm!==oldNm){
    const uSh=sh_(CFG.SHEETS.USERS),uRows=uSh.getDataRange().getValues();
    for(let j=1;j<uRows.length;j++)if(String(uRows[j][3]).toUpperCase()===oldNm){uSh.getRange(j+1,4).setValue(nm);uSh.getRange(j+1,9).setValue(ts);}
  }
  audit(u,'UPDATE_ROLE',id,nm);return{ok:true,code:200};
}
function saveRolePermissions(q,u){
  if(!admin(u))return{ok:false,code:403,error:'Admin permission required.'};
  const id=String(q.roleId||''),perms=Array.isArray(q.permissions)?q.permissions:[];
  const sh=rolesSh_(),rows=sh.getDataRange().getValues();let tRow=-1,nm='';
  for(let i=1;i<rows.length;i++)if(String(rows[i][0])===id){tRow=i+1;nm=String(rows[i][1]).toUpperCase();break;}
  if(tRow===-1)return{ok:false,code:404,error:'Role not found.'};
  if(nm==='ADMIN'){const req=['manage_employees','create_edit_roles','assign_roles','manage_permissions','view_admin_dashboard'];req.forEach(p=>{if(!perms.includes(p))perms.push(p)});}
  sh.getRange(tRow,4).setValue(JSON.stringify(perms));sh.getRange(tRow,7).setValue(now());
  audit(u,'SAVE_ROLE_PERMS',id,JSON.stringify(perms));return{ok:true,code:200};
}
function reorderRoles(q,u){
  if(!admin(u))return{ok:false,code:403,error:'Admin permission required.'};
  const ids=q.orderedIds;if(!Array.isArray(ids)||!ids.length)return{ok:false,code:400,error:'orderedIds required.'};
  const sh=rolesSh_(),rows=sh.getDataRange().getValues(),map={};
  for(let i=1;i<rows.length;i++)if(rows[i][0])map[String(rows[i][0])]=i+1;
  ids.forEach((id,idx)=>{if(map[String(id)])sh.getRange(map[String(id)],5).setValue(idx+1);});
  return{ok:true,code:200};
}
function deleteRole(q,u){
  if(!admin(u))return{ok:false,code:403,error:'Admin permission required.'};
  const id=String(q.roleId||''),sh=rolesSh_(),rows=sh.getDataRange().getValues();let tRow=-1,nm='';
  for(let i=1;i<rows.length;i++)if(String(rows[i][0])===id){tRow=i+1;nm=String(rows[i][1]).toUpperCase();break;}
  if(tRow===-1)return{ok:false,code:404,error:'Role not found.'};
  if(['ADMIN','DRIVER','MECHANIC','EMPLOYEE'].includes(nm))return{ok:false,code:400,error:'Cannot delete system role.'};
  const uRows=sh_(CFG.SHEETS.USERS).getDataRange().getValues();
  for(let j=1;j<uRows.length;j++)if(String(uRows[j][3]).toUpperCase()===nm)return{ok:false,code:400,error:'Employees are assigned to this role.'};
  sh.deleteRow(tRow);audit(u,'DELETE_ROLE',id,nm);return{ok:true,code:200};
}
function updateUser(q,u){
  if(!hasPerm(u,'manage_employees'))return{ok:false,code:403,error:'Permission denied.'};
  const id=String(q.userId||''),n=String(q.name||'').trim(),m=norm(q.mobile),r=String(q.role||'').toUpperCase(),st=String(q.status||'ACTIVE').toUpperCase();
  if(!id||!n||!/^\d{10}$/.test(m))return{ok:false,code:400,error:'Valid name and 10-digit mobile required.'};
  const f=findId(id);if(!f)return{ok:false,code:404,error:'User not found.'};
  const exRoles=getRolesList().map(x=>x.name);exRoles.push('ADMIN','MECHANIC','EMPLOYEE','DRIVER','USER');
  if(!exRoles.includes(r))return{ok:false,code:400,error:'Invalid role: '+r};
  if(r==='ADMIN'&&!admin(u))return{ok:false,code:403,error:'Only admin can assign ADMIN role.'};
  if(m!==String(f.data[2])){const ex=findUser(m);if(ex&&String(ex.data[0])!==id)return{ok:false,code:409,error:'Mobile number taken.'};}
  const curRole=String(f.data[3]).toUpperCase();
  if(curRole==='ADMIN'&&(r!=='ADMIN'||st!=='ACTIVE')){
    const all=sh_(CFG.SHEETS.USERS).getDataRange().getValues(),admins=all.slice(1).filter(x=>String(x[3]).toUpperCase()==='ADMIN'&&String(x[4]).toUpperCase()==='ACTIVE'&&String(x[0])!==id);
    if(admins.length===0)return{ok:false,code:400,error:'Cannot demote or deactivate the last active administrator.'};
  }
  if(String(f.data[0])===String(u.data[0])&&r!=='ADMIN')return{ok:false,code:400,error:'Cannot remove your own admin role.'};
  const sh=sh_(CFG.SHEETS.USERS),ts=now();
  sh.getRange(f.row,2).setValue(n);sh.getRange(f.row,3).setValue(m);sh.getRange(f.row,4).setValue(r);sh.getRange(f.row,5).setValue(st);sh.getRange(f.row,9).setValue(ts);
  audit(u,'UPDATE_USER',id,'SUCCESS');
  return{ok:true,code:200,user:{id,name:n,mobile:m,role:r,status:st}};
}
