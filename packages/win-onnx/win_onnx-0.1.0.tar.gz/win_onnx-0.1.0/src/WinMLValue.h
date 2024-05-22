//
// Created by whl on 24-5-21.
//

#pragma once
#include <winrt/Windows.AI.MachineLearning.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <vector>
#include <winrt/windows.foundation.h>
#include <winrt/windows.foundation.collections.h>

class WinMLValue {
public:
    WinMLValue() = default;

    WinMLValue(const pybind11::array &array);

    pybind11::array ToNumpyArray() const;

    winrt::Windows::AI::MachineLearning::TensorFloat AsTensorFloat() const;

    winrt::Windows::AI::MachineLearning::TensorInt64Bit AsTensorInt64() const;

    winrt::Windows::AI::MachineLearning::TensorUInt8Bit AsTensorUInt8() const;

    winrt::Windows::AI::MachineLearning::TensorFloat16Bit AsTensorFloat16() const;

    winrt::Windows::AI::MachineLearning::TensorDouble AsTensorDouble() const;

    winrt::Windows::AI::MachineLearning::TensorInt8Bit AsTensorInt8() const;

    winrt::Windows::AI::MachineLearning::TensorUInt16Bit AsTensorUInt16() const;

    winrt::Windows::AI::MachineLearning::TensorUInt32Bit AsTensorUInt32() const;

    winrt::Windows::AI::MachineLearning::TensorUInt64Bit AsTensorUInt64() const;

    winrt::Windows::AI::MachineLearning::TensorInt16Bit AsTensorInt16() const;

    winrt::Windows::AI::MachineLearning::TensorInt32Bit AsTensorInt32() const;

    winrt::Windows::AI::MachineLearning::TensorKind GetTensorKind() const;

private:
    pybind11::array array_;
    winrt::Windows::AI::MachineLearning::TensorKind tensor_kind_;

    void DetermineTensorKind();
};
