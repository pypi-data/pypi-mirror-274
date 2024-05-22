cmake_minimum_required(VERSION 3.21)

project(whisper_cpp)

set(BUILD_SHARED_LIBS "On")

set(WHISPER_METAL "On" CACHE BOOL "whisper: use Metal" FORCE)
set(WHISPER_METAL_EMBED_LIBRARY "On" CACHE BOOL "whisper: embed metal library" FORCE)

add_subdirectory(vendor/whisper.cpp)
install(
    TARGETS whisper 
    LIBRARY DESTINATION ${SKBUILD_PLATLIB_DIR}/whisper_cpp
    RUNTIME DESTINATION ${SKBUILD_PLATLIB_DIR}/whisper_cpp
    ARCHIVE DESTINATION ${SKBUILD_PLATLIB_DIR}/whisper_cpp
    FRAMEWORK DESTINATION ${SKBUILD_PLATLIB_DIR}/whisper_cpp
    RESOURCE DESTINATION ${SKBUILD_PLATLIB_DIR}/whisper_cpp
)
# Temporary fix for https://github.com/scikit-build/scikit-build-core/issues/374
install(
    TARGETS whisper 
    LIBRARY DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/whisper_cpp
    RUNTIME DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/whisper_cpp
    ARCHIVE DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/whisper_cpp
    FRAMEWORK DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/whisper_cpp
    RESOURCE DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/whisper_cpp
)
install(
    FILES $<TARGET_RUNTIME_DLLS:whisper>
    DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/whisper_cpp
)
