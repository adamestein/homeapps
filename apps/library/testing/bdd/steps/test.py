# noinspection PyPackageRequirements
from behave import given, then, when


@given('pause')
@then('pause')
@when('pause')
def pause(context):
    # Text given to raw_input() may not be shown if stdout is captured, so safer to use the output stream
    context.config.outputs[0].stream.write('Press Enter to continue ...')
    input()
