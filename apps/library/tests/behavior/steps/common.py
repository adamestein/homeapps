from pytest_bdd import given, then, when

from library.testing.notify import dialog


@given('pause')
@when('pause')
@then('pause')
def pause(request, wip_mode):
    if wip_mode:
        dialog('Paused', 'Click to continue', 'Press Enter to continue ...', ok_only=True)


@given('I proceed normally')
@when('I proceed normally')
@then('I proceed normally')
def stepbystep(request):
    request.config.stepbystep = False


@given('I proceed step by step')
@when('I proceed step by step')
@then('I proceed step by step')
def stepbystep(request):
    request.config.stepbystep = True
