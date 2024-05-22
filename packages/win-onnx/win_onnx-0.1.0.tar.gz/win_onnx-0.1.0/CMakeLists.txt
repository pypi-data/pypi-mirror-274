cmake_minimum_required(VERSION 3.28)
project(WinML)

set(CMAKE_CXX_STANDARD 20)

# 引入FetchContent模块
include(FetchContent)

#set(PYTHON_EXECUTABLE "C:\\Users\\whl\\scoop\\apps\\anaconda3\\current\\App\\python.exe")

# 下载并引入pybind11
FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG v2.12.0  # 可以使用最新版本
)
FetchContent_MakeAvailable(pybind11)

# 查找Python
if(NOT DEFINED PYTHON_EXECUTABLE)
    message(FATAL_ERROR "Please set the PYTHON_EXECUTABLE variable to the Python interpreter path")
endif()
file(GLOB SOURCES "src/*.cpp")

pybind11_add_module(winml ${SOURCES})

#add_executable(WinML main.cpp)
