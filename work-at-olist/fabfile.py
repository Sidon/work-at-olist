'''
Script Fabric for contiuous integration (library and command-line tool for 
streamlining the use of SSH for application deployment or systems administration tasks. 
fabric (python2) ou fabric3 (python 3): 
pip install fabric3
'''

import os
from termcolor import colored
import yaml
from fabric.api import run, put, env, cd, prefix, sudo, execute
from fabric.contrib.project import rsync_project
from paramiko import SSHConfig
from os.path import expanduser
from fabric.utils import abort
import pprint
pp = pprint.PrettyPrinter(indent=2)


env.use_ssh_config = True


# local - run a shell command on the local machine
# run - run a sehll command on the remote server
# put - copy to remote server via ssh (scp)
# env - environment conf.

__author__ = "Sidon Duarte, Yan Duarte"
__copyright__ = "Copyright 2017, olist project"
__credits__ = ["Sidon Duarte"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Sidon Duarte"
__email__ = "sidoncd@gmail.com"
__status__ = "Production"


# read config yaml file
with open('fab.yaml', 'r') as f:
    cfg  = yaml.load(f)

# Load .ssh configuration from current local user
ssh_config = SSHConfig()
file_ssh = os.path.expanduser("~/.ssh/config")
if os.path.exists(file_ssh):
    with open(file_ssh) as f:
        ssh_config.parse(f)


_local_repo = eval(cfg['_local_repo'])
cfg['servers']['local']['repo_project'] = _local_repo
cfg['servers']['local']['root'] = os.path.split(_local_repo)[0]
cfg['servers']['local']['dir_project'] = cfg['servers']['local']['repo_project']+'/'+cfg['project']
cfg['servers']['local']['path_apps'] = cfg['servers']['local']['repo_project']+cfg['dir_apps']
cfg['servers']['local']['backup_dir'] = cfg['servers']['local']['repo_project']+'/backup'


# save ssh config to cfbg dict
for server in cfg['servers']:
    host = ssh_config.lookup(server)
    cfg['servers'][server]['user'] = host['user']
    cfg['servers'][server]['hostname'] = host['hostname']
    cfg['servers'][server]['port'] = host['port']
    cfg['servers'][server]['source'] = server+':'+cfg['servers'][server]['repo_project']
    cfg['servers'][server]['target'] = server+':'+cfg['servers'][server]['root']


def _create_conda_env():
    """Create a conda env"""
    run('conda create -y -n %s' % cfg['conda_env'])



def _setup(_server):
    env.host_string = _server
    env.user = cfg['servers'][_server]['user']
    env.home = cfg['servers'][_server]['home']
    cfg['current_server'] = _server


def migrate(server, app='core', info=None):
    """ Make django migrations"""
    _setup(server)

    migrate_file = cfg['servers'][server]['dir_apps']+app+'/'+cfg['migrate_file']
    old_file = migrate_file+'_old'
    local_file = cfg['servers']['local']['path_apps']+app+'/'+cfg['migrate_file']

    if info is not None:
        info = [{'migrate_file': migrate_file},
                {'old_file': old_file},
                {'local_file': local_file}]
        __info(info, server)
        return

    # copy current models.py to models.py_old
    run ('cp %s %s' % (migrate_file,  old_file) )

    # Copy models.py from local to remote
    put (local_file, migrate_file)


    # Migrate apply
    with cd(cfg['servers'][server]['repo_project']):
        with prefix(cfg['servers'][server]['env_activate']):
            run ('./manage.py makemigrations %s' % app)
            run ('./manage.py migrate %s' % app)


def update_reqs(server):
    """Update requirements and collectstatic"""

    _setup(server)
    with cd(cfg['servers'][server]['repo_project']):
        with prefix(cfg['servers'][server]['env_activate']):
            run( 'pip install -r requirements' )
            run('./manage.py collectstatic --no-input -v 1')


def rsync(_src, _target, _info=None):
    '''Synchronize server via rsync'''
    _src = __chkserver(_src)
    _target = __chkserver(_target)

    if _src is None or _target is None or _src=='staging':
        print ("Valid src: local, l, producao, ou p")
        print ("Valid target: producao, p, staging ou  s")
        return

    if _src in ['producao', 'p'] and _target in ['l', 'local']:
        print ('De produção para local, não é permitido. Somente para staging, use o CVS')
        return


    if _src=='producao':
        src = cfg['servers']['producao']['source']
        target = cfg['servers']['staging']['root']
        #src = cfg['servers']['producao']['repo_project']
        #target = cfg['servers']['staging']['root']
        _setup('staging')

    if _src =='local':
        src = cfg['servers']['local']['repo_project']
        if _target == 'staging':
            target = cfg['servers']['staging']['root']
            _setup('staging')
        else:
            target = cfg['servers']['producao']['root']
            _setup('producao')
            cfg['current_server'] = 'local'  # Atende ao format env de fabric


    info = [{'_src: ': _src}, {'_target: ': _target},
            {'src: ': src}, {'target: ': target},
            {'env.host_string': env.host_string},
            {'env.user': env.user}]

    if _info is not None:
        __info(info)
        return

    cfg['current_server'] = _src
    __rsync(src, target)


def __rsync(src, target):

    print ('src==>', src)
    print ('target ==>', target)
    print ('current_server ==>', cfg['current_server'])


    if cfg['current_server']=='producao':
        # env.password = cfg['servers']['local']['pswd']
        run ("rsync --delete --compress -chazp --stats --exclude '*.sock' %s %s" %(src, target))
        return
        

    rsync_project(
        local_dir=src,
        remote_dir=target,
        exclude = cfg['rsync_exclude'],
        delete=True,
        extra_opts='--omit-dir-times',
    )


def rsdeploy(server, comment=None, migrate='n', app='core', info=None):
    """ Complete deploy via rsync"""

    _target = __chkserver(server)
    if _target not in ['producao', 'staging']:
        print (_target)
        print ('parametros para servidor validos: p, s, producao e staging')
        return
    server = _target

    _src = 'local'
    _setup('local')

    lsti = [{'_src': _src}, {'target': _target}]
    if info is not None:
        __info(lsti)
        return


    # Synchronize staging with production if current deploy is to staging
    if server=='staging':
        try:
            rsync('producao', 'staging')
        except:
            abort ('Erro em rsyn de de producao para staging')
        dbprod2staging()


    # Make migrate
    if migrate=='s':
        migrate(server)


    #  Synchronize the code (local -> target)
    try:
        rsync(_src, _target)
    except:
        abort ("Erro rsync (final)")


    # Update requirements
    update_reqs(server)

    # Restart server
    _restart_remote(server)

    # Update CVS
    if comment is not None:
        gitpush(comment)


def _restart_remote(server=None):
    """Restart remote server via CLI"""
    _setup(server)
    with cd( cfg['servers'][server]['home']):
        sudo ('systemctl restart gunicorn')
        sudo ('systemctl restart nginx')


def gitpush(comment, option='u'):
    """Update repo git"""
    _setup('local')

    with cd(cfg['servers']['local']['repo_project'] ):
        if option=='u':
            run ('git add -u')
            run ('git commit -m %s' % comment)
            run ('git push origin master')


def dbprod2staging():
    '''Synchronize database (Production -> Staging)'''
    _setup('staging')
    execute(dumpdb, cfg['servers']['staging']['db_name'], 'producao', server='staging')
    #execute(__recreate, cfg['servers']['staging']['db_name'], 'staging')


def dbprod2local():
    '''Synchronize database (Production -> local) '''
    _setup('staging')
    execute(dumpdb, cfg['servers']['local']['db_name'], 'producao', server='local')
    #execute(__recreate, cfg['servers']['staging']['db_name'], 'staging')


# Sincroniza o banco local com o staging
def dbstaging2local():
    '''Synchronize database (Staging -> Local'''
    _setup('local')
    execute(dumpdb, cfg['servers']['local']['db_name'], 'staging')

def __dump_name(dbname, host):
    return dbname+"_"+host+'.sql'


def dumpdb(dbname, host, server='local'):
    '''Create dump file from database on host and recreate on server'''

    _setup(server)
    dump_name = __dump_name(dbname, host)
    cfg['dump'] = cfg['servers'][server]['backup_dir']+'/'+dump_name
    dump_name = cfg['servers'][host]['backup_dir']+'/'+dump_name
    run('if [ -e %s ]; then rm -rf %s; fi' %(dump_name, dump_name))
    run("ssh %s 'pg_dump -U %s -h localhost -C --column-inserts > %s'" %(host, dbname, dump_name))
    src = host+':'+dump_name
    run ('scp %s %s' %(src, cfg['servers'][server]['backup_dir']))

    execute(__recreate, dbname, server)


def __recreate(dbname, server):
    _setup(server)
    run("dropdb -h localhost -U supostgres --if-exists %s" %(dbname))
    run("createdb -h localhost -U supostgres -O %s %s" %(dbname, dbname))
    run("psql -h localhost -U supostgres %s < %s" %(dbname, cfg['dump']))


def __info(lst_info):

    lst_info.append({'current_server': cfg['current_server']})
    print('\nVariáveis específicas')
    print('---------------------')
    for d in lst_info:
        print (d)

    print ('\nVariáveis default')
    print ('-----------------')
    info()


def info(_server='local'):
    """info of vars"""

    for server in cfg['servers'].keys():
        print(server, 'green')
        pp.pprint (cfg['servers'][server])

    ''' 
    _setup(_server)
    print("cfg[_server]['hostname']: ",  cfg[_server]['hostname'])
    print("cfg[_server]['port']: ", cfg[_server]['port'])
    print("env.host_string: ", env.host_string)
    print("env.user: ", env.user)
    print("env.home: ",  env.home )
    print("cfg['current_server']: ", cfg['current_server'] )


    print("cfg['servers']['local']['repo_project'] ", cfg['servers']['local']['repo_project'])
    print("cfg['servers']['local']['dir_project'] ", cfg['servers']['local']['dir_project'])
    print("cfg['servers']['local']['path_apps']  ", cfg['servers']['local']['path_apps'])
    '''

def __chkserver(_server):
    if _server not in ['p', 's', 'l', 'producao', 'staging', 'local']:
        return None

    if _server=='p':
        _server = 'producao'
    elif _server=='s':
        _server = 'staging'
    elif _server=='l':
        _server = 'local'

    return _server