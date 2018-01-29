cmake_minimum_required(VERSION 2.8)

cmake_policy(SET CMP0048 NEW)

project(tests VERSION "0.1.0")

MESSAGE(STATUS "CMAKE_SOURCE_DIR \t\t" ${CMAKE_SOURCE_DIR})
MESSAGE(STATUS "CMAKE_CURRENT_BINARY_DIR \t" ${CMAKE_CURRENT_BINARY_DIR})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -std=c++11")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -pthread")

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_CURRENT_BINARY_DIR}/bin)

include_directories(${PROJECT_SOURCE_DIR}/include)

set(SOURCE_LIB ${PROJECT_SOURCE_DIR}/src/tests.cpp)
add_library(tests STATIC ${SOURCE_LIB})

file(GLOB SOURCE_FILES ${CMAKE_SOURCE_DIR}/scripts/*.cpp)

foreach(f_name ${SOURCE_FILES})
	string(REPLACE ".cpp" "" t_name ${f_name})
	string(REPLACE "/" ";" t_name ${t_name})	
	foreach(t ${t_name})		
		set(out_name ${t})
	endforeach(t)		

	add_executable(${out_name} ${f_name})
	target_link_libraries(${out_name} tests libMantisAPI.so)
endforeach(f_name)
