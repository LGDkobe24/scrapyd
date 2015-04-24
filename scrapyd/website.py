# -*- coding: gb2312 -*-
from datetime import datetime

import socket

from twisted.web import resource, static
from twisted.application.service import IServiceCollection

from scrapy.utils.misc import load_object

from .interfaces import IPoller, IEggStorage, ISpiderScheduler

from urlparse import urlparse

class Root(resource.Resource):

    def __init__(self, config, app):
        resource.Resource.__init__(self)
        self.debug = config.getboolean('debug', False)
        self.runner = config.get('runner')
        logsdir = config.get('logs_dir')
        itemsdir = config.get('items_dir')
        local_items = itemsdir and (urlparse(itemsdir).scheme.lower() in ['', 'file'])
        self.app = app
        self.nodename = config.get('node_name', socket.gethostname())
        self.putChild('', Home(self, local_items))
        if logsdir:
            self.putChild('logs', static.File(logsdir, 'text/plain'))
        if local_items:
            self.putChild('items', static.File(itemsdir, 'text/plain'))
        self.putChild('jobs', Jobs(self, local_items))
        services = config.items('services', ())
        # print services
        for servName, servClsName in services:
          servCls = load_object(servClsName)
          self.putChild(servName, servCls(self))
        self.update_projects()

    def update_projects(self):
        self.poller.update_projects()
        self.scheduler.update_projects()

    @property
    def launcher(self):
        app = IServiceCollection(self.app, self.app)
        return app.getServiceNamed('launcher')

    @property
    def scheduler(self):
        return self.app.getComponent(ISpiderScheduler)

    @property
    def eggstorage(self):
        return self.app.getComponent(IEggStorage)

    @property
    def poller(self):
        return self.app.getComponent(IPoller)


class Home(resource.Resource):

    def __init__(self, root, local_items):
        resource.Resource.__init__(self)
        self.root = root
        self.local_items = local_items

    def render_GET(self, txrequest):
        vars = {
            'projects': ', '.join(self.root.scheduler.list_projects()),
        }
        s = """
<html>
<head><title>ScrapyÅÀ³æ·þÎñÆ÷</title></head>
<body>
<h1>ScrapyÅÀ³æ·þÎñÆ÷</h1>
<p>¿ÉÓÃµÄÏîÄ¿: <b>%(projects)s</b></p>
<ul>
<li><a href="/jobs">×¥È¡¹¤×÷</a></li>
""" % vars
        if self.local_items:
            s += '<li><a href="/items/">×¥È¡ÎïÆ·</a></li>'
        s += """
<li><a href="/logs/">×¥È¡ÈÕÖ¾</a></li>

</ul>

<h4>Êý¾Ý×¥È¡¹æ»®APIÑùÀý</h4>

<p>ÐèÒªÊ¹ÓÃ<a href="http://curl.haxx.se/">curl</a>:</p>
<p><code>curl http://localhost:6800/schedule.json -d project=myproject -d spider=somespider -d setting=DOWNLOAD_DELAY=2 -d arg1=val1</code></p>

<p><code> curl http://localhost:6800/cancel.json -d project=myproject -d job=6487ec79947edab326d6db28a2d86511e8247444 </code></p>

<p><code> curl http://localhost:6800/listprojects.json </code></p>
<p><code>  curl http://localhost:6800/listversions.json?project=myproject </code></p>
<p><code> curl http://localhost:6800/spiderid.json?project=myproject </code></p>
<p><code> curl http://localhost:6800/listspiders.json?project=myproject </code></p><p><code>  curl http://localhost:6800/listjobs.json?project=myproject </code></p>

<p><code> curl http://localhost:6800/delproject.json -d project=myproject </code></p>


<p><code> curl http://localhost:6800/delversion.json -d project=myproject -d version=r99 </code></p>

<p>¸ü¶àµÄAPI£¬¿´¹Ù·½ÎÄµµ°É <a href="http://scrapyd.readthedocs.org/en/latest/">Scrapyd documentation</a></p>


<p> [deploy:scrapyd2] <p>
  <p>  url = http://scrapyd.mydomain.com/api/scrapyd/ <p>
  <p>  username = john <p>
  <p>  password = secret <p>
  
<p>ÉÏ´«ÅÀ³æµÄÃüÁî  scrapyd-deploy -l <p>

<p>´î½¨£ºÉòÖ®Èñ<p>
</body>
</html>
""" % vars
        return s

class Jobs(resource.Resource):

    def __init__(self, root, local_items):
        resource.Resource.__init__(self)
        self.root = root
        self.local_items = local_items

    def render(self, txrequest):
        cols = 6
        s = "<html><head><title>Scrapy·þÎñÆ÷</title></head>"
        s += "<body>"
        s += "<h1>×¥È¡¹¤×÷</h1>"
        s += "<p><a href='..'>·µ»Ø</a></p>"
        s += "<table border='1'>"
        s += "<tr><th>ÏîÄ¿</th><th>ÅÀ³æ</th><th>¹¤×÷</th><th>PID</th><th>ÔËÐÐÊ±¼ä</th><th>ÈÕÖ¾</th>"
        if self.local_items:
            s += "<th>ÏîÄ¿</th>"
            cols = 7
        s += "</tr>"
        s += "<tr><th colspan='%s' style='background-color: #ddd'>×¼±¸ÔËÐÐ</th></tr>" % cols
        for project, queue in self.root.poller.queues.items():
            for m in queue.list():
                s += "<tr>"
                s += "<td>%s</td>" % project
                s += "<td>%s</td>" % str(m['name'])
                s += "<td>%s</td>" % str(m['_job'])
                s += "</tr>"
        s += "<tr><th colspan='%s' style='background-color: #ddd'>ÕýÔÚÔËÐÐ</th></tr>" % cols
        for p in self.root.launcher.processes.values():
            s += "<tr>"
            for a in ['project', 'spider', 'job', 'pid']:
                s += "<td>%s</td>" % getattr(p, a)
            s += "<td>%s</td>" % (datetime.now() - p.start_time)
            s += "<td><a href='/logs/%s/%s/%s.log'>Log</a></td>" % (p.project, p.spider, p.job)
            if self.local_items:
                s += "<td><a href='/items/%s/%s/%s.jl'>Items</a></td>" % (p.project, p.spider, p.job)
            s += "</tr>"
        s += "<tr><th colspan='%s' style='background-color: #ddd'>Íê³ÉÔËÐÐ</th></tr>" % cols
        for p in self.root.launcher.finished:
            s += "<tr>"
            for a in ['project', 'spider', 'job']:
                s += "<td>%s</td>" % getattr(p, a)
            s += "<td></td>"
            s += "<td>%s</td>" % (p.end_time - p.start_time)
            s += "<td><a href='/logs/%s/%s/%s.log'>×¥È¡ÈÕÖ¾</a></td>" % (p.project, p.spider, p.job)
            if self.local_items:
                s += "<td><a href='/items/%s/%s/%s.jl'>×¥È¡ÎïÆ·</a></td>" % (p.project, p.spider, p.job)
            s += "</tr>"
        s += "</table>"
        s += "</body>"
        s += "</html>"
        return s
