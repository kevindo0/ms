from flask import Blueprint
from flask import jsonify
from flask import request

from . import controller
from . import forms as f

ptest_bp = Blueprint('ptest_bp', __name__)


@ptest_bp.route('/test', methods=['GET', 'POST'])
def test_test():
    method = request.method
    if method == 'GET':
        params = request.args.to_dict()
        gf = f.GetForm(data=params)
        print('count:', type(gf.count.data))
        # print('params:', params)
        res = controller.c_get_test(params)
    else:
        data = request.json
        # print('data:', data)
        res = controller.c_post_test(data)
    return jsonify(res)
