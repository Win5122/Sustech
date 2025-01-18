package main

import (
	"context"
	"dncc/grpc/pb"
	"fmt"
	"log"
	"os"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	// Create a gRPC channel with no SSL/TLS configured.
	conn, err := grpc.NewClient("127.0.0.1:8082", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	// Specify to close the gRPC channel later (when the function finishes)
	defer conn.Close()
	// Create a client stub
	stub := pb.NewAssistantServiceClient(conn)
	// Greeting
	fmt.Println("> Greet: Hello Assistant?")
	greetRes, err := stub.GreetWithInfo(context.Background(), &pb.GreetRequest{
		UserName:    "Peter",
		Institution: "SUSTech",
	})
	if err != nil {
		fmt.Printf("> Failed to greet: %v", err)
		os.Exit(0)
	}
	fmt.Printf("Client received:\n%v\n", greetRes)
	// Multiplication
	fmt.Println("> Mult: Requesting a multiplication task")
	multRes, err := stub.Multiply(context.Background(), &pb.MultRequest{
		Xin: 3.5,
		Yin: 5,
	})
	fmt.Printf("> Client received:\n%v\n", multRes)
}
