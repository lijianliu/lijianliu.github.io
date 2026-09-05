(function(root){
const fresh=()=>({level:1,hp:100,ammo:5,kills:0,totalKills:0,x:0,z:3,enemies:[],spawned:0,target:4,started:false,cleared:false});
function valid(w){return w&&Number.isInteger(w.level)&&w.level>=1&&w.level<=999&&Number.isFinite(w.hp)&&w.hp>=0&&w.hp<=100&&Number.isInteger(w.ammo)&&w.ammo>=0&&w.ammo<=30&&Number.isFinite(w.x)&&Math.abs(w.x)<=12&&Number.isFinite(w.z)&&Math.abs(w.z)<=12&&Array.isArray(w.enemies)&&w.enemies.length<=20&&w.enemies.every(e=>Number.isFinite(e.x)&&Number.isFinite(e.z)&&Number.isFinite(e.hp)&&e.hp>0)&&Number.isFinite(w.kills)&&Number.isFinite(w.totalKills)&&Number.isFinite(w.spawned)&&Number.isFinite(w.target);}
function reward(w){w.hp=Math.min(100,w.hp+35);w.ammo=Math.min(30,w.ammo+8);}
function shoot(w){if(w.hp<=0||w.ammo<=0||w.cleared)return false;w.ammo--;return true;}
function hurt(w){w.hp=Math.max(0,w.hp-9);return w.hp===0;}
function hit(w,id){const e=w.enemies.find(e=>e.id===id);if(!e)return false;e.hp--;if(e.hp<=0){w.enemies=w.enemies.filter(x=>x.id!==id);w.kills++;w.totalKills++;if(w.kills>=w.target)w.cleared=true;return true;}return false;}
function next(w){w.level++;w.kills=0;w.target=Math.min(14,3+w.level);w.spawned=0;w.enemies=[];w.cleared=false;w.x=0;w.z=3;w.hp=Math.min(100,w.hp+15);}
root.Combat={fresh,valid,reward,shoot,hurt,hit,next};
})(typeof window!=='undefined'?window:globalThis);
