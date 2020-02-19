from time import sleep

from selenium.webdriver.common.action_chains import ActionChains

from django.shortcuts import resolve_url

from library.testing.image import get_fullpage_screenshot_as_png


def get_screenshot(context, full_page=True, remove_caret=True, remove_mouse=True):
    if remove_mouse:
        # Make sure the mouse does not affect the screen shot in any way
        ActionChains(context.browser.driver).move_by_offset(0, 0).perform()
        sleep(1)

    if remove_caret:
        # Always remove any blinking carets as you can never tell if the snapshot will be taken with it being seen
        context.browser.execute_script(
            '''
            var focused = $(document).find(":focus");
            if (focused.length && focused.prop("tagName") === "INPUT") {
                focused.css("color", "transparent").css("text-shadow", "0 0 0 #000");
            }
            '''
        )
        sleep(1)

    screenshot = get_fullpage_screenshot_as_png(context) if full_page else context.browser.driver.get_screenshot_as_png()

    if remove_caret:
        # Restore caret color back to normal
        context.browser.execute_script(
            '''
            var focused = $(document).find(":focus");
            if (focused.length && focused.prop("tagName") === "INPUT") {
                focused.css("color", "rgb(0, 0, 0)").css("text-shadow", "");
            }
            '''
        )

    return screenshot


def get_url(context, to=None, *args, **kwargs):
    return context.config.server_url + (resolve_url(to, *args, **kwargs) if to else '')
