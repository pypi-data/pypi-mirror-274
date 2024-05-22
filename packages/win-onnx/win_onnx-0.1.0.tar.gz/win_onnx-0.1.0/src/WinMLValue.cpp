//
// Created by whl on 24-5-21.
//

#include "WinMLValue.h"

using namespace winrt::Windows::AI::MachineLearning;
using namespace winrt::Windows::Foundation::Collections;
using namespace winrt::Windows::Foundation;

#include "WinMLValue.h"

using namespace winrt::Windows::AI::MachineLearning;

WinMLValue::WinMLValue(const pybind11::array &array) : array_(array) {
    DetermineTensorKind();
}

pybind11::array WinMLValue::ToNumpyArray() const {
    return array_;
}

TensorFloat WinMLValue::AsTensorFloat() const {
    auto buffer = array_.request();
    std::vector<int64_t> shape(buffer.shape.begin(), buffer.shape.end());
    return TensorFloat::CreateFromArray(shape, {
                                            static_cast<float *>(buffer.ptr),
                                            static_cast<float *>(buffer.ptr) + static_cast<size_t>(buffer.size)
                                        });
}

TensorInt64Bit WinMLValue::AsTensorInt64() const {
    auto buffer = array_.request();
    std::vector<int64_t> shape(buffer.shape.begin(), buffer.shape.end());
    return TensorInt64Bit::CreateFromArray(shape, {
                                               static_cast<int64_t *>(buffer.ptr),
                                               static_cast<int64_t *>(buffer.ptr) + static_cast<size_t>(buffer.size)
                                           });
}

TensorUInt8Bit WinMLValue::AsTensorUInt8() const {
    auto buffer = array_.request();
    std::vector<int64_t> shape(buffer.shape.begin(), buffer.shape.end());
    return TensorUInt8Bit::CreateFromArray(shape, {
                                               static_cast<uint8_t *>(buffer.ptr),
                                               static_cast<uint8_t *>(buffer.ptr) + static_cast<size_t>(buffer.size)
                                           });
}

TensorFloat16Bit WinMLValue::AsTensorFloat16() const {
    auto buffer = array_.request();
    std::vector<int64_t> shape(buffer.shape.begin(), buffer.shape.end());
    return TensorFloat16Bit::CreateFromArray(shape, {
                                                 static_cast<float *>(buffer.ptr),
                                                 static_cast<float *>(buffer.ptr) + static_cast<size_t>(buffer.size)
                                             });
}

TensorDouble WinMLValue::AsTensorDouble() const {
    auto buffer = array_.request();
    std::vector<int64_t> shape(buffer.shape.begin(), buffer.shape.end());
    return TensorDouble::CreateFromArray(shape, {
                                             static_cast<double *>(buffer.ptr),
                                             static_cast<double *>(buffer.ptr) + static_cast<size_t>(buffer.size)
                                         });
}

TensorInt8Bit WinMLValue::AsTensorInt8() const {
    auto buffer = array_.request();
    std::vector<int64_t> shape(buffer.shape.begin(), buffer.shape.end());
    return TensorInt8Bit::CreateFromArray(shape, {
                                              static_cast<uint8_t *>(buffer.ptr),
                                              static_cast<uint8_t *>(buffer.ptr) + static_cast<size_t>(buffer.size)
                                          });
}

TensorUInt16Bit WinMLValue::AsTensorUInt16() const {
    auto buffer = array_.request();
    std::vector<int64_t> shape(buffer.shape.begin(), buffer.shape.end());
    return TensorUInt16Bit::CreateFromArray(shape, {
                                                static_cast<uint16_t *>(buffer.ptr),
                                                static_cast<uint16_t *>(buffer.ptr) + static_cast<size_t>(buffer.size)
                                            });
}

TensorUInt32Bit WinMLValue::AsTensorUInt32() const {
    auto buffer = array_.request();
    std::vector<int64_t> shape(buffer.shape.begin(), buffer.shape.end());
    return TensorUInt32Bit::CreateFromArray(shape, {
                                                static_cast<uint32_t *>(buffer.ptr),
                                                static_cast<uint32_t *>(buffer.ptr) + static_cast<size_t>(buffer.size)
                                            });
}

TensorUInt64Bit WinMLValue::AsTensorUInt64() const {
    auto buffer = array_.request();
    std::vector<int64_t> shape(buffer.shape.begin(), buffer.shape.end());
    return TensorUInt64Bit::CreateFromArray(shape, {
                                                static_cast<uint64_t *>(buffer.ptr),
                                                static_cast<uint64_t *>(buffer.ptr) + static_cast<size_t>(buffer.size)
                                            });
}

TensorInt16Bit WinMLValue::AsTensorInt16() const {
    auto buffer = array_.request();
    std::vector<int64_t> shape(buffer.shape.begin(), buffer.shape.end());
    return TensorInt16Bit::CreateFromArray(shape, {
                                               static_cast<int16_t *>(buffer.ptr),
                                               static_cast<int16_t *>(buffer.ptr) + static_cast<size_t>(buffer.size)
                                           });
}

TensorInt32Bit WinMLValue::AsTensorInt32() const {
    auto buffer = array_.request();
    std::vector<int64_t> shape(buffer.shape.begin(), buffer.shape.end());
    return TensorInt32Bit::CreateFromArray(shape, {
                                               static_cast<int32_t *>(buffer.ptr),
                                               static_cast<int32_t *>(buffer.ptr) + static_cast<size_t>(buffer.size)
                                           });
}

TensorKind WinMLValue::GetTensorKind() const {
    return tensor_kind_;
}

void WinMLValue::DetermineTensorKind() {
    auto dtype = array_.dtype();
    if (dtype.is(pybind11::dtype::of<float>())) {
        tensor_kind_ = TensorKind::Float;
    } else if (dtype.is(pybind11::dtype::of<int64_t>())) {
        tensor_kind_ = TensorKind::Int64;
    } else if (dtype.is(pybind11::dtype::of<uint8_t>())) {
        tensor_kind_ = TensorKind::UInt8;
    } else if (dtype.is(pybind11::dtype::of<float>())) {
        tensor_kind_ = TensorKind::Float16;
    } else if (dtype.is(pybind11::dtype::of<double>())) {
        tensor_kind_ = TensorKind::Double;
    } else if (dtype.is(pybind11::dtype::of<int8_t>())) {
        tensor_kind_ = TensorKind::Int8;
    } else if (dtype.is(pybind11::dtype::of<uint16_t>())) {
        tensor_kind_ = TensorKind::UInt16;
    } else if (dtype.is(pybind11::dtype::of<uint32_t>())) {
        tensor_kind_ = TensorKind::UInt32;
    } else if (dtype.is(pybind11::dtype::of<uint64_t>())) {
        tensor_kind_ = TensorKind::UInt64;
    } else if (dtype.is(pybind11::dtype::of<int16_t>())) {
        tensor_kind_ = TensorKind::Int16;
    } else if (dtype.is(pybind11::dtype::of<int32_t>())) {
        tensor_kind_ = TensorKind::Int32;
    } else {
        throw std::runtime_error("Unsupported numpy data type");
    }
}
