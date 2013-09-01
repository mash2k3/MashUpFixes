def resolve_veehd(url):
        name = "veeHD"
        cookie_file = os.path.join(datapath, '%s.cookies' % name)
        user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
        from random import choice
        userName = ['mashup1', 'mashup3', 'mashup4', 'mashup5', 'mashup6', 'mashup7']
        try:
            loginurl = 'http://veehd.com/login'
            ref = 'http://veehd.com/'
            submit = 'Login'        
            terms = 'on'
            remember_me = 'on'
            data = {'ref': ref, 'uname': choice(userName), 'pword': 'xbmcisk00l', 'submit': submit, 'terms': terms, 'remember_me': remember_me}
            html = net(user_agent).http_POST(loginurl, data).content
            net().save_cookies(cookie_file)
            headers = {}
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'}
            net().set_cookies(cookie_file)
            print 'Mash Up VeeHD - Requesting GET URL: %s' % url
            html = net().http_GET(url, headers).content
            fragment = re.findall('playeriframe".+?attr.+?src : "(.+?)"', html)
            frag = 'http://%s%s'%('veehd.com',fragment[1])
            net().set_cookies(cookie_file)
            html = net().http_GET(frag, headers).content
            r = re.search('"video/divx" src="(.+?)"', html)
            if r:
                stream_url = r.group(1)
            if not r:
                message = name + '- 1st attempt at finding the stream_url failed probably an Mp4, finding Mp4'
                addon.log_debug(message)
                a = re.search('"url":"(.+?)"', html)
                if a:
                    r=urllib.unquote(a.group(1))
                    if r:
                        stream_url = r
                    else:
                        raise Exception ('File Not Found or removed')
                if not a:
                    a = re.findall('href="(.+?)">', html)
                    stream_url = a[1]
            return stream_url
        except Exception, e:
            print '**** Mash Up VeeHD Error occured: %s' % e
            addon.show_small_popup('[B][COLOR green]Mash Up: VeeHD Resolver[/COLOR][/B]','Error, Check XBMC.log for Details',
                                   5000, error_logo)
            return
