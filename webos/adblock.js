// Universal Ad Blocker Pro – Original: Gorstak (MIT). Für NicoTV angepasst (läuft beim App-Start im Hintergrund).
(function(){
"use strict";
var LS=window.localStorage,_parse=JSON.parse,blocked=0;
window.__adb={blocked:0};
function on(){try{return _parse(LS.getItem("nct_set")||"{}").ab!==0}catch(e){return true}}
var allow=["twitch.tv","ttvnw.net","jtvnw.net","7tv.io","7tv.app","betterttv.net","googleapis.com","gstatic.com"];
var blockedDomains=["doubleclick.net","googleadservices.com","googlesyndication.com","adservice.google.com","amazon-adsystem.com","taboola.com","outbrain.com","criteo.com","scorecardresearch.com","ads-twitter.com","static.ads-twitter.com","advertising.com","adnxs.com","pubmatic.com","rubiconproject.com","adsafeprotected.com","moatads.com","advertising.yahoo.com","adtech.de","adform.net","serving-sys.com","google-analytics.com","googletagmanager.com","facebook.com/tr","connect.facebook.net","pixel.facebook.com","analytics.twitter.com","pixel.reddit.com","ads.linkedin.com","analytics.tiktok.com","hotjar.com","fullstory.com","segment.io","segment.com","mixpanel.com","amplitude.com"];
var blockedPatterns=["/api/stats/ads","/api/stats/atr","/pagead/","/ptracking","/ad?","/ads?","/advert","/sponsored","/promotion","/tracking","/analytics","/collect?","/beacon","/pixel","/imp?","/impression","/click?","ad_banner","ad_frame","sponsored_content","promo_banner"];
function bad(u){if(!u||!on())return false;u=String(u);
 if(/(^|[\/.])(twitchads\.com|ads\.twitch\.tv|imasdk\.googleapis\.com)([\/:?]|$)/.test(u)){window.__adb.blocked=++blocked;return true}
 var h=(u.match(/^[a-z]+:\/\/([^\/?#]+)/i)||[])[1]||"";
 if(h){for(var i=0;i<allow.length;i++)if(h===allow[i]||h.slice(-allow[i].length-1)==="."+allow[i])return false}
 var hit=blockedDomains.some(function(d){return u.indexOf(d)>-1})||blockedPatterns.some(function(p){return u.indexOf(p)>-1});
 if(hit)window.__adb.blocked=++blocked;return hit}
var _fetch=window.fetch;
if(_fetch)window.fetch=function(a){var u=typeof a==="string"?a:(a&&a.url)||"";if(bad(u))return Promise.reject(new Error("Blocked by Universal Ad Blocker"));return _fetch.apply(this,arguments)};
var _open=XMLHttpRequest.prototype.open;
XMLHttpRequest.prototype.open=function(m,u){var args=[].slice.call(arguments);if(bad(u))args[1]="about:blank";return _open.apply(this,args)};
if(navigator.sendBeacon){var _sb=navigator.sendBeacon;navigator.sendBeacon=function(u){if(bad(u))return true;return _sb.apply(navigator,arguments)}}
function nuke(o,d){if(!o||typeof o!=="object"||d>8)return;["adPlacements","adSlots","playerAds","adBreakHeartbeatParams","ad3Module","adSafetyReason"].forEach(function(k){if(k in o)delete o[k]});
 Object.keys(o).forEach(function(k){if(o[k]&&typeof o[k]==="object")nuke(o[k],d+1)})}
JSON.parse=function(){var out=_parse.apply(this,arguments);try{if(on())nuke(out,0)}catch(e){}return out};
function clean(){if(!on())return;["ins.adsbygoogle",'iframe[id*="google_ads"]','iframe[id*="aswift"]','div[id*="taboola"]','div[id*="outbrain"]',".video-ad-overlay",".preroll-ad",".midroll-ad"].forEach(function(s){[].forEach.call(document.querySelectorAll(s),function(e){e.parentNode&&e.parentNode.removeChild(e)})})}
setInterval(clean,3000);
})();
