# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 13:53:17 2019

@author: zzhqi
"""
import json

from flask import Flask, request
from flask import current_app

app = Flask(__name__)


class Customer:
    def __init__(self, name, grade, age, home, office):
        self.name = name
        self.grade = grade
        self.age = age
        # self.address = Address(home, office)

    def __repr__(self):
        return repr((self.name, self.grade, self.age, self.address.home, self.address.office))


class Address:
    def __init__(self, home, office):
        self.home = home
        self.office = office

    def __repr__(self):
        return repr((self.name, self.grade, self.age))


@app.route('/test', methods=['POST'])
def hello_world():
    print(request.get_data())
    print(current_app.name)
    test_dict = {}
    test_dict['test1'] = 1
    test_dict['test2'] = 1

    customers = [
        Customer('john', 'A', 15, '111', 'aaa'),
        Customer('jane', 'B', 12, '222', 'bbb'),
        Customer('dave', 'B', 10, '333', 'ccc'),
    ]
    json_str = json.dumps(customers, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    print(json_str)

    # return json.dumps(test_dict)
    return json_str


if __name__ == '__main__':
    app.run(debug=True)
