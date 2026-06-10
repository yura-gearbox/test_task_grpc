#!/bin/bash

# stop script on any error
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE}")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/cpp-application"
BUILD_DIR="${SCRIPT_DIR}/build"

echo "[BUILD] Create build folder..."
mkdir -p "${BUILD_DIR}"

echo "[BUILD] Copying of adapter ProtobufConfig.cmake..."
cp "${SCRIPT_DIR}/ProtobufConfig.cmake.template" "${BUILD_DIR}/ProtobufConfig.cmake"

echo "[BUILD] Run config CMake..."
# CMAKE_PREFIX_PATH defines where ProtobufConfig is located 
cmake -S "${SOURCE_DIR}" -B "${BUILD_DIR}" -DCMAKE_PREFIX_PATH="${BUILD_DIR}"

echo "[BUILD] Compilation..."
cmake --build "${BUILD_DIR}" --parallel

echo "[BUILD] Build is complete successfully.!"
echo "[BUILD] Location of the executable file: ${BUILD_DIR}/grpc_udp_monitor"
