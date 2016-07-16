/*
 * File: tradebot.go
 * ------------------------------
 * Tradebot
 */

package main

import (
    "fmt"
    "encoding/json"
    "io"
    "log"
    "strings"
    "net"
)

func handleConnection(c net.Conn) {
    d : json.NewDecoder(c)

}

func listen() {
    ln, err := net.Listen("tcp", ":9999")
    if err != nil {
        fmt.Println(err)
        return
    }
}

func main() {
    fmt.Print("tradebot starting up...")
}