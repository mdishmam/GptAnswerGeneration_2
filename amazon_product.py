from amazon_paapi import AmazonApi
from pprint import pprint
import urllib.parse

# KEY = 'AKIAIOEJ2UNIS2YLQPEQ'
# SECRET = '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'
# TAG = 'sujan051-20'
# COUNTRY = 'US'
creds_file = open('amazon_credentials.txt')
cred = creds_file.readlines()
creds_file.close()

KEY, SECRET, TAG, COUNTRY = cred[0].strip(), cred[1].strip(), cred[2].strip(), cred[3].strip()

amazon = AmazonApi(KEY, SECRET, TAG, COUNTRY)


def get_product(keyword):
    search_result = amazon.search_items(keywords=keyword)
    # pprint(search_result.items[0].get('asin'))


    link = '//ws-na.amazon-adsystem.com/widgets/q?ServiceVersion=20070822&OneJS=1&Operation=GetAdHtml&MarketPlace=US&source=ss&ref=as_ss_li_til&ad_type=product_link&tracking_id=##tracking_id##&language=en_US&marketplace=amazon&region=US&asins=##asin##&show_border=true&link_opens_in_new_window=true'
    link = link.replace('##tracking_id##',TAG)
    link = link.replace('##asin##', search_result.items[0].asin)
    print(link)
    # res = urllib.parse.parse_qs(link)
    # pprint(res)
    iframe = '<iframe sandbox="allow-popups allow-scripts allow-modals allow-forms allow-same-origin" style="width:120px;height:240px;" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" src=##link##></iframe>'
    iframe = iframe.replace('##link##', link)

    # script = """<script type="text/javascript">
    # amzn_assoc_tracking_id = "##tracking_id##";
    # amzn_assoc_ad_mode = "manual";
    # amzn_assoc_ad_type = "smart";
    # amzn_assoc_marketplace = "amazon";
    # amzn_assoc_region = "US";
    # amzn_assoc_design = "enhanced_links";
    # amzn_assoc_asins = "##asin##";
    # amzn_assoc_placement = "adunit";
    # amzn_assoc_linkid = "e6d894f2f7a9a1b74b6321c06e8377d6;
    # </script>"""
    # script = script.replace('##tracking_id##',TAG)
    # script = script.replace('##asin##', search_result.items[0].asin)


    return iframe



# ifr = get_product("why is my airbrush not spraying paint")