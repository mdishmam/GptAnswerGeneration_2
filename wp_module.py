from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.compat import xmlrpc_client
import datetime

# https://brickmeup.cloud/wp-login.php
# client = Client('https://brickmeup.cloud/xmlrpc.php', 'admin', 'admin')

SITE_URL = ''
USERNAME = ''
PASSWORD = ''
client = None

def get_site_details(url:str, username:str, password:str):
    global SITE_URL, USERNAME, PASSWORD, client
    SITE_URL = url if 'xmlrpc.php' in url else f'{url}/xmlrpc.php'
    USERNAME = username
    PASSWORD = password

    client = Client(SITE_URL, USERNAME, PASSWORD)
# client = Client('https://brickmeup.cloud/xmlrpc.php', 'admin', 'admin')

wp_creds_file = open('wp_credentials.txt')
wp_cred = wp_creds_file.readlines()
wp_creds_file.close()

get_site_details(wp_cred[0], wp_cred[1], wp_cred[2])

def upload_image(file_path, file_name):
    print('Uploading image...')
    global client
    data = {
            'name': file_name.strip() + '.jpg',
            # 'name': datetime.datetime.now().strftime('%d%m%y%H%M%S') + '.jpg',
            'type': 'image/jpeg',  # mimetype
    }

    # read the binary file and let the XMLRPC library encode it into base64
    with open(file_path, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

    response = client.call(media.UploadFile(data))
    # response == {
    #       'id': 6,
    #       'file': 'picture.jpg'
    #       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
    #       'type': 'image/jpeg',
    # }
    # attachment_id = response['id']
    print('\t\tdone.')
    return response['id'], response['url']

def post_in_wp(title, body, thumbnail=None, status='publish', tag='', category=''):
    print('Uploading post...')
    global client
    post = WordPressPost()
    post.title = title
    post.content = body
    post.post_status = status
    post.thumbnail = thumbnail
    post.terms_names = {
                        # 'post_tag': [tag],
                        'category': [category]
                     }
    post.id = client.call(posts.NewPost(post))

    print('\t\tdone.')
    return post.id


# post_in_wp(title='test', body='test', category='large_test')
