cmake_minimum_required(VERSION 2.8)

cmake_policy(SET CMP0048 NEW)

project(apitest VERSION "0.1.0")

enable_testing()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -std=c++11")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -pthread")

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_CURRENT_BINARY_DIR}/bin)

include_directories(${PROJECT_SOURCE_DIR}/include)

#set(SOURCE_LIB ${PROJECT_SOURCE_DIR}/src/apitest.cpp)
#add_library(tests STATIC ${SOURCE_LIB})

find_package (Threads REQUIRED)

include(ExternalProject)

ExternalProject_Add(
    gtest
    URL https://github.com/google/googletest/archive/master.zip
    PREFIX ${CMAKE_CURRENT_BINARY_DIR}/gtest
    
    INSTALL_COMMAND ""
)

ExternalProject_Get_Property(gtest SOURCE_DIR BINARY_DIR)

add_library(libgtest IMPORTED STATIC GLOBAL)
add_dependencies(libgtest gtest)

set_target_properties(libgtest PROPERTIES
    "IMPORTED_LOCATION" "${BINARY_DIR}/googlemock/gtest/libgtest.a"
    "IMPORTED_LINK_INTERFACE_LIBRARIES" "${CMAKE_THREAD_LIBS_INIT}"
)

add_library(libgmock IMPORTED STATIC GLOBAL)
add_dependencies(libgmock gtest)

set_target_properties(libgmock PROPERTIES
    "IMPORTED_LOCATION" "${BINARY_DIR}/googlemock/libgmock.a"
    "IMPORTED_LINK_INTERFACE_LIBRARIES" "${CMAKE_THREAD_LIBS_INIT}"
)

include_directories("${SOURCE_DIR}/googletest/include"
                    "${SOURCE_DIR}/googlemock/include")

file(GLOB SOURCE_FILES ${CMAKE_SOURCE_DIR}/scripts/*.cpp)

foreach(f_name ${SOURCE_FILES})
	string(REPLACE ".cpp" "" t_name ${f_name})
	string(REPLACE "/" ";" t_name ${t_name})	
	foreach(t ${t_name})		
		set(out_name ${t})
	endforeach(t)		

	add_executable(${out_name} ${f_name})

	target_link_libraries(${out_name} libgtest libgmock libMantisAPI.so)
endforeach(f_name)
