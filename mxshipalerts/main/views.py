from . import main


@main.route('/actions', methods=['POST'])
def actions():
    return 'Works!'


