# Compiler settings
CXX = g++
CXXFLAGS = -std=c++17 -Wall
LDFLAGS = -L$(shell brew --prefix sfml)/lib -lsfml-graphics -lsfml-window -lsfml-system

# Directories
INCLUDES = -I$(shell brew --prefix sfml)/include

# Source files
SRC = trafficSimulationEE273.cpp

# Output file
OUT = trafficSimulationEE273

# Default target
all: $(OUT)

# Rule for compiling the project
$(OUT): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) $(INCLUDES) $(LDFLAGS) -o $(OUT)

# Clean rule
clean:
	rm -f $(OUT)

# Rebuild everything
rebuild: clean all

