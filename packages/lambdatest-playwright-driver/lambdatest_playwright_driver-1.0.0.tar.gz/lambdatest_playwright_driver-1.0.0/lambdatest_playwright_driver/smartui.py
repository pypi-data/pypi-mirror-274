from lambdatest_sdk_utils import is_smartui_enabled, fetch_dom_serializer, post_snapshot # type: ignore
from lambdatest_sdk_utils import setup_logger, get_logger # type: ignore
from playwright.async_api import Page # type: ignore

def smartui_snapshot(page: Page, name: str, options={}):
    # setting up logger
    setup_logger()
    logger = get_logger('lambdatest-playwright-driver')
    

    if not page:
        raise ValueError('A Playwright `page` object is required.')
    if not name:
        raise ValueError('The `snapshotName` argument is required.')
    if is_smartui_enabled() is False: 
        raise Exception("Cannot find SmartUI server.")
    
    try:
        resp = fetch_dom_serializer()
        page.evaluate(resp['data']['dom'])
                
        dom = dict()
        dom['name'] = name
        dom['url'] = page.url        
        dom['dom'] = page.evaluate("([options]) => SmartUIDOM.serialize(options)",[options])
        
        res = post_snapshot(dom, 'lambdatest-playwright-driver', options=options)

        if res and res.get('data') and res['data'].get('warnings') and len(res['data']['warnings']) != 0:
            for warning in res['data']['warnings']:
                logger.warning(warning)

        logger.info(f'Snapshot captured {name}')
    except Exception as e:
        logger.error(f"SmartUI snapshot failed '{name}'")
        logger.error(e)


