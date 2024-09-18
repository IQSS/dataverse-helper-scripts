from stress_settings import *
import random, string
import json
from search_pages import get_random_search_url
from mydata_links import get_random_mydata_url

#from bs4 import BeautifulSoup


FILE_ID_MAP = dict(k_250=2670610,
                  k_500=2670615,
                  mb_1=2670612,
                  mb_2=2670613,
                  mb_5=2670608,
                  mb_10=2670609,
                  mb_50=2670614,
                  mb_100=2670611,
                  #gb_1=2670827
                  )

def get_locust_request_kwargs():
    return dict(verify=False,)   # allow a self-signed certificate

def login_page_but_no_login(l):
    msg('> login page (but no login)')
    l.client.get('/loginpage.xhtml', **get_locust_request_kwargs())

def harvested_page(l):
    msg('> harvested_page')
    l.client.get('/dataverse/harvested', **get_locust_request_kwargs())
    #rhttps://dataverse.harvard.edu/dataverse/harvested

def usual_static_resources(l):
    """
    Get the css, js, etc. associated with most pages
    """
    resource_links = [
        '/javax.faces.resource/theme.css.xhtml?ln=primefaces-bootstrap',
        '/javax.faces.resource/jquery/jquery.js.xhtml?ln=primefaces&v=4.0',
        '/javax.faces.resource/primefaces.js.xhtml?ln=primefaces&v=4.0',
        '/javax.faces.resource/primefaces.css.xhtml?ln=primefaces&v=4.0',
        #'/jquery/jquery-plugins.js.xhtml?ln=primefaces&v=4.0',
        #'/jquery/jquery-plugins.js.xhtml?ln=primefaces&v=4.0',
        '/javax.faces.resource/bs/css/bootstrap.css.xhtml?version=4.2',
        '/javax.faces.resource/css/structure.css.xhtml?version=4.2',
        '/javax.faces.resource/js/owl.carousel.js.xhtml?version=4.2',
        '/javax.faces.resource/js/jquery.sharrre.js.xhtml?version=4.2',
    ]
    for rlink in resource_links:
        l.client.get(rlink, **get_locust_request_kwargs())

def random_mydata_page(l):

    #r = l.client.get('/dataverseuser.xhtml?selectTab=dataRelatedToMe', **get_locust_request_kwargs())
    #print r.text
    #return

    mydata_info = get_random_mydata_url()
    description, mydata_url = mydata_info
    mydata_url += "&key={0}".format(get_creds_info('API_TOKEN_FOR_MY_DATA'))
    msg('> search url: {0}'.format(description))
    #msg('> search url: {0} - {1}'.format(description, mydata_url))
    r = l.client.get(mydata_url, **get_locust_request_kwargs())
    print ('r.status_code', r.status_code)
    print ('r.text', r.text[:200])

def random_search_page(l):
    search_url = get_random_search_url()
    msg('> search url: {0}'.format(search_url))
    l.client.get(search_url, **get_locust_request_kwargs())

def homepage(l):
    msg('> homepage')
    l.client.get('/', **get_locust_request_kwargs())

def homepage_files_facet(l):
    msg('> homepage (q=&types=files)')
    l.client.get('/?q=&types=files', **get_locust_request_kwargs())

def homepage_all_dvfacets(l):
    msg('> homepage (q=&types=files)')
    l.client.get('/?q=&types=files', **get_locust_request_kwargs())
    #?q=&types=dataverses%3Adatasets%3Afiles&sort=dateSort&order=desc&page=1

def profile_page(l):
    msg('> profile_page')
    r = l.client.get('/dataverseuser.xhtml', **get_locust_request_kwargs())

def random_dataset_page(l):
    msg('> random_dataset_page')

    persistent_ids = get_creds_info(KEY_PERSISTENT_IDS)
    assert persistent_ids is not None, 'No values found in creds file for %s' % KEY_PERSISTENT_IDS
    assert len(persistent_ids) > 0, 'No values found in creds file for list %s' % KEY_PERSISTENT_IDS

    random_id_info = random.choice(persistent_ids)

    pid = random_id_info['id']

    dataset_url = '/dataset.xhtml?persistentId=%s' % pid

    l.client.get(dataset_url, **get_locust_request_kwargs())


def login_attempt_with_user1_from_creds(l):

    username, password = get_user_creds(1)

    form_vals = {"loginForm:credentialsContainer2:0:credValue": username,
                 "loginForm:credentialsContainer2:1:sCredValue": password,
                 "loginForm": "loginForm"}
    #print 'form_vals', form_vals
    r = l.client.post('/loginpage.xhtml?redirectPage=/dataverseuser.xhtml',
                form_vals,
                **get_locust_request_kwargs())

    if r.status_code == 200:
        msg('login success!')
    else:
        msg('login fail')

