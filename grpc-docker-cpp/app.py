from __future__ import print_function
import logging
 
import grpc
 
import helloworld_pb2
import helloworld_pb2_grpc
 
from helloworld_pb2 import ComputeRequest, Operator
 
from flask import Flask, request
 
 
app = Flask(__name__)
 
 
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
 
    return f"Greeter client received: {response.message} \n"
 
def calc_run(ops, lhs, rhs):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        compute_req = ComputeRequest(operator=ops, lhs=lhs, rhs=rhs)
 
        response = stub.Compute(compute_req)
 
    return f"Compute client received: {response.result} \n"
 
 
@app.route('/', methods=['GET'])
def index():
    return run()
 
@app.route('/calc', methods=['GET'])
def calc():
    query_dict = request.args.to_dict()
    ops = query_dict['ops']
    lhs = query_dict['lhs']
    rhs = query_dict['rhs']
 
    print(ops, lhs, rhs)
 
    ops_dict = {'add': Operator.ADD, 'sub': Operator.SUB,
                'mul': Operator.MUL, 'div': Operator.DIV,
                'pow': Operator.POW}
   
 
    return calc_run(ops_dict[ops], float(lhs), float(rhs))
 
 
if __name__ == '__main__':
    logging.basicConfig()
 
    app.run()
