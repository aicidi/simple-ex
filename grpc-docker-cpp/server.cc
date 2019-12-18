/*
 *
 * Copyright 2019 The Cloud Robotics Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */
 
#include <csignal>
#include <future>
#include <iostream>
#include <memory>
#include <string>
#include <thread>
 
#include <cmath>
 
#include <grpcpp/grpcpp.h>
 
#include "helloworld.grpc.pb.h"
 
using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using helloworld::Greeter;
using helloworld::HelloReply;
using helloworld::HelloRequest;
 
using helloworld::Operator;
using helloworld::ComputeRequest;
using helloworld::ComputeResponse;
 
// The gRPC server is defined globally so that SIGTERM handler can shut it
// down when Kubernetes stops the process.
std::unique_ptr<Server> server;
 
// Logic and data behind the server's behavior.
class GreeterServiceImpl final : public Greeter::Service {
  Status SayHello(ServerContext* context, const HelloRequest* request,
                  HelloReply* reply) override {
    std::cout << "Received request: " << request->ShortDebugString()
              << std::endl;
    std::string prefix("Hello ");
    reply->set_message(prefix + request->name());
    return Status::OK;
  }
 
  Status Compute(ServerContext* context, const ComputeRequest* request, ComputeResponse* reply) override
 {
    switch(request->operator_()) {
    case Operator::ADD:
            reply->set_result(request->lhs() + request->rhs());
            break;
 
        case Operator::SUB:
            reply->set_result(request->lhs() - request->rhs());
            break;
 
        case Operator::MUL:
            reply->set_result(request->lhs() * request->rhs());
            break;
 
        case Operator::DIV:
            reply->set_result(request->lhs() / request->rhs());
            break;
 
        case Operator::POW:
            reply->set_result(std::pow(request->lhs(), request->rhs()));
            break;
 
        default:
            return Status{grpc::INVALID_ARGUMENT, "Unknown operator."};
    }
 
    return Status::OK;
 }
};
 
void RunServer() {
  std::string server_address("0.0.0.0:50051");
  GreeterServiceImpl service;
 
  ServerBuilder builder;
  // Listen on the given address without any authentication mechanism. Cloud
  // Robotics Core ensures that clients are authenticated.
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  // Register "service" as the instance through which we'll communicate with
  // clients. In this case it corresponds to a *synchronous* service.
  builder.RegisterService(&service);
  // Finally assemble the server.
  server = builder.BuildAndStart();
  std::cout << "Server listening on " << server_address << std::endl;
 
  std::signal(SIGTERM, [](int) {
    // When SIGTERM is received, shutdown the gRPC server.
    server->Shutdown();
  });
 
  // Wait for the server to shutdown.
  server->Wait();
}
 
int main(int argc, char** argv) {
  RunServer();
 
  return 0;
}
