import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
google_ip = socket.gethostbyname("google.com")
sock.connect((google_ip, 80))

sock.send("GET / HTTP/1.1\n".encode())
sock.send("\n".encode())

buffer = sock.recv(4096)
buffer = buffer.decode().replace("\r\n", "\n")
sock.close()

print(buffer)

'''
HTTP/1.1 200 OK
Date: Tue, 21 May 2019 21:04:55 GMT
Expires: -1
Cache-Control: private, max-age=0
Content-Type: text/html; charset=ISO-8859-1
P3P: CP="This is not a P3P policy! See g.co/p3phelp for more info."
Server: gws
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Set-Cookie: 1P_JAR=2019-05-21-21; expires=Thu, 20-Jun-2019 21:04:55 GMT; path=/; domain=.google.com
Set-Cookie: NID=184=usYdW37LNlxJnvEnFiBY5-J6P29VVy0oSQQMWV7wd0CAKYtJeo_zlOu5VRSHiOXg-esRaMpMSNhf8P9mQtbWmQllpZwXGIOw8G2r0YnkZwSCbIV7TJdxCBH2pKG2V9g4XIWphNVcK97Y_2jiC_JRan1n8eGR5ztfL_-H4F3V-yI; expires=Wed, 20-Nov-2019
21:04:55 GMT; path=/; domain=.google.com; HttpOnly
Accept-Ranges: none
Vary: Accept-Encoding
Transfer-Encoding: chunked

52e0
<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="ko"><head><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><meta content="/images/branding/googleg/1x/googleg_standard_color_128dp.png" itemprop="image"><title>Google</title><script nonce="7kOv2/KULOJDFBWsfQmxmg==">(function(){window.google={kEI:'92fkXI_vK-SSr7wPlaW5uA4',kEXPI:'0,1353747,57,1958,2422,698,527,731,223,528,1047,1258,1894,57,321,206,1017,166,439,129,309,2332598,107,329376,1294,12383,4855,32692,15247,867,7505,4952,4987,9044,2196,369,3314,5505,2436,5373,575,835,284,2,578,728,2068,364,1361,4323,4967,774,2247,2646,2101,1151,2,1965,2595,3601,669,1050,1808,1397,81,7,491,620,29,1395,8909,1288,2,620,3387,796,1222,36,920,746,7,120,1217,1364,346,1,1264,2736,3061,2,631,2562,2,4,2,670,44,4658,124,2608,632,803,1425,656,18,320,1592,389,228,2,1159,404,373,1,2,369,1014,302,78,625,756,98,36,2,354,29,400,992,1107,10,168,8,109,187,831,235,810,450,174,885,82,48,459,94,11,14,11,2497,602,381,25,177,323,5,1252,67,90,141,243,299,92,1,231,193,531,268,103,112,161,25,62,165,57,22,16,108,709,912,587,70,71,24,237,1,100,432,189,818,109,151,1189,2,7,7,1153,5,337,554,606,453,185,107,20,13,186,5,348,189,1,206,117,9,153,30,41,6,322,227,366,716,643,276,60,1,158,153,638,636,247,1,749,57,12,340,1186,1858,5931200,13,1861,1012,5997581,43,2799830,4,1572,549,333,444,1,2,80,1,900,583,9,304,1,8,1,2,2132,1,1,1,1,1,414,1,748,141,59,726,3,7,563,1,2075,72,44,2,4,31,1,1,8,10,1,5,5',authuser:0,kscs:'c9c918f0_92fkXI_vK-SSr7wPlaW5uA4',kGL:'KR'};google.sn='webhp';google.kHL='ko';})();(function(){google.lc=[];google.li=0;google.getEI=function(a){for(var b;a&&(!a.getAttribute||!(b=a.getAttribute("eid")));)a=a.parentNode;return b||google.kEI};google.getLEI=function(a){for(var b=null;a&&(!a.getAttribute||!(b=a.getAttribute("leid")));)a=a.parentNode;return b};google.https=function(){return"https:"==window.location.protocol};google.ml=function(){return null};google.time=function(){return(new Date).getTime()};google.log=function(a,b,e,c,g){if(a=google.logUrl(a,b,e,c,g)){b=new Image;var d=google.lc,f=google.li;d[f]=b;b.onerror=b.onload=b.onabort=function(){delete d[f]};google.vel&&google.vel.lu&&google.vel.lu(a);b.src=a;google.li=f+1}};google.logUrl=function(a,b,e,c,g){var d="",f=google.ls||"";e||-1!=b.search("&ei=")||(d="&ei="+google.getEI(c),-1==b.search("&lei=")&&(c=google.getLEI(c))&&(d+="&lei="+c));c="";!e&&google.cshid&&-1==b.search("&cshid=")&&"slh"!=a&&(c="&cshid="+google.cshid);a=e||"/"+(g||"gen_204")+"?atyp=i&ct="+a+"&cad="+b+d+f+"&zx="+google.time()+c;/^http:/i.test(a)&&google.https()&&(google.ml(Error("a"),!1,{src:a,glmm:1}),a="");return a};}).call(this);(function(){google.y={};google.x=function(a,b){if(a)var c=a.id;else{do c=Math.random();while(google.y[c])}google.y[c]=[a,b];return!1};google.lm=[];google.plm=function(a){google.lm.push.apply(google.lm,a)};google.lq=[];google.load=function(a,b,c){google.lq.push([[a],b,c])};google.loadAll=function(a,b){google.lq.push([a,b])};}).call(this);google.f={};var a=window.location,b=a.href.indexOf("#");if(0<=b){var c=a.href.substring(b+1);/(^|&)q=/.test(c)&&-1==c.indexOf("#")&&a.replace("/search?"+c.replace(/(^|&)fp=[^&]*/g,"")+"&cad=h")};</script><style>#gb{font:13px/27px Arial,sans-serif;height:30px}#gbz,#gbg{position:absolute;white-space:nowrap;top:0;height:30px;z-index:1000}#gbz{left:0;padding-left:4px}
'''