def login_attempt_with_random_user_from_creds(l):

    username, password = get_random_user_creds()

    form_vals = {"loginForm:credentialsContainer2:0:credValue": username,
                 "loginForm:credentialsContainer2:1:sCredValue": password,
                 "loginForm": "loginForm"}

    r = l.client.post('/loginpage.xhtml?redirectPage=/dataverse.xhtml',
                form_vals,
                **get_locust_request_kwargs())

    if r.status_code == 200:
        msg('login success!')
    else:
        msg('login fail')

def login_fail_with_random_user_pw(l):
    msg('> Login Fail with random user/password')

    random_user = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    random_pass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    form_vals = {"loginForm:credentialsContainer2:0:credValue": random_user,
                "loginForm:credentialsContainer2:1:sCredValue": random_pass,
                "loginForm": "loginForm"}

    r = l.client.post('/loginpage.xhtml?redirectPage=/dataverse.xhtml',
                form_vals,
                **get_locust_request_kwargs())

    if r.status_code == 200:
        msg('login success!')
    else:
        msg('login fail')

def download_1g_file(l):

    download_url = '/api/access/datafile/%s' % FILE_ID_MAP.get('gb_1')

    msg("> Download 1gb file: %s " % (download_url))

    l.client.get(download_url, **get_locust_request_kwargs())

def assign_and_revoke_role(l):
    """
    Grant then revoke a role using the equivalent of these curl commands:

    1. scripts/search/tests/grant-spruce-admin-on-birds
    curl -s -X POST -H "Content-type:application/json" -d "{\"assignee\": \"@spruce\",\"role\": \"admin\"}" "http://localhost:8080/api/dataverses/birds/assignments?key=$FINCHKEY"

    2. scripts/search/tests/revoke-spruce-admin-on-birds
    curl -s -X DELETE "http://localhost:8080/api/dataverses/$BIRDS_DATAVERSE/assignments/$SPRUCE_ADMIN_ON_BIRDS?key=$FINCHKEY"
    """

    # get parameters from setting file

    dataverse = get_creds_info('API_TEST_INFO')['role_definition_point']
    # finch key (owns birds dataverse)
    key = get_creds_info('API_TEST_INFO')['api_token']
    #username ='@spruce'
    username = get_creds_info('API_TEST_INFO')['role_assignee']
    #role = 'admin'
    role = get_creds_info('API_TEST_INFO')['role']

    # make "grant role" request
    payload = dict(assignee=username, role=role)
    #url = '/api/dataverses/{0}/assignments?key={1}'.format(dataverse, key)
    url = '/api/dataverses/{0}/assignments'.format(dataverse)
    msg("> grant role assignment: %s " % (url))
    headers = { 'X-Dataverse-key':key, 'Content-type':'application/json' }
    r = l.client.post(url, data=json.dumps(payload), headers=headers, **get_locust_request_kwargs())
    if (r.status_code != 200):
        msg(r.text)
        return
    msg(r.text)
    rjson = r.json()
    # example JSON response: {"status":"OK","data":{"id":14,"assignee":"@spruce","roleId":1,"_roleAlias":"admin","definitionPointId":2}}
    new_id = rjson.get('data',{}).get('id')
    if new_id is None:
        msg('No id found in JSON from creating assignment: %s' % r.text)
        return

    # make "delete role" request
    #delete_url = '/api/dataverses/{0}/assignments/{1}?key={2}'.format(dataverse, new_id, key)
    delete_url = '/api/dataverses/{0}/assignments/{1}'.format(dataverse, new_id)
    r = l.client.delete(delete_url, headers=headers, **get_locust_request_kwargs())
    #print r.status_code
    print (r.text)
    #print r.json()


def random_download_file(l):
    """
    http://dvn-vm5.hmdc.harvard.edu:8080/api/access/datafile/2670610
    """
    global FILE_ID_MAP

    #gb_1=

    rand_selection = random.choice(FILE_ID_MAP.keys())
    #rand_selection = "mb_100"

    assert rand_selection in FILE_ID_MAP, "file size key not found.  Valid values: %s" % id_map.keys()

    download_url = '/api/access/datafile/%s' % FILE_ID_MAP.get(rand_selection)

    msg("> Download file (%s): %s " % (rand_selection, download_url))

    l.client.get(download_url, **get_locust_request_kwargs())
