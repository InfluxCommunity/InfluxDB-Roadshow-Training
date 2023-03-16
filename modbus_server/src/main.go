package main

import (
	"encoding/binary"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"syscall"

	"github.com/grid-x/modbus"
	"github.com/tbrandon/mbserver"
)

type Config struct {
	Address   string            `json:"address"`
	Registers map[string]string `json:"registers"`
}

// Define a function to return the holding register value as data
func createReadFunction(registers map[uint16]uint16) func(*mbserver.Server, mbserver.Framer) ([]byte, *mbserver.Exception) {
	return func(_ *mbserver.Server, f mbserver.Framer) ([]byte, *mbserver.Exception) {
		framer, ok := f.(*mbserver.TCPFrame)
		if !ok {
			return nil, &mbserver.GatewayTargetDeviceFailedtoRespond
		}
		if framer.Device != 1 {
			return nil, &mbserver.GatewayTargetDeviceFailedtoRespond
		}

		data := f.GetData()
		register := binary.BigEndian.Uint16(data[0:2])
		nRegs := binary.BigEndian.Uint16(data[2:4])
		nBytes := nRegs * 2
		log.Printf("Got read request with function %d at %d with %d registers\n", f.GetFunction(), register, nRegs)

		// Add the length in bytes and the register to the returned data
		buf := make([]byte, nBytes+1)
		buf[0] = byte(nBytes)
		for i := uint16(0); i < nRegs; i++ {
			r := register + i
			binary.BigEndian.PutUint16(buf[2*i+1:], registers[r])
		}
		return buf, &mbserver.Success
	}
}

func main() {
	// Check command line arguments
	if len(os.Args) < 2 {
		log.Fatalf("Usage: %s <config file>", os.Args[0])
	}

	// Read the configuration and prepare the registers
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		log.Fatalf("Reading file %q failed: %v", os.Args[1], err)
	}
	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		log.Fatalf("Parsing configuration failed: %v", err)
	}

	if cfg.Address == "" {
		log.Fatalln("Required address missing in configuration")
	}
	if len(cfg.Registers) == 0 {
		log.Fatalln("No registers specified")
	}

	registers := make(map[uint16]uint16, len(cfg.Registers))
	for k, v := range cfg.Registers {
		register, err := strconv.ParseUint(k, 10, 16)
		if err != nil {
			log.Fatalf("invalid register %q: %v", k, err)
		}
		hex := strings.ToLower(v)
		hex = strings.TrimPrefix(hex, "0x")
		hex = strings.TrimPrefix(hex, "x")
		value, err := strconv.ParseUint(hex, 16, 16)
		if err != nil {
			log.Fatalf("invalid value %q for register %q: %v", v, k, err)
		}
		registers[uint16(register)] = uint16(value)
	}

	// Setup a Modbus server to test against
	serv := mbserver.NewServer()
	readFunc := createReadFunction(registers)
	serv.RegisterFunctionHandler(modbus.FuncCodeReadHoldingRegisters, readFunc)
	if err := serv.ListenTCP(cfg.Address); err != nil {
		panic(err)
	}
	defer serv.Close()

	fmt.Printf("Listening for connections at tcp://%s...\n", cfg.Address)
	done := make(chan os.Signal, 1)
	signal.Notify(done, syscall.SIGINT, syscall.SIGTERM)
	fmt.Println("Blocking, press ctrl+c to continue...")
	<-done // Will block here until user hits ctrl+c
}
