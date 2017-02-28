package main

import (
	"fmt"
	"github.com/firstrow/tcp_server"
)

func main() {
	server := tcp_server.New("localhost:1025")

	server.OnNewClient(func(c *tcp_server.Client) {
		// new client connected
		// lets send some message
		c.Send("hey")

	})
	server.OnNewMessage(func(c *tcp_server.Client, message string) {
		// new message received
		fmt.Println(message)

	})
	server.OnClientConnectionClosed(func(c *tcp_server.Client, err error) {
		// connection with client lost
		fmt.Println("closed")
	})

	server.Listen()
}
